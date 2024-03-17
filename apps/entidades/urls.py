from django.urls import path
from .views import Inicio, landing, RegistrarPerfil, ListadoPerfiles, LoginPersonalidado, ListaZona, RegistrarZona, ActualizarZona

urlpatterns = [
    path('vista/', Inicio.as_view(), name='vista'),
    path('landing/', landing.as_view()),
    path('registrar-perfil/', RegistrarPerfil.as_view(), name='new_perfil'),
    path('listado-de-perfiles/', ListadoPerfiles.as_view(), name='lista_perfiles'),

    # control de acceso
    path('ingresar/', LoginPersonalidado.as_view(), name='login'),

    path('listado-de-zonas/', ListaZona.as_view(), name='lista_zonas'),
    path('registro-de-zona/', RegistrarZona.as_view(), name='nueva_zona'),
    path('actualizar-zona/', ActualizarZona.as_view(), name='actualizar_zona'),
]
