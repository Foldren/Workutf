from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from django.http import HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.contrib.auth import authenticate, login, logout

from Main.models import AddonUserInfo
from additionalpy.requests_check import Additional

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.decorators import action



class MainViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]

    #
    # Корневой метод класса, url_name = main-list
    #
    def list(self, request, successRegAlert = 0):
        if not request.user.is_anonymous:
            Additional.checkProfileTables(request)

        return Response({
            'app_name': 'Main',
            'page_title': "RecTop - Сервис взаимодействия с клиентами",
            'successRegAlert': successRegAlert,
        }, template_name = 'main.html')


    #
    # Метод для регистрации нового пользователя с отправкой на email подтверждения
    #
    @action(url_path='reg_new_user', url_name='reg_new_user', methods=['post'], detail=False)
    def registrationNewUser(self, request):
        try:
            login = request.POST.get('login')
            email = request.POST.get('email')
            password = request.POST.get('password')
            verifyC = ""

            try:
                #генерируем код верификации
                flagExit = 0
                while(flagExit != 1):
                    try:
                        verifyC = get_random_string(length=200)
                        AddonUserInfo.objects.get(verify_code = verifyC)
                    except ObjectDoesNotExist:
                        flagExit = 1

                #добавляем разметку для тела сообщения
                msg = render_to_string('../templates/verifyMessage.html', {'loginVal': login, 'verifyCode': verifyC, 'site_url': settings.SITE_URL})

                #создаем пользователя и добавляем в группу
                user = User.objects.create_user(
                    username = login,
                    email = email,
                    password = password,
                    is_active = 0)

                group = Group.objects.get(name='Пользователи')
                user.groups.add(group)

                #прикрепляем код к аккаунту
                profileUser = AddonUserInfo.objects.create(
                    user_id = user.id,
                    verify_code = verifyC,
                )

                user.profile = profileUser
                user.save()

                #отправляем сообщение
                send_mail(
                    subject = 'Добро пожаловать на платформу RecTop!',
                    message = 'Для подтверждения аккаунта <b>' + login + '</b> перейдите по ссылке:',
                    from_email = settings.DEFAULT_FROM_EMAIL,
                    recipient_list = [email],
                    html_message = msg,
                    fail_silently = False,
                )
            except BadHeaderError:
                raise BadHeaderError('Кто-то изменил header')

        except ValidationError:
            raise ValidationError('Логин содержит недопустимые символы')

        except IntegrityError:
            raise IntegrityError('Данное имя пользователя уже занято')

        return HttpResponse("Isaac you did it!")


    #
    # Метод для авторизации нового пользователя с проверкой ключа подтверждения
    #
    @action(url_path='auth_new_user', url_name='auth_new_user', methods=['get'], detail=False)
    def authorizationNewUser(self, request):
        verifyC = request.GET.get('verifyCode')

        try:
            profile = AddonUserInfo.objects.get(verify_code = verifyC)
        except:
            return HttpResponse("Код верификации не верный или ссылка уже не активна")

        user = User.objects.get(id = profile.user_id)
        user.is_active = 1
        user.save()
        profile.delete()

        login(request, user, backend='django.contrib.auth.backends.ModelBackend')

        return self.list(request, 1)


    #
    # Метод авторизации пользователя
    #
    @action(url_path='auth_user', url_name='auth_user', methods=['post'], detail=False)
    def authorizationUser(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
        else:
            return HttpResponse("Логин или пароль заданы не верно")

        return HttpResponse("You are welcome")


    #
    # Метод деавторизации пользователя
    #
    @action(url_path='log_out_user', url_name='log_out_user', methods=['post'], detail=False)
    def logOutUser(self, request):
        logout(request)
        return HttpResponse("You are log out")
