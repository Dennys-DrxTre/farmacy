from django.urls import path
from .views import ListadoIngresos, DetalleIngresoView, RegistrarIngreso, BuscarProductosView

urlpatterns = [
    path('listado-de-ingresos/', ListadoIngresos.as_view(), name='listado_ingresos'),
    path('detalle-de-ingreso/<int:pk>/', DetalleIngresoView.as_view(), name='detalle_ingreso'),
    path('registrar-ingreso/', RegistrarIngreso.as_view(), name='registrar_ingreso'),
    path('buscar-productos/', BuscarProductosView.as_view(), name='buscar_productos'),

]
