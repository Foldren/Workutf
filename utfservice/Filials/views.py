from Main.models import Filial, PlatformAccount
from django.http import HttpResponse

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from additionalpy.permissions import IsFilialOwner, IsFilialIncludeTarif, IsNoneDeactivateFilialStatus


class FilialsViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]


    def list(self, request):
        user = request.user
        platformAccountsObjects = PlatformAccount.objects.filter(user=request.user)
        filialsObjects = Filial.objects.exclude(status=0).select_related("platform_account").filter(platform_account__in=platformAccountsObjects).values("id", "address","status","logotype","platform_account__name_organization","qr_code_img_url")

        return Response({
            'app_name': "Filials",
            'page_title': "Список филиалов пользователя: " + user.username,
            "filials": filialsObjects,
        }, template_name='filials.html')


    @action(url_path='change_status_filial', url_name='change_status_filial', methods=['post'], permission_classes=[IsFilialOwner, IsFilialIncludeTarif, IsNoneDeactivateFilialStatus], detail=False)
    def changeStatusFilial(self, request):
        idFilial = request.POST.get('idFilial')
        statusFilial = request.POST.get('statusFilial')

        Filial.objects.filter(id=idFilial).update(status=statusFilial)

        return HttpResponse(1)
