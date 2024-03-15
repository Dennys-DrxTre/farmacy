from django.urls import path
from .views import Inicio, landing, RegistrarPerfil

urlpatterns = [
    path('vista/', Inicio.as_view(), name='vista'),
    path('landing/', landing.as_view()),
    path('registrar-perfil/', RegistrarPerfil.as_view()),
]
