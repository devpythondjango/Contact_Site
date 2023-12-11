from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('ariza/', views.ariza, name="ariza"),
    path('ariza/sms_code/', views.verify_sms_code, name='verify_sms_code'),
    path('captcha/', views.generate_captcha_image, name='generate_captcha'),
   
]