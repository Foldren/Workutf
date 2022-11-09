from django.contrib import admin
from .models import Filial, AddonUserInfo, Question, Review, PlatformAccount


admin.site.register(PlatformAccount)
admin.site.register(Review)
admin.site.register(Filial)
admin.site.register(AddonUserInfo)
admin.site.register(Question)