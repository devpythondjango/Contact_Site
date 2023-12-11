from django.urls import path
from .views import views, appli_views, applications, status

urlpatterns = [
    path('', views.dashboard, name="dashboard"),

    path('profile/', views.ProfileView.as_view(), name="profile"),

    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('tablitsa/', applications.tablitsa, name="tablitsa"),
    path('export_to_excel/', applications.export_to_excel, name='export_to_excel'),

    path('application/<int:pk>/view/', appli_views.ariza_view, name='application_view'),
    path('application/<int:pk>/edit/', appli_views.ariza_edit, name='application_edit'),
    path('export_to_excel/<int:pk>', appli_views.export_to_excel_id, name='export_to_excel_id'),

    path('tablitsa/yangi/', status.status_yangi, name="status_yangi"),
    path('yangi/export_to_excel_status1/', status.export_to_excel_status1, name='export_to_excel_status1'),

    path('tablitsa/tekshirilmoqda/', status.status_tekshirilmoqda, name="status_tekshirilmoqda"),
    path('yangi/export_to_excel_status2/', status.export_to_excel_status2, name='export_to_excel_status2'),

    path('tablitsa/tekshirildi/', status.status_tekshirildi, name="status_tekshirildi"),
    path('yangi/export_to_excel_status3/', status.export_to_excel_status3, name='export_to_excel_status3'),

    path('tablitsa/rad_etildi/', status.status_rad_etildi, name="status_rad_etildi"),
    path('yangi/export_to_excel_status4/', status.export_to_excel_status4, name='export_to_excel_status4'),

    path('tablitsa/malumot_topilmadi/', status.status_malumot_topilmadi, name="status_malumot_topilmadi"),
    path('yangi/export_to_excel_status5/', status.export_to_excel_status5, name='export_to_excel_status5'),
]