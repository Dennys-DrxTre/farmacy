from django.contrib import admin
from .models import Solicitud, DetalleSolicitud, Jornada, DetalleJornada, Ingreso, DetalleIngreso, TipoMov, Historial, DetalleIventarioSolicitud, DetalleIventarioJornada
# Register your models here.

class SolicitudAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_soli', 'proceso_actual', 'estado', 'tipo_solicitud')
    list_filter = ('proceso_actual', 'estado', 'tipo_solicitud')
    search_fields = ('pk', 'proceso_actual', 'estado', 'tipo_solicitud')
    ordering = ('pk', 'fecha_soli')
    # readonly_fields = ('date_of_birth',)

class DetSolicitudAdmin(admin.ModelAdmin):
    list_display = ('pk', 'solicitud', 'producto', 'cant_solicitada', 'cant_entregada')
    list_filter = ('producto',)
    search_fields = ('pk', 'producto')
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class DetInventarioSolicitudAdmin(admin.ModelAdmin):
    list_display = ('pk', 'detsolicitud', 'inventario', 'cantidad')
    list_filter = ('inventario',)
    search_fields = ('pk', 'inventario')
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class JornadaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_solicitud', 'fecha_jornada', 'jefe_comunidad', 'proceso_actual', 'estado')
    list_filter = ('jefe_comunidad', 'proceso_actual', 'estado')
    search_fields = ('pk', 'jefe_comunidad')
    ordering = ('pk', 'fecha_solicitud', 'fecha_jornada')
    # readonly_fields = ('date_of_birth',)

class DetJornadaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'beneficiado', 'cant_solicitada', 'cant_aprobada')
    list_filter = ('beneficiado',)
    search_fields = ('pk', 'beneficiado')
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class DetInventarioJornadaAdmin(admin.ModelAdmin):
    list_display = ('pk', 'detjornada', 'inventario', 'cantidad')
    list_filter = ('inventario',)
    search_fields = ('pk', 'inventario')
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class IngresoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha', 'descripcion', 'tipo_ingreso')
    list_filter = ('tipo_ingreso',)
    search_fields = ('pk', 'tipo_ingreso')
    ordering = ('pk', 'fecha')
    # readonly_fields = ('date_of_birth',)

class DetIngresoAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ingreso', 'inventario', 'cantidad', 'lote')
    list_filter = ('inventario',)
    search_fields = ('pk',)
    ordering = ('pk',)
    # readonly_fields = ('date_of_birth',)

class TipoMoviAdmin(admin.ModelAdmin):
    list_display = ('pk', 'nombre', 'operacion')
    search_fields = ('pk', 'nombre')
    ordering = ('pk', 'nombre')
    # readonly_fields = ('date_of_birth',)

class HistorialAdmin(admin.ModelAdmin):
    list_display = ('pk', 'fecha_mov', 'tipo_mov', 'empleado', 'producto', 'cantidad')
    list_filter = ('producto',)
    search_fields = ('pk', 'producto')
    ordering = ('pk', 'fecha_mov')
    # readonly_fields = ('date_of_birth',)

admin.site.register(Solicitud, SolicitudAdmin)
admin.site.register(DetalleSolicitud, DetSolicitudAdmin)
admin.site.register(Jornada, JornadaAdmin)
admin.site.register(DetalleJornada, DetJornadaAdmin)
admin.site.register(Ingreso, IngresoAdmin)
admin.site.register(DetalleIngreso, DetIngresoAdmin)
admin.site.register(TipoMov, TipoMoviAdmin)
admin.site.register(Historial, HistorialAdmin)
admin.site.register(DetalleIventarioSolicitud, DetInventarioSolicitudAdmin)
admin.site.register(DetalleIventarioJornada, DetInventarioJornadaAdmin)
