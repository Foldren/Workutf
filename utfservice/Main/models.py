from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, timedelta


PLATFORMS_LIST = [
        (0, 'Yandex'),
        (1, '2GIS'),
        (2, 'Google'),
        (3, 'Flamp'),
        (4, 'Zoon'),
        (5, 'Yell')]

TARIFF_LIST = [
        (1, 'Генератор отзывов'),
        (2, 'Какое-то название'),
        (3, 'Репутация под ключ'),]


class AddonUserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_company = models.CharField(max_length=200, verbose_name="Юр. Лицо", blank=True)
    phone_number = models.IntegerField(verbose_name="Номер телефона", default=False, blank=True)
    full_name = models.CharField(max_length=200, blank=True, verbose_name="Полное имя")

    # Код верификации для подтверждения регистрации через почту
    verify_code = models.TextField(max_length=200, default="Авторизован через соц.сети", blank=True)
    tariff = models.IntegerField(choices=TARIFF_LIST, default=0, verbose_name="Тариф")

    class Meta:
        db_table = 'additional_user_info'
        verbose_name = 'Доп. даннные профиля'
        verbose_name_plural = "Доп. данные профилей"



class PlatformAccount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Владелец аккаунта")
    platform = models.IntegerField(choices=PLATFORMS_LIST, default=False)

    # Id организации и другие данные в сервисе
    id_organization = models.CharField(max_length=200, default="", verbose_name="Id организации")
    name_organization = models.CharField(max_length=200, verbose_name="Название организации", blank=True)
    login = models.CharField(max_length=100, verbose_name="Логин")
    password = models.CharField(max_length=150, verbose_name="Пароль")

    # Последняя дата загрузки всех отзывов (фиксируется ограничением по запросам к платформе)
    last_date_load_reviews = models.DateTimeField(default=datetime.now()-timedelta(hours=13))

    # Последняя дата загрузки филиалов (фиксируется ограничением по запросам к платформе)
    last_date_load_filials = models.DateTimeField(default=datetime.now()-timedelta(hours=13))

    # Количество ответов на отзывы (в будущем фиксируется тарифом)
    types_answer_review = models.IntegerField(default=0, verbose_name="Количество ответов")

    class Meta:
        db_table = 'platform_account'
        verbose_name = 'Аккаунт с сервисов'
        verbose_name_plural = "Аккаунты с сервисов"



class Filial(models.Model):
    STATUS_LIST = [
        (0, 'Подгружен с сервиса'),
        (1, 'Активирован'),
        (2, 'Невидимый'),]

    TYPE_LIST = [
        (0, 'В процентах'),
        (1, 'В сумме'),
        (2, 'Бесплатно'),]

    platform_account = models.ForeignKey(PlatformAccount, on_delete = models.CASCADE, verbose_name="Владелец", editable=True)

    # Данные филиала с платформы
    id_platform_filial = models.CharField(max_length=200, default="", verbose_name="Id филиала на платформе")
    address = models.CharField(max_length=250, default="", verbose_name="Адрес филиала")

    # Логотип филиала (виден только на платформе RecTop)
    logotype = models.ImageField(upload_to='filial/logotype', max_length=300, verbose_name="Логотип")

    status = models.IntegerField(choices=STATUS_LIST, default=0, verbose_name="Статус")

    # Последняя дата загрузки отзывов филиала (фиксируется ограничением по запросам к платформе)
    last_date_load_reviews = models.DateTimeField(default=datetime.now()-timedelta(hours=13))

    # QR код
    qr_code_img_url = models.ImageField(upload_to='filial/qrcode', max_length=300, verbose_name="QR Код - ссылка на картинку")
    qr_url = models.CharField(max_length=300, default="", verbose_name="Ссылка для QR Кода")

    # Конфигурация виджета
    widget_type = models.IntegerField(choices=TYPE_LIST, default=False, verbose_name="Тип")
    widget_sum = models.IntegerField(default=False, verbose_name="Сумма")

    class Meta:
        db_table = 'filial'
        verbose_name = 'Филиал'
        verbose_name_plural = "Филиалы"

    def __str__(self):
        return f"{self.address}"



class Question(models.Model):
    filial = models.ForeignKey(Filial, on_delete = models.CASCADE, verbose_name="Филиал")
    content_text = models.CharField(max_length=250, verbose_name="Содержание")

    class Meta:
        db_table = 'question'
        verbose_name = 'Вопрос'
        verbose_name_plural = "Вопросы"



class Review(models.Model):
    RATES_LIST = [
        (0, 'Очень плохо'),
        (1, 'Плохо'),
        (2, 'Неплохо'),
        (3, 'Средне'),
        (4, 'Хорошо'),
        (5, 'Отлично')]

    STATUS_LIST = [
        (0, 'Не прочитано'),
        (1, 'Прочитано'),
        (2, 'С ответом'),
    ]

    REPLY_STATUS_LIST = [
        (0, 'Нельзя отвечать'),
        (1, 'Можно отвечать'),
    ]

    filial = models.ForeignKey(Filial, on_delete = models.CASCADE, verbose_name="Филиал", editable=False)

    # Данные отзыва, подгруженные с сервисов
    id_platform_review = models.CharField(max_length=200, default="", verbose_name="Id отзыва на платформе")
    status = models.IntegerField(choices=STATUS_LIST, default=0)
    rating = models.IntegerField(choices=RATES_LIST, default=False, verbose_name="Рейтинг")
    content = models.TextField(max_length=5000, verbose_name="Содержание")
    time = models.DateTimeField()
    author_name = models.CharField(max_length=350, verbose_name="Имя рецензента")
    author_url = models.CharField(max_length=1000, verbose_name="Ссылка на рецензента")
    profile_photo_url = models.CharField(max_length=1000, verbose_name="Ссылка на фото профиля")
    relative_time_description = models.CharField(max_length=300, verbose_name="Пояснение по времени")
    answerable = models.IntegerField(choices=REPLY_STATUS_LIST, default=1)

    class Meta:
        db_table = 'review'
        verbose_name = 'Отзыв'
        verbose_name_plural = "Отзывы"



class Answer(models.Model):
    review = models.ForeignKey(Review, on_delete = models.CASCADE, verbose_name="Отзыв", editable=False)
    content = models.TextField(max_length=500, verbose_name="Содержание")

    class Meta:
        db_table = 'answer_review'
        verbose_name = 'Ответ на отзыв'
        verbose_name_plural = "Ответы на отзывы"
