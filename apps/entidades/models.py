from django.db import models
from django.forms import model_to_dict

# zona
class Zona(models.Model):
	zona_residencia = models.CharField(max_length=60, blank=False, null=False)

	class Meta:
		verbose_name = 'Zona'
		verbose_name_plural = 'Zonas'

	def __str__(self):
		return self.zona_residencia

	def toJSON(self):
		item = model_to_dict(self)
		return item

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