from Main.models import Review
from datetime import datetime, timedelta
from django.core import serializers
import json


class DateAdds:
    @staticmethod
    def getSubNowAndDate(difDate):
        return datetime.now() - difDate


class PlatformReviewMethods:
    filialObj = int()
    last_date_load = datetime.now()
    time_review_update = timedelta(hours=12)


    def __init__(self, filialO, lastDateLoad, timeRevwUpdate):
        self.filialObj = filialO
        self.last_date_load = lastDateLoad
        self.time_review_update = timeRevwUpdate


    #
    # Метод определения превышения лимита запросов по времени
    # (tzinfo - информация о часовом поясе)
    #
    # last_date_change - время последней загрузки отзывов
    # time_review_update - лимит на следующее обновление
    #
    def checkRequestLastLoadDate(self):
        return DateAdds.getSubNowAndDate(self.last_date_load.replace(tzinfo=None)) >= self.time_review_update


    #
    # Обновление полей существующих отзывов
    #
    def __updateFieldsReviews(self, reviewBdObj, reviewReqObj):
        reviewBdObj.content = reviewReqObj.content
        reviewBdObj.rating = reviewReqObj.rating
        reviewBdObj.author_name = reviewReqObj.author_name
        reviewBdObj.author_url = reviewReqObj.author_url
        reviewBdObj.profile_photo_url = reviewReqObj.profile_photo_url
        reviewBdObj.relative_time_description = reviewReqObj.relative_time_description
        reviewBdObj.time = reviewReqObj.time

        reviewBdObj.save()


    #
    # Метод проверки на новые отзывы (по id на платформе)
    # Удаляет удаленные с сервисов отзывы! Обновляет данные измененных отзывов!
    #
    def __checkReview(self, listObjReqReviews):
        reviewsBD = Review.objects.filter(filial=self.filialObj)
        newReviewsList = list()
        idsNewReviews = list()

        for reviewRequest in listObjReqReviews:
            try:
                reviewBD = reviewsBD.get(id_platform_review=reviewRequest.id_platform_review)
            except:
                newReviewsList.append(reviewRequest)
                idsNewReviews.append(reviewRequest.id_platform_review)
                continue

            self.__updateFieldsReviews(reviewBD, reviewRequest)
            idsNewReviews.append(reviewRequest.id_platform_review)

        # Удаляем отзывы которых нет в списке отзывов из запроса
        reviewsBD.exclude(id_platform_review__in=idsNewReviews).delete()

        return newReviewsList


    #
    # Метод универсальной загрузки отзывов в базу данных
    #
    # listModelsReviews - список model объектов отзывов
    #
    def bulkUpdateReviewsList(self, listModelsReviews):
        newListModelsReviewsObj = list()
        newListModelsReviewsObj = self.__checkReview(listModelsReviews)

        self.filialObj.last_date_load_reviews = datetime.now()
        self.filialObj.save()

        Review.objects.bulk_create(newListModelsReviewsObj)

