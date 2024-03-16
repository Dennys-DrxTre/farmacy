from django.urls import path
from .views.ingresos.views import ListadoIngresos, DetalleIngresoView, RegistrarIngreso, BuscarProductosView
from .views.solicitudes_fisicas.views import ListadoSolictudOnline, DetalleMiSolicitudOnline
urlpatterns = [
    # INGRESOS
    path('listado-de-ingresos/', ListadoIngresos.as_view(), name='listado_ingresos'),
    path('detalle-de-ingreso/<int:pk>/', DetalleIngresoView.as_view(), name='detalle_ingreso'),
    path('registrar-ingreso/', RegistrarIngreso.as_view(), name='registrar_ingreso'),
    path('buscar-productos/', BuscarProductosView.as_view(), name='buscar_productos'),

    # MIS SOLICITUDES
    path('mis-solictudes-de-medicamentos/', ListadoSolictudOnline.as_view(), name='mis_solicitudes_medicamentos'),
    path('mi-solictud-de-medicamento/<int:pk>/', DetalleMiSolicitudOnline.as_view(), name='mi_solicitud_medicamento'),
]
