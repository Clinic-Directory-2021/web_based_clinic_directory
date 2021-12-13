from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='dashboard'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('register_user_firebase/', views.register_user_firebase, name='register_user_firebase'),
    path('login_validation/', views.login_validation, name='login_validation'),
    path('logout/', views.logout, name='logout'),
    path('homepage/', views.homepage, name='homepage'),
    path('settings/', views.settings, name='settings'),
    path('save_clinic_info/', views.save_clinic_info, name='save_clinic_info'),
    path('add_item/', views.add_item, name='add_item'),
    path('add_item_firebase/', views.add_item_firebase, name='add_item_firebase'),
    path('edit_item_firebase/', views.edit_item_firebase, name='edit_item_firebase'),
    path('search_item/', views.search_item, name='search_item'),
    path('getSearchData/', views.getSearchData, name='getSearchData'),
    path('search_clinic/', views.search_clinic, name='search_clinic'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('about/', views.about, name='about'),
    path('product_item_availability/', views.product_item_availability, name='product_item_availability'),

    path('addAppointment/', views.addAppointment, name='addAppointment'),
    
]