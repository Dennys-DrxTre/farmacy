from django.db import models

# zona
class Zona(models.Model):
	zona_residencia = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Zona'
		verbose_name_plural = 'Zonas'

	def __str__(self) -> str:
		return super().__str__()

	def save(self, *args, **kwargs):
		self.zona_residencia = (self.zona_residencia).upper()
		return super(Zona, self).save(*args, **kwargs)

# ubicacion del producto
class Ubicacion(models.Model):
	ubicacion = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Ubicación'
		verbose_name_plural = 'Ubicaciones'

	def __str__(self):
		return f'{self.ubicacion}'

	def save(self, *args, **kwargs):
		self.ubicacion = (self.ubicacion).upper()
		return super(Ubicacion, self).save(*args, **kwargs)
	
# tipo de insumo
class Tipo_insumo(models.Model):
	nombre_tipo_insumo = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Tipo de insumo'
		verbose_name_plural = 'Tipo de insumos'

	def __str__(self) -> str:
		return super().__str__()

	def save(self, *args, **kwargs):
		self.nombre_tipo_insumo = (self.nombre_tipo_insumo).upper()
		return super(Tipo_insumo, self).save(*args, **kwargs)

# lote del producto
class Lote(models.Model):
	lote = models.CharField(max_length=60, blank=False, null=False)
	canti_pro = models.IntegerField(blank=False, null=False)
	fecha_lote = models.DateField(auto_now=True, blank=False, null=False)

	class Meta:
		verbose_name = 'Lote'
		verbose_name_plural = 'Lotes'
		ordering = ['lote']

	def __str__(self) -> str:
		return super().__str__()

	def save(self, *args, **kwargs):
		self.lote = (self.lote).upper()
		return super(Lote, self).save(*args, **kwargs)
	
# laboratorio
class Laboratorio(models.Model):
	nombre_laboratorio = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Laboratorio'
		verbose_name_plural = 'Laboratorios'

	def __str__(self) -> str:
		return super().__str__()

	def save(self, *args, **kwargs):
		self.nombre_laboratorio = (self.nombre_laboratorio).upper()
		return super(Laboratorio, self).save(*args, **kwargs)
	
# representante (de la comunidad?)
class Representante(models.Model):
	nacio_repr = models.CharField(max_length=2, blank=False, null=False)
	cedula_repr = models.CharField(max_length=8, blank=False, null=False)
	nombre_repr = models.CharField( max_length=50, blank=False, null=False)
	apellido_repr = models.CharField(max_length=50, blank=False, null=False)
	parentesco = models.CharField(max_length=50, blank=False, null=False)

	class Meta:
		verbose_name = 'Representante'
		verbose_name_plural = 'Representantes'
		ordering = ['cedula_repr']

	def __str__(self):
		return f'{self.cedula_repr}'

	def save(self, *args, **kwargs):
		self.nombre_repr = (self.nombre_repr).upper()
		self.apellido_repr = (self.apellido_repr).upper()
		return super(Representante, self).save(*args, **kwargs)
	
# paciente
class Paciente(models.Model):
	
	nacio_pac = models.CharField(max_length=2, blank=False, null=False)
	cedula_pac = models.CharField(max_length=8, blank=False, null=False)
	nombre_pac = models.CharField(max_length=50, blank=False, null=False)
	apellido_pac = models.CharField(max_length=50, blank=False, null=False)
	telefono_pac = models.CharField(max_length=11, blank=False, null=False)
	email_pac = models.EmailField(unique=True, max_length=100, blank=False, null=False)
	cargo_pac = models.CharField(max_length=30, blank=False, null=False)
	id_zona = models.ForeignKey(Zona, verbose_name='Zona', on_delete=models.PROTECT, blank=False, null=False)
	sexo_pac = models.CharField(max_length=10, blank=False, null=False)
	fecha_nacimiento_pac = models.DateField(auto_now=False, blank=False, null=False)
	embarazada = models.CharField(max_length=2, blank=True, null=True)
	cod_repr = models.ForeignKey(Representante, verbose_name='Representante', on_delete=models.PROTECT, blank=True, null=True)
	constancia_residencia = models.FileField(upload_to='constancias_residencia/', max_length=200, blank=False, null=False)
	
	class Meta:
		verbose_name = 'Paciente'
		verbose_name_plural = 'Pacientes'
		ordering = ['cedula_pac']

	def __str__(self):
		return f'{self.nombre_pac} {self.apellido_pac}'

	def save(self, *args, **kwargs):
		self.nombre_pac = (self.nombre_pac).upper()
		self.apellido_pac = (self.apellido_pac).upper()
		return super(Paciente, self).save(*args, **kwargs)

# productos
class Producto(models.Model):
	nombre_producto = models.CharField(max_length=50, blank=False, null=False)
	id_ubicacion = models.ForeignKey(Ubicacion, verbose_name='Ubicación', on_delete=models.PROTECT, blank=False, null=False)
	id_tipo_insumo = models.ForeignKey(Tipo_insumo, verbose_name='Tipo de insumo', on_delete=models.PROTECT, blank=False, null=False)
	id_lote = models.ForeignKey(Lote, verbose_name='Lote', on_delete=models.PROTECT, blank=False, null=False)
	id_laboratorio = models.ForeignKey(Laboratorio, verbose_name='Laboratorio', on_delete=models.PROTECT, blank=False, null=False)
	limite = models.IntegerField(blank=False, null=False)
	stock_prod = models.IntegerField(null = False, blank= False)

	class Meta:
		verbose_name = 'Producto'
		verbose_name_plural = 'Productos'
		ordering = ['nombre_producto']

	def __str__(self):
		return f'{self.nombre_producto}'

	def save(self, *args, **kwargs):
		self.nombre_producto = (self.nombre_producto).upper()
		return super(Producto, self).save(*args, **kwargs)
	
# solicitud de producto
class Solicitud(models.Model):
	fecha_soli = models.DateField(auto_now=True, blank=False, null=False)
	cod_pac = models.ForeignKey(Paciente, verbose_name='Paciente', on_delete=models.PROTECT, blank=False, null=False)
	descripcion_soli = models.TextField(blank=False, null=False)
	id_producto = models.ManyToManyField(Producto, verbose_name='Producto')
	recipe = models.FileField(upload_to='recipes/', blank=False, null=False)
	proceso_actual = models.CharField(max_length=50, default='ATENCION AL CLIENTE')
	estado = models.CharField(max_length=50, default='EN PROCESO', blank=False, null=False)
	aceptaciones = models.PositiveIntegerField(default=0)

	class Meta:
		verbose_name = 'Solicitud de Medicamento'
		verbose_name_plural = 'Solicitud de Medicamentos'
		ordering = ['fecha_soli']

	def __str__(self):
		return f'{self.descripcion_soli}'

	def save(self, *args, **kwargs):
		self.descripcion_soli = (self.descripcion_soli).upper()
		return super(Solicitud, self).save(*args, **kwargs)

# detalle de la solicitud
class DetalleSolicitud(models.Model):
	solicitud = models.ForeignKey('Solicitud', on_delete=models.CASCADE)
	producto = models.ForeignKey('Producto', on_delete=models.CASCADE)
	cantidad = models.IntegerField(default=1)

	class Meta:
		unique_together = ('solicitud', 'producto')  # Asegurar que no haya duplicados

	def __str__(self):
		return f'{self.solicitud.id_soli} - {self.producto.nombre} - {self.cantidad}'

# empleados
class Empleado(models.Model):
	nacio_empl = models.CharField(max_length=2, blank=False, null=False)
	cedula_empl = models.CharField(max_length=8, blank=False, null=False)
	nombre_empl = models.CharField(max_length=50, blank=False, null=False)
	apellido_empl = models.CharField(max_length=50, blank=False, null=False)
	telefono_empl = models.CharField(max_length=11, blank=False, null=False)
	direccion_exacta = models.TextField(blank=False, null=False)
	cargo = models.CharField(max_length=30, blank=False, null=False)
	
	class Meta:
		verbose_name = 'Empleado'
		verbose_name_plural = 'Empleados'
		ordering = ['cedula_empl']

	def __str__(self):
		return f'{self.nombre_empl} {self.apellido_empl}'

	def save(self, *args, **kwargs):
		self.nombre_empl = (self.nombre_empl).upper()
		self.apellido_empl = (self.apellido_empl).upper()
		return super(Empleado, self).save(*args, **kwargs)
	
# tipo de movimiento
class Tipo_mov(models.Model):
	descripcion = models.TextField(blank=False, null=False)

	class Meta:
		verbose_name = 'Tipo de Movimiento'
		verbose_name_plural = 'Tipos de Movimientos'
		ordering = ['descripcion']

	def __str__(self):
		return f'{self.descripcion}'

	def save(self, *args, **kwargs):
		self.descripcion = (self.descripcion).upper()
		return super(Tipo_mov, self).save(*args, **kwargs)

# movimiento del inventario
class Movimiento_inventario(models.Model):
	fecha_mov = models.DateField(auto_now=True, blank=False, null=False)
	motivo_mov = models.TextField(blank=False, null=False)
	tipo_mov = models.ForeignKey(Tipo_mov, verbose_name='Tipo de Movimiento', on_delete=models.PROTECT, blank=False, null=False)
	cod_empl = models.ForeignKey(Empleado, verbose_name='Empleado', on_delete=models.PROTECT, blank=False, null=False)
	id_producto = models.ForeignKey(Producto, verbose_name='Producto', on_delete=models.PROTECT, blank=False, null=False)
	cantidad = models.IntegerField(blank=False, null=False)

	class Meta:
		verbose_name = 'Movimiento de Inventario'
		verbose_name_plural = 'Movimientos de Inventario'
		ordering = ['fecha_mov']

	def __str__(self):
		return f'{self.fecha_mov} {self.tipo_mov}'

	def save(self, *args, **kwargs):
		self.motivo_mov = (self.motivo_mov).upper()
		return super(Movimiento_inventario, self).save(*args, **kwargs)

"""
# usuario base
class UsuarioManager(BaseUserManager):
	def create_user(self, email, username, nombre, apellido, cargo, paciente, password = None):
		if not email:
			raise ValueError('El usuario debe tener un correo electrónico')

		usuario = self.model(
			username = username,
			nombre = nombre,
			apellido = apellido,
			email = self.normalize_email(email),
			cargo = cargo,
			paciente = paciente
		)

		usuario.set_password(password)
		usuario.save()
		return usuario

	def create_superuser(self, username, nombre, apellido, email, cargo, password, paciente):
		usuario = self.create_user(
			email,
			username = username,
			nombre = nombre,
			apellido = apellido,
			password = password,
			cargo = cargo,
			paciente = paciente
		)
		usuario.cargo = 'ADMINISTRADOR'
		usuario.save()
		return usuario

# usuario
class Usuario(AbstractBaseUser):
	nombre = models.CharField(max_length=16, blank=False, null=False)
	apellido = models.CharField(max_length=16, blank=False, null=False)
	email = models.EmailField(max_length=100, blank=False, null=False)
	cargo = models.CharField(max_length=30, blank=False, null=False)
	imagen = models.ImageField(upload_to='perfil/', blank=True, null=True)
	intentos_fallidos = models.IntegerField(default=0)
	cuenta_bloqueada = models.BooleanField(default=False)
	paciente = models.OneToOneField(Paciente, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return f'{self.username}'

	def save(self, *args, **kwargs):
		self.username = (self.username).upper()
		self.nombre = (self.nombre).upper()
		self.apellido = (self.apellido).upper()
		self.email = (self.email).upper()
		return super(Usuario, self).save(*args, **kwargs)

# landing page
class LandingContent(models.Model):
	imagen1 = models.ImageField(upload_to='landing_images', default='images/slide1.jpg')
	imagen2 = models.ImageField(upload_to='landing_images', default='images/slide2.jpg')
	imagen3 = models.ImageField(upload_to='landing_images', default='images/slide3.jpg')
	imagen4 = models.ImageField(upload_to='landing_images', default='images/slide4.jpg')
	imagen5 = models.ImageField(upload_to='landing_images', default='images/slide5.jpg')
	texto1 = models.TextField(default='Incluya el texto del cintillo')

"""