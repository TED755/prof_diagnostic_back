from django.urls import path
from . import views

urlpatterns = [
    path('user/register', views.register),
    path('user/login', views.login),
    path('user/refresh', views.refresh),
    path('user/logout', views.end_session),
    path('user/register/teaching_exp', views.get_teaching_exp),
    path('user/register/position', views.get_position),
    path('user/register/category', views.get_category),
    path('user/register/raion', views.get_raion),
    path('user/register/region_rf', views.get_region_rf),
    path('user/register/locality_type', views.get_locality_type)
]
