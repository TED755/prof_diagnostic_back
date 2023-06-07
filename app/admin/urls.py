from django.urls import path
from . import views

urlpatterns = [
    path('migrate_hist', views.migrate_hist)
]
