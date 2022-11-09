from django.apps import AppConfig
from django_cleanup.signals import cleanup_pre_delete
# from . import Additional


class DashboardConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Dashboard'

    # def ready(self):
    #     def qr_code_pre_delete(**kwargs):
    #         if kwargs['file'].name == "filial/logotype/nophoto.png":
    #             raise Exception('nophotoFileExc')

    #     cleanup_pre_delete.connect(qr_code_pre_delete)
