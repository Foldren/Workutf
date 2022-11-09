from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.renderers import TemplateHTMLRenderer

from additionalpy.permissions import IsFilialOwner, IsFilialIncludeTarif
from additionalpy.review_methods import PlatformReviewMethods
from apiservices.api_2gis import Api2Gis
from additionalpy.encrypt_util import EncryptDecryptData

from Main.models import Filial, Review, PlatformAccount
from datetime import datetime


class ReviewsViewSet(viewsets.ViewSet):
    renderer_classes = [TemplateHTMLRenderer]
    permission_classes = [IsAuthenticated]


    def list(self, request):
        return Response({
            'app_name': "Rates",
            'page_title': "Отзывы о филиале",
            # "reviews": Api_Reviews.getJsonGoogleReviews(request.user.id, 91, '1xLwQymEmsRG4aXn2_LD1A'),
            # "reviews": Api_Reviews.get2GISReviews()
            }, template_name = "reviews.html")


    #
    # Метод для отображения отзывов филиала
    #
    @action(url_path='filial_reviews/(?P<idFilial>[0-9]+)', url_name='filial_reviews', methods=['get'], permission_classes = [IsFilialOwner, IsFilialIncludeTarif], detail=False)
    def showFilialReviews(self, request, idFilial):
        filialObj = Filial.objects.get(id=idFilial)
        lastDateLoad = filialObj.last_date_load_reviews

        reviewsPlatform = PlatformReviewMethods(filialObj, lastDateLoad, Api2Gis.TIME_REVIEWS_UPDATE)

        if reviewsPlatform.checkRequestLastLoadDate():
            login = filialObj.platform_account.login
            password = EncryptDecryptData.decrypt(filialObj.platform_account.password)
            platformFilialId = filialObj.id_platform_filial

            # авторизуемся в 2гис и подгружаем отзывы
            Api2GisReviews = Api2Gis(login, password)
            reviewsApi = Api2GisReviews.getFilialReviews(platformFilialId)

            # получаем нужный формат отзывов для загрузки в бд
            reviewsListObj = Api2Gis.getFormattedReviewsList(idFilial, reviewsApi)

            reviewsPlatform.bulkUpdateReviewsList(reviewsListObj)

            # обновляем дату загрузки отзывов
            filialObj.last_date_load_reviews = datetime.now()
            filialObj.save()

            del Api2GisReviews

        # подгружаем отзывы из бд
        reviews = Review.objects.filter(filial=filialObj)
        platformAccounts = PlatformAccount.objects.filter(user=request.user)
        filialsUser = Filial.objects.exclude(status=0).select_related("platform_account").filter(platform_account__in=platformAccounts).values("id","address","platform_account__name_organization","platform_account__platform")

        return Response({
            "app_name": "Reviews",
            "page_title": "Отзывы о филиале",
            "filials": filialsUser,
            "filialId": filialObj.id,
            "reviews": reviews,
            "name_organization": filialObj.platform_account.name_organization,
            "address": filialObj.address,
            "platform": filialObj.platform_account.platform,
            }, template_name = "reviews.html")

    #
    # Метод для отображения отзывов филиала
    #
    @action(url_path='change_review_status', url_name='change_review_status', methods=['post'], permission_classes = [IsFilialOwner, IsFilialIncludeTarif], detail=False)
    def changeReviewStatus(self, request, idFilial):
        idFilial = request.POST.get("idFilial")
        statusReview = request.POST.get("statusFilial")

        pass

