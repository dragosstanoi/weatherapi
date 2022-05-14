from django.urls import path

from . import views

from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('', views.api_home, name="api-home"),
    path('login/', views.api_login, name="login"),
    path('logout/', views.api_logout, name="logout"),
    path('api_login', obtain_auth_token, name="api-login"),

    path('locations/', views.api_locations, name="locations"),
    path('locations/<str:pk>', views.api_location_detail, name="location-detail"),
    path('locations/<str:lk>/parameters', views.api_location_parameters, name="location-parameters"),
    path('locations/<str:lk>/parameters/<str:pk>', views.api_location_parameters_detail, name="location-parameters-detail"),
]
