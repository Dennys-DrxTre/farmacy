from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from apps.entidades.models import Perfil, Persona, User, Beneficiado, Zona
from django.contrib.auth.models import Permission
from .forms import PerfilForm
from .permisos import permisos_usuarios
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class Inicio(TemplateView):
	template_name = 'pages/dashboard/inicio.html'

class landing(TemplateView):
	template_name = 'landingPage/landing.html'

class ListadoPerfiles(ListView):
	model = Perfil
	template_name = 'pages/entidades/listado_usuarios.html'
	context_object_name = 'perfiles'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sub_title'] = 'Lista de Usuarios'
		return context
	
class RegistrarPerfil(SuccessMessageMixin, TemplateView):
	template_name = 'pages/entidades/registrar_perfil.html'
	success_message = 'El Usuario se ha registrado correctamente'

	def post(self, request, *args, **kwargs):

		usuario = User()
		usuario.username = f'{request.POST["nacionalidad"]}{request.POST["cedula"]}'
		usuario.email = request.POST["email"]
		usuario.set_password(request.POST["password"])
		usuario.is_active = request.POST.get('is_active', False)
		usuario.save()

		permissions = Permission.objects.filter(codename__in=permisos_usuarios[request.POST["rol"]])
		for permission in permissions:
			usuario.user_permissions.add(permission)
		usuario.save()

		perfil = Perfil()
		perfil.nacionalidad = request.POST["nacionalidad"]
		perfil.cedula = request.POST["cedula"]
		perfil.nombres = request.POST["nombres"]
		perfil.apellidos = request.POST["apellidos"]
		perfil.telefono = f'{request.POST["codigo_tlf"]}{request.POST["telefono"]}'
		perfil.genero = request.POST["genero"]
		perfil.f_nacimiento = request.POST["f_nacimiento"]
		perfil.embarazada = request.POST["embarazada"]
		perfil.c_residencia = request.FILES["c_residencia"]
		perfil.zona = Zona.objects.get(id = request.POST["zona"])
		perfil.direccion = request.POST["direccion"]
		perfil.rol = request.POST["rol"]
		perfil.usuario = User.objects.get(username = usuario.username)
		perfil.save()

		beneficiado = Beneficiado()
		beneficiado.perfil = Perfil.objects.get(cedula = perfil.cedula)
		beneficiado.nacionalidad = request.POST["nacionalidad"]
		beneficiado.cedula = request.POST["cedula"]
		beneficiado.nombres = request.POST["nombres"]
		beneficiado.apellidos = request.POST["apellidos"]
		beneficiado.telefono = request.POST["telefono"]
		beneficiado.genero = request.POST["genero"]
		beneficiado.f_nacimiento = request.POST["f_nacimiento"]
		beneficiado.embarazada = request.POST["embarazada"]
		beneficiado.c_residencia = request.FILES["c_residencia"]
		beneficiado.zona = Zona.objects.get(id = request.POST["zona"])
		beneficiado.direccion = request.POST["direccion"]
		beneficiado.save()

		# enviando el correo de registro

		# Cargar la plantilla HTML
		html_content = render_to_string('templates/email/email_registro.html', {'correo': request.POST['email'], 'nombres': request.POST['nombres'], 'apellidos': request.POST['apellidos']})

		# Configurar el correo electrónico
		subject, from_email, to = 'REGISTRO EXITOSO', 'FARMACIA COMUNITARIA ASIC LEONIDAS RAMOS', request.POST['email']
		text_content = 'ESTE ES UN MENSAJE DE BIENVENIDA.'

		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")

		# Enviar el correo electrónico
		msg.send()

		# Redirige al usuario a la URL de éxito
		return redirect(reverse_lazy('lista_perfiles'))
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = PerfilForm()
		return context
		

# control de acceso
	
class LoginPersonalidado(TemplateView):
	template_name = 'acceso/login.html'