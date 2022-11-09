from django.apps import AppConfig
from django_cleanup.signals import cleanup_pre_delete


class ProfileConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Profile'

    def ready(self):
        def qr_code_pre_delete(**kwargs):
            if kwargs['file'].name == "filial/logotype/nophoto.png":
                raise Exception('nophotoFileExc')

        cleanup_pre_delete.connect(qr_code_pre_delete)

