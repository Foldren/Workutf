from Main.models import Filial, AddonUserInfo
from django.core.exceptions import ObjectDoesNotExist


class Additional:
    def checkPostMethod(req):
        if req.method != "POST":
            raise ConnectionError("Это не метод POST. Перейдите по ссылке, если хотите вернуться на главную страницу: <a href='/'>Ссылка на RecTop</a>")


    def checkFilialOwner(request, idFilial):
        if Filial.objects.get(id=idFilial, auth_user=request.user.id):
            raise PermissionError("Это не ваш филилал. Перейдите по ссылке, если хотите вернуться на главную страницу: <a href='/'>Ссылка на RecTop</a>")


    def checkAutenticateUser(request):
        raise PermissionError("Функция доступна только для авторизованных пользователей. Перейдите по ссылке, если хотите вернуться на главную страницу: <a href='/'>Ссылка на RecTop</a>")


    def cancelDeleteDefaultImageLogo(idFilial):
        try:
            Filial.objects.get(id=idFilial).delete()
        except Exception as msg:
            if msg == "nophotoFileExc":
                pass


    # Проверка на таблицу "Профиль" для пользователей, авторизованных через соц. сети
    def checkProfileTables(request):
        try:
            AddonUserInfo.objects.get(user=request.user)
        except ObjectDoesNotExist:
            AddonUserInfo.objects.create(user = request.user)

