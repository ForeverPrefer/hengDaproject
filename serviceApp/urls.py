from django.urls import path
from . import views

app_name = 'serviceApp'

urlpatterns = [
     path('download/', views.download, name='download'),
    path('getDoc/<int:id>/', views.getDoc, name='getDoc'),
    path('platform/', views.platform, name = 'platform'),
    path('facedetect/', views.facedetect, name='facedetect'),  # 人脸检测api
    path('facedetectDemo/', views.facedetectDemo, name='facedetectDemo'),
]
