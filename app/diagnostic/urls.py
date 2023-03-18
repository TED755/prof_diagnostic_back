from django.urls import path
from . import views

urlpatterns = [
    # path('diagnostic/start', views.start),
    path('diagnostic/get', views.get_diagnostic),
    path('diagnostic/save_progress', views.save_progress)

]
