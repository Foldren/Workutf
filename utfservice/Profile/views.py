from Main.models import PlatformAccount, AddonUserInfo, Filial
from django.http import HttpResponse
from datetime import datetime

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from additionalpy.encrypt_util import EncryptDecryptData
from django.contrib.auth.models import User

from apiservices.api_2gis import Api2Gis
from apiservices.api_yandex import ApiYandex
from apiservices.api_zoon import ApiZoon

from additionalpy.platforms_methods import PlatformFilialsMethods
from django.core.files.storage import FileSystemStorage

import qrcode
from PIL import Image

import json


class ProfileViewSet(viewsets.ViewSet):
    # Обязательный параметр queryset = Platform.objects.all(), либо установить basename в urls route, для маршрутизации
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes=[IsAuthenticated]


    def list(self, request):
        accountsObjs = PlatformAccount.objects.filter(user=request.user)
        addonsProfile = AddonUserInfo.objects.get(user=request.user)

        return Response({
            'app_name': "Profile",
            'page_title': "Профиль пользователя",
            'additional_data_profile': addonsProfile,
            'accounts': accountsObjs,
        }, template_name="profile.html")


    #
    # Метод для обновления данных профиля
    #
    @action(url_path='save_profile', url_name='save_profile', methods=['post'], detail=False)
    def saveProfileData(self, request):
        userN= request.POST.get('nameUser')
        nameOrg = request.POST.get('nameOrganization')
        mail = request.POST.get('email')
        phone = request.POST.get('number')
        fullname = request.POST.get('full_name')


        AddonUserInfo.objects.filter(user=request.user).update(
            name_organization = nameOrg,
            phone_number = phone,
            full_name = fullname,
        )

        User.objects.filter(id=request.user.id).update(
            username = userN,
            email = mail,
        )

        return HttpResponse(1)


    #
    # Метод добавления аккаунта сервиса
    #
    @action(url_path='add_platform_account', url_name='add_platform_account', methods=['post'], detail=False)
    def addAccount(self, request):
        loginP = request.POST.get('login')
        passwordP = request.POST.get('password')
        platformP = request.POST.get('platformRadio')

        # выведет ошибку в случае неверного пароля
        if PlatformAccount.objects.filter(user=request.user, platform=platformP, login=loginP):
            raise ValueError("Вы уже добавили этого пользователя")
        else:
            authObj = PlatformFilialsMethods.getApiAuthObject(platformP, loginP, passwordP)

        PlatformAccount.objects.create(
            user = request.user,
            platform = platformP,
            login = loginP,
            password = EncryptDecryptData.encrypt(passwordP),
            id_organization = authObj.organizationId,
            name_organization = authObj.organizationName,
        )

        del authObj

        return HttpResponse(1)


    #
    # Метод подгрузки филиалов профиля
    #
    @action(url_path='load_platform_filials', url_name='load_platform_filials', methods=['post'], detail=False)
    def loadFilials(self, request):
        accountId = request.POST.get('accountId')
        platformAccount = PlatformAccount.objects.get(id=accountId)
        accountFilialsObj = PlatformFilialsMethods(platformAccount, Api2Gis.TIME_BRANCH_UPDATE)


        if accountFilialsObj.checkRequestLastLoadDate():
            apiSession = PlatformFilialsMethods.getApiAuthObject(
                platformAccount.platform, # Платформа
                platformAccount.login, # Логин
                EncryptDecryptData.decrypt(platformAccount.password) # Пароль расшифрованный
            )

            # filialsReqObjs = apiSession.getDictFilialsItems()

            # try:
            #     accountFilialsObj.bulkUpdateFilialsList(filialsReqObjs, apiSession.ascIdFilial, apiSession.ascAddressFilial)
            # except Exception as msg:
            #     if msg == "nophotoFileExc":
            #         pass

            answerTest = apiSession.jsonResponseAuth

            del apiSession

            # platformAccount.last_date_load_filials = datetime.now()
            # platformAccount.save()

        # filialsResultObjs = accountFilialsObj.getFilialsJsonFromDb()

        return HttpResponse(json.dumps(answerTest))


    #
    # Метод подключения новых филиалов к аккаунту
    #
    @action(url_path='include_filials', url_name='include_filials', methods=['post'], detail=False)
    def includeFilials(self, request):
        filials = request.POST.getlist('filials')
        filialsPlatform = request.POST.get('filial-platform')

        platformObj = PlatformAccount.objects.get(user=request.user, platform=filialsPlatform)
        includedFilials = Filial.objects.filter(platform_account=platformObj, id_platform_filial__in=filials)
        includedFilials.update(status=2)

        for filial in includedFilials:
            filial.qr_url = f'https://www.rectop.ru/qrcoderates/{filial.id}'

            qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H) #Ставим самый высокий уровень проверки ошибок H
            qr.add_data(filial.qr_url) # Прикрепляем ссылку к Qr коду
            qr.make()

            qrImg = qr.make_image(fill_color="black", back_color="white").convert('RGB')
            logo = Image.open("/home/workutf/utfservice/static/images/qr_code_favicon.jpg")
            pos = ((qrImg.size[0] - logo.size[0]) // 2, (qrImg.size[1] - logo.size[1]) // 2)

            qrImg.paste(logo, pos) #вставляем посередине логотип

            fs = FileSystemStorage(
                location="/home/workutf/utfservice/media/filial/qrcode",
                base_url="filial/qrcode",
            )

            # Генерируем уникальное имя для файла в нашей директории qrcode
            validNameImg = fs.get_available_name("QRcode.png")
            qrImgUrl = f'/home/workutf/utfservice/media/filial/qrcode/{validNameImg}'

            qrImg.save(qrImgUrl, format="png")

            filial.qr_code_img_url = f'/media/filial/qrcode/{validNameImg}'
            filial.logotype = '/media/filial/logotype/nophoto.png'


        Filial.objects.bulk_update(includedFilials, ['qr_url', 'logotype', 'qr_code_img_url'])

        return HttpResponse(1)