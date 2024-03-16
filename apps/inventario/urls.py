from django.urls import path

from .views import ListadoProcuctos,DetalleProductoView

urlpatterns = [
    path('listado-de-productos/', ListadoProcuctos.as_view(), name='listado_productos'),
    path('detalle-de-producto/<int:pk>/', DetalleProductoView.as_view(), name='detalle_producto'),
]
