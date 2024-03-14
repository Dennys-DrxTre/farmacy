from django.db import models
from django.forms import model_to_dict

from apps.entidades.models import Paciente, Empleado
from apps.inventario.models import Producto, Inventario

# Create your models here.
# solicitud de producto
class Solicitud(models.Model):
	
	class Status(models.TextChoices):
		EN_PROCRESO = 'EP', 'En Proceso'
		APROBADO = 'AP', 'Aprobado'
		EN_ESPERA_DE_ENTREGA = 'EE', 'En Espera de Entrega'
		ENTREGADO = 'ET', 'Entregado'

	fecha_soli = models.DateField(auto_now=True, blank=False, null=False)
	cod_pac = models.ForeignKey(Paciente, verbose_name='Paciente', on_delete=models.PROTECT, blank=False, null=False)
	descripcion_soli = models.TextField(blank=False, null=False)
	recipe = models.FileField(upload_to='recipes/', blank=False, null=False)
	proceso_actual = models.CharField(max_length=50, default='ATENCION AL CLIENTE')
	estado = models.CharField(max_length=2, choices=Status.choices, default=Status.EN_PROCRESO, blank=False, null=False)
	validado_almacenista = models.BooleanField(default=False)
	validado_admin = models.BooleanField(default=False)

	class Meta:
		verbose_name = 'Solicitud de Medicamento'
		verbose_name_plural = 'Solicitud de Medicamentos'
		ordering = ['fecha_soli']

	def __str__(self):
		return f'{self.descripcion_soli}'

	def toJSON(self):
		item = model_to_dict(self)
		return item

# detalle de la solicitud
class DetalleSolicitud(models.Model):
	solicitud = models.ForeignKey(Solicitud, on_delete=models.CASCADE)
	producto = models.ForeignKey(Inventario, on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=1)

	class Meta:
		unique_together = ('solicitud', 'producto')  # Asegurar que no haya duplicados

	def __str__(self):
		return f'{self.solicitud.id_soli} - {self.producto.nombre} - {self.cantidad}'

	def toJSON(self):
		item = model_to_dict(self)
		return item

# tipo de movimiento
class Tipo_mov(models.Model):
	nombre = models.CharField(max_length=50)

	class Meta:
		verbose_name = 'Tipo de Movimiento'
		verbose_name_plural = 'Tipos de Movimientos'
		ordering = ['nombre']

	def __str__(self):
		return f'{self.nombre}'

	def toJSON(self):
		item = model_to_dict(self)
		return item

# movimiento del inventario
# class Movimiento_inventario(models.Model):
# 	fecha_mov = models.DateField(auto_now=True, blank=False, null=False)
# 	motivo_mov = models.TextField(blank=False, null=False)
# 	tipo_mov = models.ForeignKey(Tipo_mov, verbose_name='Tipo de Movimiento', on_delete=models.PROTECT, blank=False, null=False)
# 	cod_empl = models.ForeignKey(Empleado, verbose_name='Empleado', on_delete=models.PROTECT, blank=False, null=False)
# 	id_producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.PROTECT, blank=False, null=False)
# 	cantidad = models.IntegerField(blank=False, null=False)

# 	class Meta:
# 		verbose_name = 'Movimiento de Inventario'
# 		verbose_name_plural = 'Movimientos de Inventario'
# 		ordering = ['fecha_mov']

# 	def __str__(self):
# 		return f'{self.fecha_mov} {self.tipo_mov}'

# 	def save(self, *args, **kwargs):
# 		self.motivo_mov = (self.motivo_mov).upper()
# 		return super(Movimiento_inventario, self).save(*args, **kwargs)