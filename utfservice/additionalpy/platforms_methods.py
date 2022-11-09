from Main.models import Filial, PlatformAccount
from datetime import datetime, timedelta
from django.core import serializers
import json

from apiservices.api_2gis import Api2Gis
from apiservices.api_yandex import ApiYandex
from apiservices.api_zoon import ApiZoon

class DateAdds:
    @staticmethod
    def getSubNowAndDate(difDate):
        return datetime.now() - difDate


class PlatformFilialsMethods():
    platformAccount = PlatformAccount()
    last_date_load_filials = datetime.now()

    # Ограничение на следующую загрузку филиалов
    limit_time_filials_load = timedelta(hours=12)


    def __init__(self, account, limitTFilialsLoad):
        self.platformAccount = account
        self.last_date_load_filials = account.last_date_load_filials
        self.limit_time_filials_load = limitTFilialsLoad


    @staticmethod
    def getSliceTextParam(text, paramName, offsetStart = 0, offsetEnd = 0):
        paramFindPosition = text.find(paramName)

        pos1 = paramFindPosition + offsetStart
        pos2 = text.find('\"', pos1) + offsetEnd

        return text[pos1:pos2]


    @staticmethod
    def getApiAuthObject(platformNumber, login, password):
        if platformNumber == 0 or platformNumber == "0": #Яндекс
            resultObj = ApiYandex(login, password)

        elif platformNumber == 1 or platformNumber == "1": #2GIS
            resultObj = Api2Gis(login, password)

        elif platformNumber == 2 or platformNumber == "2": #Google
            pass

        elif platformNumber == 3 or platformNumber == "3": #Flamp
            pass

        elif platformNumber == 4 or platformNumber == "4": #Zoon
            resultObj = ApiZoon(login, password)

        elif platformNumber == 5 or platformNumber == "5": #Yell
            pass

        return resultObj


    #
    # Метод определения превышения лимита запросов по времени
    # (tzinfo - информация о часовом поясе)
    #
    # last_date_load_filials - время последней загрузки филиалов
    # limit_time_filials_load - лимит на следующее обновление
    #
    def checkRequestLastLoadDate(self):
        return DateAdds.getSubNowAndDate(self.last_date_load_filials.replace(tzinfo=None)) >= self.limit_time_filials_load


    #
    # Проверка полей (адрес), изменение в случае разницы (позже сделать проверку на изменение телефона)
    #
    def __checkDiffAddressFilialAndUpdate(self, filialBdObj, filialReqObj):
        if filialBdObj.address != filialReqObj.address:
            filialBdObj.address = filialReqObj.address
            filialBdObj.save()


    #
    # Метод проверки на новые филиалы (по id на платформе)
    # Удаляет удаленные с сервисов филиалы! Обновляет адрес измененных филиалов!
    #
    def __checkFilials(self, listObjFilials):
        filialsBD = Filial.objects.filter(platform_account=self.platformAccount)

        if not filialsBD:
            return listObjFilials

        newFilialsList = list()
        idsNewFilials = list()

        for filialRequest in listObjFilials:
            try:
                filialBD = filialsBD.get(id_platform_filial=filialRequest.id_platform_filial)
            except:
                newFilialsList.append(filialRequest)
                idsNewFilials.append(filialRequest.id_platform_filial)
                continue

            self.__checkDifferenceAndUpdate(filialBD, filialRequest)
            idsNewFilials.append(filialRequest.id_platform_filial)

        # Удаляем филиалы которых нет в списке филиалов из запроса
        filialsBD.objects.exclude(id_platform_filial__in=idsNewFilials).delete()

        return newFilialsList


    #
    # Метод универсальной подгрузки новых филиалов в базу данных
    #
    # listDictFilials - список dict объектов филиалов
    # nameAsc, addressAsc..  - индексы свойств dict объекта филиалов
    #
    def bulkUpdateFilialsList(self, listDictFilials, idPlatformFilialAsc, addressAsc):
        filialsListObj = list()

        for filial in listDictFilials:
            filialsListObj.append(
                Filial(
                    platform_account = self.platformAccount,
                    id_platform_filial = filial[f'{idPlatformFilialAsc}'],
                    address = filial[f'{addressAsc}'],
                    status = 0,
                )
            )

        updateFilialsList = self.__checkFilials(filialsListObj)
        Filial.objects.bulk_create(updateFilialsList)


    #
    # Метод получения dict объектов филиалов из базы данных
    #
    def getFilialsJsonFromDb(self):
        fieldsFilials=['id_platform_filial', 'address', 'status']

        filialsStringJson = serializers.serialize("json", Filial.objects.filter(platform_account=self.platformAccount), fields=fieldsFilials)
        filialsDict = json.loads(filialsStringJson)

        filials = [element['fields'] for element in filialsDict]

        return json.dumps(filials)
