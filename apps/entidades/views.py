from django.shortcuts import render
from django.views.generic import TemplateView, ListView, View
from apps.entidades.models import Perfil, Persona, User, Beneficiado, Zona
from django.contrib.auth.models import Permission
from .forms import PerfilForm, ZonaForm
from .permisos import permisos_usuarios
from django.contrib.messages.views import SuccessMessageMixin
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
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
		if request.POST["genero"] == 'MA':
			perfil.embarazada = False
		else:
			perfil.embarazada = request.POST["embarazada"]
		perfil.f_nacimiento = request.POST["f_nacimiento"]
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
		if request.POST["genero"] == 'MA':
			beneficiado.embarazada = False
		else:
			beneficiado.embarazada = request.POST["embarazada"]
		beneficiado.f_nacimiento = request.POST["f_nacimiento"]
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