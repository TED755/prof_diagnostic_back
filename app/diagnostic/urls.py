from django.urls import path
from . import views

urlpatterns = [
    path('get', views.get_diagnostic),
    path('save_progress', views.save_progress),
    path('results', views.get_results),
    path('get_questions', views.get_questions),
    path('get_progress', views.get_progress),
]
