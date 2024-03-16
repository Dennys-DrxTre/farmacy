from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from apps.entidades.models import Perfil, Persona, User, Beneficiado, Zona
from .forms import PerfilForm
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

class Inicio(TemplateView):
	template_name = 'pages/dashboard/inicio.html'

class landing(TemplateView):
	template_name = 'landingPage/landing.html'

class RegistrarPerfil(TemplateView):
	template_name = 'pages/entidades/registrar_perfil.html'

	def post(self, request, *args, **kwargs):

		# Aquí puedes agregar lógica personalizada antes de guardar el objeto
		# Por ejemplo, crear un usuario relacionado
		usuario = User()
		usuario.username = f'{request.POST["nacionalidad"]}{request.POST["cedula"]}'
		usuario.email = request.POST["email"]
		usuario.set_password(request.POST["password"])
		usuario.is_active = True
		usuario.save()

		perfil = Perfil()
		perfil.nacionalidad = request.POST["nacionalidad"]
		perfil.cedula = request.POST["cedula"]
		perfil.nombres = request.POST["nombres"]
		perfil.apellidos = request.POST["apellidos"]
		perfil.telefono = request.POST["telefono"]
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

		# Aquí puedes agregar lógica personalizada después de guardar el objeto
		# Por ejemplo, enviar un mensaje de éxito
		messages.success(request, 'El Usuario se ha registrado correctamente')

		# Redirige al usuario a la URL de éxito
		return redirect(reverse_lazy('vista'))
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['zona'] = Zona.objects.all()
		return context
		