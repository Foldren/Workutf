from requests import get, Session
from datetime import timedelta
from django.conf import settings
from Main.models import Review
from bs4 import BeautifulSoup


# Ограничение: 1000 запросов в месяц на получение списка филиалов
class ApiZoon:
    TIME_BRANCH_UPDATE = timedelta(hours=12)
    TIME_REVIEWS_UPDATE = timedelta(hours=12)

    X_APIKEY = "accweb96f8"
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

    session = 0
    accessToken = ""
    organizationId = ""
    organizationName = ""
    jsonResponseAuth = ""

    ascIdFilial = 'id'
    ascAddressFilial = 'address'
    asUrlFilial = 'url'


    #
    # Конструктор с функцией авторизации на платформе 2gis
    #
    def __init__(self, login, password):
        self.session = Session()

        responseAuth = self.session.post('https://spb.zoon.ru/js.php?area=profile',
            data = {
                'sourceType': "header",
                'prof_id': "",
                'email': "anthon.galitsin@yandex.ru",
                'password': "irulevoi777",
                'action': "login",
            },
            headers = {
                'authority': "spb.zoon.ru",
                'accept': "*/*",
                'accept-language': "ru-RU,ru;q=0.9",
                'content-type': "application/x-www-form-urlencoded; charset=UTF-8",
                # 'cookie': 'city=spb; sid=50ec2370630f42b608401565196888; anon_id=20220831141502pKRt.5c02; _ym_uid=1661944502360400798; _ym_d=1661944502; _ga=GA1.2.967715657.1661944502; _gid=GA1.2.1823379105.1661944502; firstvisitdate=2022-08-31; _ym_isad=2',
                'origin': 'https://spb.zoon.ru',
                'referer': 'https://spb.zoon.ru/',
                'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'empty',
                'sec-fetch-mode': 'cors',
                'sec-fetch-site': 'same-origin',
                'user-agent': self.USER_AGENT,
                'x-requested-with': 'XMLHttpRequest',
            },
        )

        bsPageFilialsHtml = self.getBSFilialsHtml()

        # подгружаем имя организации
        self.organizationName = bsPageFilialsHtml.find(class_='page-title-block').find(itemprop="name").string

        if responseAuth.status_code == 200:
            self.jsonResponseAuth = responseAuth.json()
            # self.accessToken = "Bearer " + jsonResonseAuth['result']['access_token']
            # self.__loadOrganizationData()
        else:
            self.jsonResponseAuth = responseAuth.content

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
    # Метод получения разметки со списком филиалов
    #
    def getBSFilialsHtml(self):
        response = self.session.get('https://business.zoon.ru/lk/info',
            headers = {
                'authority': 'business.zoon.ru',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ru-RU,ru;q=0.9',
                'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'none',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': self.USER_AGENT,
                },
        )

        htmlObjectBusinessPage = BeautifulSoup(response.text, 'lxml')

        # берем ссылку на первый филиал
        filialHtmlUrl = htmlObjectBusinessPage.select_one('.orgs .org .info a')

        # переходим на нее чтобы взять ссылку на список филалов организации
        pageFilialResponse = self.session.get(filialHtmlUrl['href'],
            headers = {
                'authority': 'spb.zoon.ru',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ru-RU,ru;q=0.9',
                'cache-control': 'max-age=0',
                'referer': 'https://zoon.ru/',
                'sec-ch-ua': '"Google Chrome";v="105", "Not)A;Brand";v="8", "Chromium";v="105"',
                'sec-ch-ua-mobile': '?0',
                'sec-ch-ua-platform': '"Windows"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-site',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': self.USER_AGENT,
            },
        )



        pageFilialHtml = BeautifulSoup(pageFilialResponse.text, 'lxml')

        # получаем ссылку на все филалы с адресами
        urlFilials = pageFilialHtml.find("dt", string="Адреса сети").find_next("a")['href']

        # переходим на нее чтобы собрать данные по организациям
        pageFilialsResponse = self.session.get(urlFilials,
            headers = {
                'authority': 'spb.zoon.ru',
                'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
                'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
                'cache-control': 'no-cache',
                'pragma': 'no-cache',
                'referer': 'https://spb.zoon.ru/trainings/avtoshkola_rulevoi_na_kushelevskoj_doroge/',
                'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
                'sec-ch-ua-mobile': '?1',
                'sec-ch-ua-platform': '"Android"',
                'sec-fetch-dest': 'document',
                'sec-fetch-mode': 'navigate',
                'sec-fetch-site': 'same-origin',
                'sec-fetch-user': '?1',
                'upgrade-insecure-requests': '1',
                'user-agent': self.USER_AGENT,
            },
        )

        return BeautifulSoup(pageFilialsResponse.text, 'lxml')

    #
    # Метод на получение списка филиалов организации 2gis
    #
    def getDictFilialsItems(self):
        pageFilialsHtml = self.getBSFilialsHtml()

        # подгружаем филиалы
        filialsTagObjects = pageFilialsHtml.find(attrs={'data-uitest': 'results-container'}).find_all("li", recursive=False)

        filialsListDict = list()

        # Собираем нужные атрибуты
        for element in filialsTagObjects:
            filialsListDict.append({
                'id': element.get('data-id'),
                'address': element.find(class_="address").string,
                'url': element.find(attrs={'data-uitest': 'org-link'})['href']
            })

        return filialsListDict


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