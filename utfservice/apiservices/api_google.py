from requests import get, Session
from datetime import timedelta
from django.conf import settings
from .review_methods import ReviewMethods
from Main.models import AddonUserInfo
import json
from datetime import datetime, timedelta


# Ограничения: 100 000 запросов в месяц, ключ работает только по заданному ip и только в определенном сервисе
# (изменить можно в консоли google https://console.cloud.google.com)
#
class ApiGoogle:
    TIME_BRANCH_UPDATE = timedelta(hours=24)
    TIME_LOAD_REVIEWS = timedelta(hours=24)
    TIME_REPLY_REVIEW = timedelta(hours=24)

    X_APIKEY = "accweb96f8"
    USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

    session = 0
    accessToken = ""
    organizationId = ""

    #
    # Конструктор с функцией авторизации на платформе 2gis
    #
    def __init__(self, login, password):
        self.session = Session()

        responseAuth = self.session.post('https://api.account.2gis.com/api/1.0/users/auth',
            json = {
                "login": login,
                "password": password,
            },
            headers = {
                "accept": "application/json, text/plain, */*",
                "accept-language": "ru,en;q=0.9",
                "content-type": "application/json",
                "locale": "ru",
                "origin": "https://account.2gis.com",
                "referer": "https://account.2gis.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": self.USER_AGENT,
                "x-api-key": self.X_APIKEY,
            }
        )

        if responseAuth.status_code == 200:
            jsonResonseAuth = responseAuth.json()
            self.accessToken = "Bearer " + jsonResonseAuth['result']['access_token']
            self.__loadIdOrganization()
        else:
            raise("Ошибка авторизации")

    #
    # Диструктор с завершением сессии
    #
    def __del__(self):
        self.session.close()


    #
    # Метод на загрузку id организации 2gis
    #
    def __loadIdOrganization(self):
        responseOrgId = self.session.get('https://api.account.2gis.com/api/1.0/users',
            headers = {
                "authority": "api.account.2gis.com",
                "accept": "application/json, text/plain, */*",
                "accept-language": "ru,en;q=0.9",
                "authorization": self.accessToken,
                "content-type": "application/json",
                "locale": "ru",
                "origin": "https://account.2gis.com",
                "referer": "https://account.2gis.com/",
                "sec-fetch-dest": "empty",
                "sec-fetch-mode": "cors",
                "sec-fetch-site": "same-site",
                "user-agent": self.USER_AGENT,
                "x-api-key": self.X_APIKEY,
            }
        )

        jsonResponseOrgId = responseOrgId.json()
        self.organizationId = jsonResponseOrgId['result']['orgs'][0]['id']


    #
    # Метод на получение списка организации 2gis
    #
    # Ограничение: 1000 запросов в месяц
    #
    def getDictFilialsIdAndAddress(self):
        response = get('https://catalog.api.2gis.com/2.0/catalog/branch/list',
            params = {
                'key': settings.API_KEY_2GIS,
                'org_id': self.organizationId,
            },
        )

        responseFilials = response.json()
        resultFilialsInfo = dict()

        # Выводим только адрес и id
        for filial in responseFilials['result']['items']:
            resultFilialsInfo[filial['id']] = filial['address_name']

        return resultFilialsInfo


    def getGoogleReviews(self, request_user_id, request_filial_id, place_id, lang='ru'):
        lastDateLoad = AddonUserInfo.objects.get(user_id=request_user_id).last_date_load_google

        googleReviews = ReviewMethods(request_filial_id, lastDateLoad, self.TIME_LOAD_REVIEWS)

        if(googleReviews.checkRequestLastLoadDate()):
            response = get('https://maps.googleapis.com/maps/api/place/details/json',
                params = {
                    'key': 'AIzaSyA3Fve6JXGiSWR8UnPZug-gIQlrfI9aTR0',
                    'place_id': 'ChIJ-1xLwQymEmsRG4aXn2_LD1A',
                    'fields': 'url,review,rating',
                    'language': lang,
                }
            )

            if response.status_code != 200:
                return response.status_code
            else:
                responseAnswer = json.loads(response.text)
                dictReviews = responseAnswer['result']['reviews']

                googleReviews.bulkUpdateReviewsList(
                    listDictReviews = dictReviews,
                    service = 1, # 1 - Google
                    ratingIndex = "rating",
                    contentIndex = "text",
                    timeIndex = "time",
                    nameIndex = "author_name",
                    authUrlIndex = "author_url",
                    profPhotoIndex = "profile_photo_url",
                    relTimeIndex = "relative_time_description"
                )

                newProfile = AddonUserInfo.objects.get(user_id=request_user_id)
                newProfile.last_date_load_google = datetime.now()
                newProfile.save()

                return dictReviews

        else:
            return googleReviews.getReviewsJsonFromDb()