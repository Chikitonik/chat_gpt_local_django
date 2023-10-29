from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.user_auth_login, name='login'),
    path('logout/', views.custom_logout, name='logout'),
    path('personal_page/', views.personal_page, name='personal_page')

]
