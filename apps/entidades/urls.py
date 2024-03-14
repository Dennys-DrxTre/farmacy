from django.urls import path
from .views import Inicio, landing

urlpatterns = [
    path('vista/', Inicio.as_view()),
    path('landing/', landing.as_view()),
]
