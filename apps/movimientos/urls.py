from django.urls import path
from .views.ingresos.views import ListadoIngresos, DetalleIngresoView, RegistrarIngreso, BuscarProductosView
from .views.solicitudes_online.views import MisSolicitudesMedOnline, DetalleMiSolicitudOnline, RegistrarMiSolicitud, RegistrarBeneficiado
from .views.solicitudes.views import SolicitudesMed, EditarSolicitud
from .views.mantenimiento.views import ListadoTipoMovi, ActualizarTipoMovi, RegistrarTipoMovi

urlpatterns = [
    # INGRESOS
    path('listado-de-ingresos/', ListadoIngresos.as_view(), name='listado_ingresos'),
    path('detalle-de-ingreso/<int:pk>/', DetalleIngresoView.as_view(), name='detalle_ingreso'),
    path('registrar-ingreso/', RegistrarIngreso.as_view(), name='registrar_ingreso'),
    path('buscar-productos/', BuscarProductosView.as_view(), name='buscar_productos'),

    # MIS SOLICITUDES
    path('mis-solictudes-de-medicamentos/', MisSolicitudesMedOnline.as_view(), name='mis_solicitudes_medicamentos'),
    path('mi-solictud-de-medicamento/<int:pk>/', DetalleMiSolicitudOnline.as_view(), name='mi_solicitud_medicamento'),

    path('listado-de-tipos-movimientos/', ListadoTipoMovi.as_view(), name='listado_tipo_movi'),
    path('agregar-tipos-movimientos/', RegistrarTipoMovi.as_view(), name='nuevo_tipo_movi'),
    path('editar-tipos-movimientos/', ActualizarTipoMovi.as_view(), name='edit_tipo_movi'),

    path('registrar-mi-solicitud/', RegistrarMiSolicitud.as_view(), name='registrar_mi_solicitud'),
    path('registrar-beneficiado-modal/', RegistrarBeneficiado.as_view(), name='registrar_beneficiado_modal'),

    # SOLICITUDES
    path('solictudes-de-medicamentos/', SolicitudesMed.as_view(), name='listado_solicitudes_medicamentos'),
    path('modificar-solicitud-de-medicamentos/<int:pk>/', EditarSolicitud.as_view(), name='modificar_solicitudes_medicamentos'),

]
