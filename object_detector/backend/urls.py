from django.conf.urls import url, include
from rest_framework import routers
from django.views.generic import TemplateView
from object_detection_api.views import object_detection_api
from face_recognition_api.views import face_recognition_api

router = routers.DefaultRouter()

urlpatterns = [

    url(r'^object_detection_api/$', object_detection_api),
    url(r'^face_recognition_api/$', face_recognition_api),

]
