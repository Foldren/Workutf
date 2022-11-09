from django.http import HttpResponse
from Main.models import Filial, Question, PlatformAccount
from django.core.files.storage import FileSystemStorage

from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from additionalpy.permissions import IsFilialOwner, IsFilialIncludeTarif, IsNoneDeactivateFilialStatus


class DashboardViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated&IsFilialOwner&IsFilialIncludeTarif]


    def list(self, request, idFilial):
        platformAccount = PlatformAccount.objects.filter(user=request.user)
        filialObj = Filial.objects.get(platform_account__in=platformAccount, id=idFilial)
        questionsObj = Question.objects.select_related("filial").filter(filial=filialObj)

        return Response({
            'app_name': "Dashboard",
            'page_title': "Панель администрирования филиалов",
            'filial': filialObj,
            'questions': questionsObj,
            }, template_name = 'dashboard.html')


    @action(url_path='change_main_info_filial', url_name='change_main_info_filial', methods=['post'], permission_classes=[IsNoneDeactivateFilialStatus], detail=False)
    def changeMainInfoFilial(self, request, idFilial):
        logotype = request.FILES.get('logotype')
        statusFilial = request.POST.get('statusFilial')
        filialObj = Filial.objects.get(id=idFilial)

        if logotype:
            if 'image' in logotype.content_type:
                fs = FileSystemStorage(
                    location="/home/workutf/utfservice/media/filial/logotype",
                    base_url="/media/filial/logotype")

                # удаляем текущую картинку
                if filialObj.logotype.name != "nophoto.png":
                    fs.delete(str(filialObj.logotype).removeprefix("/media/filial/logotype/"))

                # сохранение новую в файловой системе
                filenameLogo = fs.save("logotype.png", logotype)

                # получение адреса, по которому лежит файл
                logotypeOrgImgUrl = fs.url(filenameLogo)
            else:
                return HttpResponse("Недопустимый формат файла: 0")
        else:
            logotypeOrgImgUrl = filialObj.logotype

        filialObj.logotype = logotypeOrgImgUrl
        filialObj.status = statusFilial
        filialObj.save()

        return HttpResponse(1)


    @action(url_path='save_widget_filial', url_name='save_widget_filial', methods=['post'], detail=False)
    def saveWidgetFilial(self, request, idFilial):
        questions = request.POST.getlist('question')
        typeWidget = request.POST.get('type_charge')
        volumeCashback = request.POST.get('volume_cashback')
        questionsListObj = list()

        filialObj = Filial.objects.get(id=idFilial)

        filialObj.widget_type = typeWidget
        filialObj.widget_sum = volumeCashback
        filialObj.save()

        Question.objects.filter(filial_id=idFilial).delete()

        for content_quest in questions:
            questionsListObj.append(Question(filial=filialObj, content_text=content_quest))

        Question.objects.bulk_create(questionsListObj)


        return HttpResponse(questions)