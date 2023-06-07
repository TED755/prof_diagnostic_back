from django.urls import path
from . import views

urlpatterns = [
    path('register', views.register),
    path('login', views.login),
    path('refresh', views.refresh),
    path('logout', views.end_session),
    path('register/teaching_exp', views.get_teaching_exp),
    path('register/position', views.get_position),
    path('register/category', views.get_category),
    path('register/raion', views.get_raion),
    path('register/region_rf', views.get_region_rf),
    path('register/locality_type', views.get_locality_type)
]
