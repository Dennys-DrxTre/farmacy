from django.urls import path

from .views import ListadoProcuctos,DetalleProductoView, Laboratorio, RegistrarLab, ListadoTiposInsumos, ListadoAlmacen

urlpatterns = [
    path('listado-de-productos/', ListadoProcuctos.as_view(), name='listado_productos'),
    path('detalle-de-producto/<int:pk>/', DetalleProductoView.as_view(), name='detalle_producto'),

    # mantenimiento
    path('listado-de-laboratorios/', Laboratorio.as_view(), name='listado_lab'),
    path('registro-de-laboratorio/', RegistrarLab.as_view(), name='nuevo_lab'),

    path('listado-de-insumos/', ListadoTiposInsumos.as_view(), name='listado_insumos'),
    path('listado-de-almacenes/', ListadoAlmacen.as_view(), name='listado_almacen'),
]
