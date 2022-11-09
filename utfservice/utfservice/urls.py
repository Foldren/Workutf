"""utfservice URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import routers
from Profile.views import ProfileViewSet
from Main.views import MainViewSet
from Filials.views import FilialsViewSet
from Dashboard.views import DashboardViewSet
from Reviews.views import ReviewsViewSet

router = routers.SimpleRouter(trailing_slash=False)
router.register('', MainViewSet, 'main')
router.register('profile', ProfileViewSet, 'profile')
router.register('filials', FilialsViewSet, 'filials')
router.register(r'dashboard/(?P<idFilial>[0-9]+)', DashboardViewSet, 'dashboard')
router.register('reviews', ReviewsViewSet, 'reviews')

urlpatterns = [
    path('', include((router.urls, 'Rectop'))),
    path('admin/', admin.site.urls), #админка
    re_path(r'^social/', include('social_django.urls', namespace='social')), #Для авторизации через соц. сети
    path('accounts/', include('allauth.urls')), # +1
]
