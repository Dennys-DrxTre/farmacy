from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from apps.entidades.models import Perfil, Persona, User, Beneficiado, Zona, LandingPage
from django.contrib.auth.models import Permission
from .forms import PerfilForm, ZonaForm, FormLanding
from .permisos import permisos_usuarios
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db import IntegrityError
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .mixins import ValidarUsuario


from .models import Perfil
from apps.inventario.models import Producto
from apps.movimientos.models import Solicitud, Jornada
# Create your views here.

class Inicio(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_inicio'
	template_name = 'pages/dashboard/inicio.html'

	def get(self, request, *args, **kwargs):
		context = {}
		cantidad_usuarios = Perfil.objects.all().count()
		cantidad_productos = Producto.objects.all().count()
		cantidad_solicitudes = Solicitud.objects.all().count()
		cantidad_jornadas = Jornada.objects.all().count()

		mis_solicitudes_de_medicamentos = Solicitud.objects.filter(perfil_id=request.user.perfil.pk).order_by('-pk')[:20]
		mis_solicitudes_de_jornadas_de_medicamentos = Jornada.objects.filter(jefe_comunidad_id=request.user.perfil.pk).order_by('-pk')[:20]


		context['cantidad_usuarios'] = cantidad_usuarios
		context['cantidad_productos'] = cantidad_productos
		context['cantidad_solicitudes'] = cantidad_solicitudes
		context['cantidad_jornadas'] = cantidad_jornadas
		context['mis_solicitudes_de_medicamentos'] = mis_solicitudes_de_medicamentos
		context['mis_solicitudes_de_jornadas_de_medicamentos'] = mis_solicitudes_de_jornadas_de_medicamentos

		return render(request, self.template_name, context)

class landing(TemplateView):
	template_name = 'landingPage/landing.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['landing'] = LandingPage().get_config()
		return context

class ActualizarLanding(ValidarUsuario, TemplateView):
	permission_required = 'entidades.change_imagen'
	template_name = 'landingPage/edit_landing.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		action = request.POST['action']

		# Obtener la configuración de la página de inicio
		conf = LandingPage.get_config()

		if action == 'edit_landing':
			# Lista de nombres de campos para imágenes y texto
			campos = ['imagen1', 'imagen2', 'imagen3', 'imagen4', 'imagen5', 'texto1']

			# Iterar sobre los campos y actualizar el objeto conf si el campo está presente en request.FILES o request.POST
			for campo in campos:
				if campo.startswith('imagen'):
					if request.FILES.get(campo):
						setattr(conf, campo, request.FILES.get(campo))
				elif campo.startswith('texto'):
					if request.POST.get(campo):
						setattr(conf, campo, request.POST.get(campo))

			# Guardar el objeto actualizado
			conf.save()
			
			messages.add_message(request, messages.SUCCESS, 'La configuración de la página de inicio ha sido actualizada exitosamente.')
			return redirect(reverse_lazy('edit_landing'))

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = FormLanding(instance=LandingPage.get_config())
		return context
		

class ListadoPerfiles(ListView):
	model = Perfil
	template_name = 'pages/entidades/listado_usuarios.html'
	context_object_name = 'perfiles'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['sub_title'] = 'Lista de Usuarios'
		context['form'] = PerfilForm()
		return context

from django.contrib.auth.models import User, Permission
from django.http import JsonResponse
from django.views import View

class RegistrarPerfil(View):
	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		
		if action == 'nuevo_usuario':
			username = f'{request.POST["nacionalidad"]}{request.POST["cedula"]}'
			if not User.objects.filter(username=username).exists() and not Perfil.objects.filter(cedula = request.POST["cedula"]):
				usuario = User()
				usuario.username = username
				usuario.first_name = request.POST["nombres"]
				usuario.last_name = request.POST["apellidos"]
				usuario.email = request.POST["email"]
				usuario.is_active = request.POST.get('is_active', False)
				usuario.set_password(request.POST["password1"])
				usuario.save()

				permissions = Permission.objects.filter(codename__in=permisos_usuarios[request.POST["rol"]])
				usuario.user_permissions.set(permissions)
				usuario.save()

				
				perfil = Perfil.objects.create(
					nacionalidad=request.POST["nacionalidad"],
					cedula=request.POST["cedula"],
					nombres=request.POST["nombres"],
					apellidos=request.POST["apellidos"],
					telefono=f'{request.POST["codigo_tlf"]}{request.POST["telefono"]}',
					genero=request.POST["genero"],
					embarazada=request.POST["genero"] == 'MA' or request.POST["embarazada"],
					f_nacimiento=request.POST["f_nacimiento"],
					c_residencia=request.FILES.get("c_residencia"),
					zona=Zona.objects.get(id=request.POST["zona"]),
					direccion=request.POST["direccion"],
					rol=request.POST["rol"],
					usuario=usuario
				)

				if not Beneficiado.objects.filter(cedula=request.POST["cedula"]).exists():
					Beneficiado.objects.create(
						perfil=perfil,
						nacionalidad=request.POST["nacionalidad"],
						cedula=request.POST["cedula"],
						nombres=request.POST["nombres"],
						apellidos=request.POST["apellidos"],
						telefono=request.POST["telefono"],
						genero=request.POST["genero"],
						embarazada=request.POST["genero"] == 'MA' or request.POST["embarazada"],
						f_nacimiento=request.POST["f_nacimiento"],
						c_residencia=request.FILES.get("c_residencia"),
						zona=Zona.objects.get(id=request.POST["zona"]),
						direccion=request.POST["direccion"]
					)
				
				else:
					data['response'] = {'title': 'Ocurrió un error!', 'data': 'Beneficiado ya existe.', 'type_response': 'danger'}
				
				data['response'] = {'title': 'Exito!', 'data': 'Usuario creado correctamente.', 'type_response': 'success'}

			else:
				data['response'] = {'title': 'Ocurrió un error!', 'data': 'Usuario ya esta registrado.', 'type_response': 'danger'}
		else:
			data['response'] = {'title': 'Ocurrió un error!', 'data': 'Error de solicitud.', 'type_response': 'danger'}
				
		
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['form'] = PerfilForm()
		return context



# control de acceso
	
class LoginPersonalidado(TemplateView):
	template_name = 'acceso/login.html'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action_login']

			if action == 'login':
				naci = request.POST['naci']
				ci = request.POST['ci']
				username = f'{naci}{ci}'
				password = request.POST['password']

				user = authenticate(request, username=username, password=password)
				if user is not None:
					login(request, user)
					data['response'] = {'title':'Exito!', 'data': 'Ingreso validado correctamente.', 'type_response': 'success'}

				else:
					if not User.objects.filter(username = username):
						data['response'] = {'title':'Ocurrió un error!', 'data': 'El usuario no existe.', 'type_response': 'danger'}
					else:
						data['response'] = {'title':'Ocurrió un error!', 'data': 'Contraseña incorrecta.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		return context

class CambiarClave(View):
	#permission_required = 'core.change_password_users'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action_password']
		try:
			
			if action == 'cambiar_clave':

				username = request.POST['username']
				password = request.POST['password_actual']

				user = authenticate(request, username=username, password=password)
				if user is not None:
					usuario = User.objects.get(username = username)
					usuario.set_password(request.POST['new_password'])
					usuario.save()
					logout(request)
					data['response'] = {'title':'Exito!', 'data': 'Contraseña actualizada correctamente.', 'type_response': 'success'}
				
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Contraseña actual incorrecta.', 'type_response': 'danger'}
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'Solicitud invalida.', 'type_response': 'danger'}
					
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

class Logout(View):
	def get(self, request):
		logout(request)
		return redirect('/')

class ListaZona(TemplateView):
	template_name = "pages/mantenimiento/listado_zonas.html"

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'search_zonas':
				data = []
				for i in Zona.objects.all():
					item = i.toJSON()
					data.append(item)
				# Convertir la lista de datos en un JsonResponse
				return JsonResponse(data, safe=False)
				
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de zonas"
		return context

class RegistrarZona(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nueva_zona':
				form = ZonaForm(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Zona registrada correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ActualizarZona(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		action = request.POST['action']
		try:
			if action == 'edit_zona':
				zona = Zona.objects.filter(id = request.POST['id']).first()
				form = ZonaForm(request.POST, instance=zona)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'La zona se ha actualizado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}
			
		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)	