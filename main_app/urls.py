from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_user_firebase/', views.register_user_firebase, name='register_user_firebase'),
    path('login_validation/', views.login_validation, name='login_validation'),
]