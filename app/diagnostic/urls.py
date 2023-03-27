from django.urls import path
from . import views

urlpatterns = [
    # path('diagnostic/start', views.start),
    path('diagnostic/get', views.get_diagnostic),
    path('diagnostic/save_progress', views.save_progress),
    path('admin/diagnostic/load_recomendations', views.load_recomendations),
    path('diagnostic/results', views.get_results),
    path('diagnostic/get_questions', views.get_questions)
]
