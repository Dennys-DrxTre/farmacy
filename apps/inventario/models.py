from django.db import models
from django.forms import model_to_dict

# ubicacion del producto
class Almacen(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Ubicación'
		verbose_name_plural = 'Ubicaciones'

	def __str__(self):
		return f'{self.nombre}'
	
# tipo de insumo
class TipoInsumo(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Tipo de insumo'
		verbose_name_plural = 'Tipo de insumos'

	def __str__(self):
		return self.nombre

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# laboratorio
class Laboratorio(models.Model):
	nombre = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Laboratorio'
		verbose_name_plural = 'Laboratorios'

	def __str__(self):
		return self.nombre

	def toJSON(self):
		item = model_to_dict(self)
		return item
	
# productos
class Producto(models.Model):
	nombre_producto = models.CharField(max_length=50, blank=False, null=False)
	almacen = models.ForeignKey(Almacen, verbose_name='Ubicación', on_delete=models.PROTECT, blank=False, null=False)
	tipo_insumo = models.ForeignKey(TipoInsumo, verbose_name='Tipo de insumo', on_delete=models.PROTECT, blank=False, null=False)
	laboratorio = models.ForeignKey(Laboratorio, verbose_name='Laboratorio', on_delete=models.PROTECT, blank=False, null=False)
	if_expire_date = models.BooleanField(default=True, verbose_name='Si caduca')
	stock_minimo = models.IntegerField(blank=False, null=False)
	total_stock = models.IntegerField(null = False, blank= False)

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['nombre_producto']

	def __str__(self):
		return f'{self.nombre_producto}'

	def toJSON(self):
		item = model_to_dict(self)
		return item

class Inventario(models.Model):
	lote = models.CharField(max_length=50,verbose_name='Codigo de lote')
	expiry_date = models.DateField(auto_now=False, auto_now_add=False, verbose_name='Fecha de vencimiento')
	stock = models.IntegerField(default=0, verbose_name='Stock')
	product = models.ForeignKey(Producto, on_delete=models.CASCADE, related_name='inventorario', verbose_name='Producto')

	class Meta:
		verbose_name = 'Inventario'
		verbose_name_plural = 'Inventarios'
		# permissions = [
		# 	("can_view_student", "Can view student"),
		# ]

	def __str__(self):
		return "{} - {}".format(self.product.name, self.stock)

	def toJSON(self):
		item = model_to_dict(self)
		return item

# lote del producto
# class Lote(models.Model):
# 	lote = models.CharField(max_length=60, blank=False, null=False)
# 	canti_pro = models.IntegerField(blank=False, null=False)
# 	fecha_lote = models.DateField(auto_now=True, blank=False, null=False)

# 	class Meta:
# 		verbose_name = 'Lote'
# 		verbose_name_plural = 'Lotes'
# 		ordering = ['lote']

# 	def __str__(self):
# 		return self.lote
