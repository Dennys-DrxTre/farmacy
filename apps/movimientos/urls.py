from django.urls import path
from .views.ingresos.views import ListadoIngresos, DetalleIngresoView, RegistrarIngreso, BuscarProductosView, BuscarProductosIngresoView
from .views.solicitudes_online.views import MisSolicitudesMedOnline, DetalleMiSolicitudOnline, RegistrarMiSolicitud, RegistrarBeneficiado
from .views.solicitudes.views import (
    SolicitudesMed, 
    EditarSolicitud, 
    MedicamentoEntregado, 
    DetalleSolicitudMed, 
    RegistrarSolicitudPresencial, 
    RegistrarBeneficiadoFisico, 
    RegistrarPerfilFisico, 
    MedicamentoEnEsperaEntrega,
    VerificarDatosSolicitudMed,
    RechazarSolicitudMedicamento
)
from .views.mantenimiento.views import ListadoTipoMovi, ActualizarTipoMovi, RegistrarTipoMovi
from .views.jornadas.views import MisSolicitudesJornadas

urlpatterns = [
    # INGRESOS
    path('listado-de-ingresos/', ListadoIngresos.as_view(), name='listado_ingresos'),
    path('detalle-de-ingreso/<int:pk>/', DetalleIngresoView.as_view(), name='detalle_ingreso'),
    path('registrar-ingreso/', RegistrarIngreso.as_view(), name='registrar_ingreso'),
    path('buscar-productos/', BuscarProductosView.as_view(), name='buscar_productos'),
    path('buscar-productos-ingresos/', BuscarProductosIngresoView.as_view(), name='buscar_productos_ingresos'),
    # MIS SOLICITUDES
    path('mis-solictudes-de-medicamentos/', MisSolicitudesMedOnline.as_view(), name='mis_solicitudes_medicamentos'),
    path('mi-solictud-de-medicamento/<int:pk>/', DetalleMiSolicitudOnline.as_view(), name='mi_solicitud_medicamento'),
    path('registrar-mi-solicitud/', RegistrarMiSolicitud.as_view(), name='registrar_mi_solicitud'),
    path('registrar-beneficiado-modal/', RegistrarBeneficiado.as_view(), name='registrar_beneficiado_modal'),

    # SOLICITUDES
    path('solictudes-de-medicamentos/', SolicitudesMed.as_view(), name='listado_solicitudes_medicamentos'),
    path('registrar-solicitud/', RegistrarSolicitudPresencial.as_view(), name='registrar_solicitud_presencial'),
    path('detalle-de-solicitud-de-medicamento/<int:pk>/', DetalleSolicitudMed.as_view(), name='detalle_solicitud_med'),
    path('modificar-solicitud-de-medicamentos/<int:pk>/', EditarSolicitud.as_view(), name='modificar_solicitudes_medicamentos'),
    path('solicitud-de-medicamento-entregado/<int:pk>/', MedicamentoEntregado.as_view(), name='solicitud_de_medicamento_entregado'),
    path('solicitud-de-medicamento-en-espera-de-entrega/<int:pk>/', MedicamentoEnEsperaEntrega.as_view(), name='solicitud_de_medicamento_en_espera_entrega'),
    path('solicitud-de-medicamento-verificada/<int:pk>/', VerificarDatosSolicitudMed.as_view(), name='solicitud_de_medicamento_verificada'),
    path('rechazar-solicitud-de-medicamento/', RechazarSolicitudMedicamento.as_view(), name='rechazar_solicitud_medicamento'),
    path('registrar-beneficiado-fisico-modal/', RegistrarBeneficiadoFisico.as_view(), name='registrar_beneficiado_fisico_modal'),
    path('registrar-perfil-fisico-modal/', RegistrarPerfilFisico.as_view(), name='registrar_perfil_fisico_modal'),

    # TIPO MOVIMIENTOS
    path('listado-de-tipos-movimientos/', ListadoTipoMovi.as_view(), name='listado_tipo_movi'),
    path('agregar-tipos-movimientos/', RegistrarTipoMovi.as_view(), name='nuevo_tipo_movi'),
    path('editar-tipos-movimientos/', ActualizarTipoMovi.as_view(), name='edit_tipo_movi'),

    # JORNADAS
    path('mis-solicitudes-de-jornadas/', MisSolicitudesJornadas.as_view(), name='mi_listado_jornadas'),
]
