from requests import get, Session
from datetime import timedelta
from django.conf import settings
from Main.models import Review


# Ограничение: 1000 запросов в месяц на получение списка филиалов
class Api2Gis:
    TIME_BRANCH_UPDATE = timedelta(hours=12)
    TIME_REVIEWS_UPDATE = timedelta(hours=12)

    X_APIKEY = "accweb96f8"
    USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

    session = 0
    accessToken = ""
    organizationId = ""
    organizationName = ""

    ascIdFilial = "id"
    ascAddressFilial = "address_name"
    asUrlFilial = "url"

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
            self.__loadOrganizationData()
        else:
            raise ValueError("Пользователя не существует, либо указан неверный пароль")

    #
    # Диструктор с завершением сессии
    #
    def __del__(self):
        self.session.close()


    #
    # Метод на получение форматированного списка моделей отзывов 2Gis
    #
    @staticmethod
    def getFormattedReviewsList(filialId, reviewsApiList):
        reviewsFListObj = list()

        for review in reviewsApiList:
            reviewsFListObj.append(
                Review(
                    filial_id = filialId,
                    id_platform_review = review["id"],
                    rating = review["rating"],
                    content = review["text"],
                    time = review["dateCreated"],
                    author_name = review["user"]["name"],
                    author_url = "#",
                    profile_photo_url = review["user"]["photoPreviewUrls"]["320x"],
                    relative_time_description = "",
                    answerable = review["allowedActions"]["reply"],
                )
            )

        return reviewsFListObj


    #
    # Метод на загрузку id организации 2gis
    #
    def __loadOrganizationData(self):
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
        self.organizationName = jsonResponseOrgId['result']['orgs'][0]['name']


    #
    # Метод на получение списка филиалов организации 2gis
    #
    def getDictFilialsItems(self):
        response = get('https://catalog.api.2gis.com/2.0/catalog/branch/list',
            params = {
                'key': settings.API_KEY_2GIS,
                'org_id': self.organizationId,
            }
        )

        responseFilials = response.json()

        return responseFilials['result']['items']


    #
    # Метод на получение списка отзывов филиала
    #
    def getFilialReviews(self, filial_2gis_id):
        response = self.session.get(f'https://api.account.2gis.com/api/1.0/presence/branch/{filial_2gis_id}/reviews',
            params = {
                "pinRequestedFirst": "false",
                "limit": "50",
            },
            headers = {
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

        responseJson = response.json()

        return responseJson['result']['items']


    #
    # Метод для отправки ответа на отзыв (сделать проверку на то что отзыв с 2гис!)
    #
    def sendAnswerOnReview(self, msg):
        response = self.session.post("https://api.account.2gis.com/api/1.0/presence/reviews/35554824/comments",
            json = {
                "catalog": "2gis",
                "isOfficialAnswer": False,
                "text": msg,
            },
            headers = {
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

        return response.json()


    # #
    # # Метод на получение списка всех отзывов организации
    # #
    # # Ограничение: 1000 запросов в месяц
    # #
    # def getFilialReviews(self):
    #     response = self.session.get(f'https://api.account.2gis.com/api/1.0/presence/org/{self.organizationId}/reviews',
    #         params = {
    #             "pinRequestedFirst": "false",
    #             "limit": "50",
    #         },
    #         headers = {
    #             "accept": "application/json, text/plain, */*",
    #             "accept-language": "ru,en;q=0.9",
    #             "authorization": self.accessToken,
    #             "content-type": "application/json",
    #             "locale": "ru",
    #             "origin": "https://account.2gis.com",
    #             "referer": "https://account.2gis.com/",
    #             "sec-fetch-dest": "empty",
    #             "sec-fetch-mode": "cors",
    #             "sec-fetch-site": "same-site",
    #             "user-agent": self.USER_AGENT,
    #             "x-api-key": self.X_APIKEY,
    #         }
    #     )

    #     return response.json()