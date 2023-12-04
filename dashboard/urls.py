from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('tablitsa/', views.tablitsa, name="tablitsa"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
]