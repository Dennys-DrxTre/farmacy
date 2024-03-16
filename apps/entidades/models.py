from django.db import models
from django.forms import model_to_dict
from django.contrib.auth.models import User

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

class Persona(models.Model):

	class Genero(models.TextChoices):
		MASCULINO = 'MA', 'Masculino'
		FEMENINO = 'FE', 'Femenino'

	class Nacionalidad(models.TextChoices):
		VENEZOLANO = 'V-', 'V-'
		EXTRANJERO = 'E-', 'E-'
		JURIDICO = 'J-', 'J-'

	nacionalidad = models.CharField(max_length=2, choices=Nacionalidad.choices, default=Nacionalidad.VENEZOLANO, blank=False, null=False)
	cedula = models.CharField(max_length=8, blank=False, null=False)
	nombres = models.CharField(max_length=50, blank=False, null=False)
	apellidos = models.CharField(max_length=50, blank=False, null=False)
	telefono = models.CharField(max_length=11, blank=False, null=False)
	genero = models.CharField(max_length=2, blank=False, null=False, choices=Genero.choices)
	f_nacimiento = models.DateField(auto_now_add = False, auto_now=False, blank=False, null=False)
	embarazada = models.BooleanField(blank=False, null=False)
	c_residencia = models.FileField(upload_to='constancias_residencias/', blank=True, null=True)
	zona  = models.ForeignKey(Zona, on_delete=models.PROTECT, blank=False, null=False)
	direccion = models.TextField(blank=False, null=False)
	
	class Meta:
		abstract = True

	def toJSON(self):
		item = model_to_dict(self)
		return item

class Perfil(Persona):
	class Rol(models.TextChoices):
		ADMINISTRADOR = 'AD', 'Administrador'
		ALMACENISTA = 'AL', 'Almacenista'
		AT_CLIENTE = 'AT', 'Atención al Cliente'
		JEFE_COMUNIDAD = 'JC', 'Jefe de Comunidad'
		PACIENTE = 'PA', 'Paciente'
	
	rol = models.CharField(max_length=2, choices=Rol.choices, default=Rol.PACIENTE)
	usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
	
	def __str__(self):
		return str(self.cedula)
	
	class Meta:
		verbose_name = 'perfil'
		verbose_name_plural = 'perfiles'
		permissions = [
			('cambiar_password', 'cambiar contraseña a usuarios'),
			('cambiar_estado_usuarios', 'cambiar estado de usuarios'),
			('cambiar_estado_jornada', 'cambiar estatus de jornadas'),
			('cambiar_estado_solicitudes', 'cambiar status de solicitudes')
		]

	def toJSON(self):
		item = model_to_dict(self)
		return item

class Beneficiado(Persona):
	perfil = models.ForeignKey(Perfil, on_delete=models.PROTECT, related_name='beneficiados')

	def __str__(self):
		return str(self.cedula)
		
	class Meta:
		verbose_name = 'Beneficiado'
		verbose_name_plural = 'Beneficiados'

	def toJSON(self):
		item = model_to_dict(self)
		return item
