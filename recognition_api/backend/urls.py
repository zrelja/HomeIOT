from django.conf.urls import url, include
from rest_framework import routers
from django.views.generic import TemplateView
from object_detection_api.views import object_detection_api


router = routers.DefaultRouter()

urlpatterns = [

    url(r'^object_detection_api/$', object_detection_api),

]
