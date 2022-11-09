from rest_framework import permissions
from Main.models import Filial


class PermAddons:
    #
    # Метод проверки, где передан id Филиала
    #
    def checkKwargKeyOrPost(request, view, key):
        if key in view.kwargs:
            result = view.kwargs[key] # Чтобы посмотреть параметры get запроса к view используем view.kwargs!
        else:
            result = request.POST.get(key)# Если id был передан в теле запроса

        return result


#
# Проверка владельца филиала
#
class IsFilialOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        idFilial = PermAddons.checkKwargKeyOrPost(request, view, 'idFilial')

        try:
            filialObj = Filial.objects.get(id=idFilial)
        except Exception:
            return False

        return filialObj.platform_account.user == request.user


#
# Проверка разрешения на включения филиала в тариф
#
class IsFilialIncludeTarif(permissions.BasePermission):
    def has_permission(self, request, view):
        idFilial = PermAddons.checkKwargKeyOrPost(request, view, 'idFilial')

        try:
            filialObj = Filial.objects.get(id=idFilial)
        except Exception:
            return False

        return filialObj.status == 1 or filialObj.status == 2


#
# Проверка запрета на отключение филиала
#
class IsNoneDeactivateFilialStatus(permissions.BasePermission):
    def has_permission(self, request, view):
        status = PermAddons.checkKwargKeyOrPost(request, view, 'statusFilial')

        return status == 1 or status == 2 or status == "1" or status == "2"