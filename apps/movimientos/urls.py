from django.urls import path
from .views import ListadoIngresos, DetalleIngreso

urlpatterns = [
    path('listado-de-ingresos/', ListadoIngresos.as_view(), name='listado_ingresos'),
    path('detalle-de-ingreso/<int:pk>/', DetalleIngreso.as_view(), name='detalle_ingreso'),

]
