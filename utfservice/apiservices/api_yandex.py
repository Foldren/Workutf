from requests import get, Session
from datetime import timedelta
from django.conf import settings
from Main.models import Review
from bs4 import BeautifulSoup


class ApiYandex:
    TIME_BRANCH_UPDATE = timedelta(hours=12)
    TIME_REVIEWS_UPDATE = timedelta(hours=12)

    USER_AGENT = "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1"

    session = 0
    accessToken = ""
    organizationId = ""
    organizationName = ""
    jsonResponseAuth = ""

    proccessUid = ""
    csrfToken = ""


    #
    # Конструктор с функцией авторизации на платформе 2gis
    #
    def __init__(self, login, password):
        self.session = Session()

        # responseAuth = self.session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/start',
        #     data = {
        #         'login': 'autoshkola-rulevoi',
        #         'retpath': 'https://passport.yandex.ru/profile',
        #     },
        #     headers = {
        #         'Accept': 'application/json, text/javascript, */*; q=0.01',
        #         'Accept-Language': 'ru,en;q=0.9',
        #         'Connection': 'keep-alive',
        #         'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        #         'Origin': 'https://passport.yandex.ru',
        #         'Referer': 'https://passport.yandex.ru/',
        #         'Sec-Fetch-Dest': 'empty',
        #         'Sec-Fetch-Mode': 'cors',
        #         'Sec-Fetch-Site': 'same-origin',
        #         'User-Agent': self.USER_AGENT,
        #         'X-Requested-With': 'XMLHttpRequest',
        #         'Y-Browser-Experiments': 'NDgzODI4LDAsLTE=',
        #         'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
        #         'sec-ch-ua-mobile': '?0',
        #         'sec-ch-ua-platform': '"Windows"',
        #      },
        # )

        # responseAuth = self.session.post('https://passport.yandex.ru/auth',
        #     headers = {
        #         'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        #         'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
        #         'Connection': 'keep-alive',
        #         'Referer': 'https://yandex.ru/',
        #         'Sec-Fetch-Dest': 'document',
        #         'Sec-Fetch-Mode': 'navigate',
        #         'Sec-Fetch-Site': 'same-site',
        #         'Sec-Fetch-User': '?1',
        #         'Upgrade-Insecure-Requests': '1',
        #         'User-Agent': self.USER_AGENT,
        #         'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
        #         'sec-ch-ua-mobile': '?1',
        #         'sec-ch-ua-platform': '"Android"',
        #     },
        # )

        responseAuth = self.session.get('https://passport.yandex.ru/auth/list',
            headers = {
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'Accept-Language': 'ru,en;q=0.9',
                'Cache-Control': 'no-cache',
                'Connection': 'keep-alive',
                'Pragma': 'no-cache',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'same-origin',
                'Sec-Fetch-User': '?1',
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': self.USER_AGENT,
                'Y-Browser-Experiments': 'NDgzODI4LDAsLTE=',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        textAuthPage = responseAuth.text

        self.proccessUid = self.getSliceTextParam(textAuthPage, "process_uuid", 13)
        self.csrfToken = self.getSliceTextParam(textAuthPage, "csrf", 19)

        responseAuth = self.session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/start',
            data = {
                'csrf_token': self.csrfToken,
                'login': 'autoshkola-rulevoi@yandex.ru',
                'process_uuid': self.proccessUid,
            },
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'ru,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://passport.yandex.ru',
                'Referer': 'https://passport.yandex.ru/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': self.USER_AGENT,
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        responseAuthJson = responseAuth.json()
        trackId = responseAuthJson["track_id"]


        responseAuth = self.session.post('https://passport.yandex.ru/registration-validations/auth/multi_step/commit_password',
            data = {
                'csrf_token': self.csrfToken,
                'track_id': trackId,
                'password': 'R67304jf!',
                'retpath': 'https://passport.yandex.ru/profile',
            },
            headers = {
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'Accept-Language': 'ru,en;q=0.9',
                'Connection': 'keep-alive',
                'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
                'Origin': 'https://passport.yandex.ru',
                'Referer': 'https://passport.yandex.ru/',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin',
                'User-Agent': self.USER_AGENT,
                'X-Requested-With': 'XMLHttpRequest',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
            }
        )

        responseAuth = self.session.get('https://yandex.ru/sprav/companies',
            headers = {
                'authority': 'yandex.ru',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ru,en;q=0.9',
                'cache-control': 'max-age=0',
                'device-memory': '8',
                'downlink': '10',
                'dpr': '1',
                'ect': '4g',
                'if-none-match': 'W/"2ab11-98lQ5JJylbOtmlFE3TR7NlnaXC8"',
                'referer': 'https://yandex.ru/business/boost',
                'rtt': '50',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.167 YaBrowser/22.7.4.957 Yowser/2.5 Safari/537.36',
                'viewport-width': '1920',
            }
        )


        # if responseAuth.status_code == 200:
        #     self.jsonResponseAuth = responseAuth.json()
            # self.accessToken = "Bearer " + jsonResonseAuth['result']['access_token']
            # self.__loadOrganizationData()
        # else:

        self.jsonResponseAuth = responseAuth.text

    #
    # Диструктор с завершением сессии
    #
    def __del__(self):
        self.session.close()


    @staticmethod
    def getSliceTextParam(text, paramName, offsetStart = 0, offsetEnd = 0):
        paramFindPosition = text.find(paramName)

        pos1 = paramFindPosition + offsetStart
        pos2 = text.find('\"', pos1) + offsetEnd

        return text[pos1:pos2]

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
    # Метод на получение списка филиалов организации 2gis (выводит максимум 50 филиалов!)
    #
    def getDictFilialsItems(self):
        response = self.session.get('https://yandex.ru/sprav/companies',
            params = {
                'limit': 50,
                'page': 1,
            },
            headers = {
                'authority': 'yandex.ru',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ru,en;q=0.9',
                'cache-control': 'no-cache',
                'device-memory': '8',
                'ect': '4g',
                'pragma': 'no-cache',
                'rtt': '50',
                'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Yandex";v="22"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'viewport-width': '1920',
                'y-browser-experiments': 'NDgzODI4LDAsLTE=',
                'user-agent': self.USER_AGENT,
            },
        )

        responseFilials = response.text

        return responseFilials


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