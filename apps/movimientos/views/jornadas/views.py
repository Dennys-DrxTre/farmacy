import json
from datetime import date
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib.auth.models import Permission
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.template.loader import render_to_string
from apps.movimientos.email_utils import EmailThread
from apps.entidades.mixins import ValidarUsuario
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from django.views.generic import (
	TemplateView,
	ListView,
	UpdateView,
	DetailView,
	View
)

from apps.movimientos.models import Jornada, DetalleJornada
from apps.inventario.models import Producto, Inventario
from apps.entidades.models import Comunidad

from apps.movimientos.forms import MiJornadaForm,ComunidadForm

class MisSolicitudesJornadas(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_mis_jornada_medicamentos'
	template_name = 'pages/jornadas/mis_solicitudes_jornadas.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		jornadas = Jornada.objects.filter(jefe_comunidad__cedula=self.request.user.perfil.cedula).order_by('-pk')
		context["sub_title"] = "Mis Solicitudes de Jornadas"	
		context['jornadas'] = jornadas
		return context
	
class SolicitudesJornadas(ValidarUsuario, TemplateView):
	permission_required = 'entidades.view_jornada'
	template_name = 'pages/jornadas/solicitudes_jornadas.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		jornadas = Jornada.objects.all().order_by('-pk')
		context["sub_title"] = "Solicitudes de Jornadas"	
		context['jornadas'] = jornadas
		return context
	
class DetalleMiJornada(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_mis_jornada_medicamentos'
	template_name = 'pages/jornadas/detalle_mi_jornada.html'
	# permission_required = 'anuncios.requiere_secretria'

	def get(self, request, pk, *args, **kwargs):
		context = {}
		try:
			mi_jornada = Jornada.objects.get(pk=pk, jefe_comunidad=request.user.perfil)
			context['jornada'] = mi_jornada
			context["sub_title"] = "Detalle de mi Jornada"
			return render(request, self.template_name, context)
		except Jornada.DoesNotExist:
			return redirect('mi_listado_jornadas')
		
class DetalleJornada(ValidarUsuario, TemplateView):
	permission_required = 'entidades.view_jornada'
	template_name = 'pages/jornadas/detalle_jornada.html'
	# permission_required = 'anuncios.requiere_secretria'

	def get(self, request, pk, *args, **kwargs):
		context = {}
		try:
			jornada = Jornada.objects.get(pk=pk)
			context['jornada'] = jornada
			context["sub_title"] = "Detalle de Jornada"
			return render(request, self.template_name, context)
		except Jornada.DoesNotExist:
			return redirect('listado_jornadas')

class RegistrarMiJornada(ValidarUsuario, TemplateView):
	permission_required = 'entidades.registrar_mi_jornada_medicamentos'
	template_name = 'pages/jornadas/registrar_mi_jornada.html'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])
			jornada = Jornada()
			jornada.fecha_solicitud = date.today()
			jornada.descripcion = vents['descripcion']
			jornada.jefe_comunidad_id = request.user.perfil.pk
			jornada.proceso_actual = jornada.FaseProceso.ADMINISTRADOR
			jornada.estado = jornada.Status.EN_PROCRESO 
			jornada.save()
			for det in vents['beneficiados']:
				comunidad = Comunidad.objects.filter(pk=det['id']).first()
				jornada.comunidad.add(comunidad)

			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['id']).first()

				detalle = DetalleJornada()
				detalle.jornada_id = jornada.pk
				detalle.producto_id = producto.pk
				detalle.cant_solicitada = det['cantidad']
				detalle.save()

			messages.success(request,'Solicitud de jornada registrada correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Solicitud de jornada registrada correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar Mi Jornada"
		context["form"] = MiJornadaForm()
		context["form_c"] = ComunidadForm()
		return context
	
class BuscarBeneficiadoComunidadView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST['action']
		if action == 'search_beneficiados':
			data = []
			ids_exclude = json.loads(request.POST.get('ids'))
			comunidad = Comunidad.objects.filter(Q(nombres__icontains=request.POST.get('term')) | Q(cedula__icontains=request.POST.get('term')), jefe_comunidad=request.user.perfil)
			for i in comunidad.exclude(pk__in=ids_exclude)[0:10]:
				item = i.toJSON()
				item['text'] = i.nombres
				item['id'] = i.pk
				data.append(item)

		elif action == 'search_beneficiados_table':
			data = []
			ids_exclude = json.loads(request.POST.get('ids'))
			comunidad = Comunidad.objects.filter(jefe_comunidad=request.user.perfil)
			for i in comunidad.exclude(pk__in=ids_exclude):
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombres)
				item['id'] = i.pk
				data.append(item)
		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}

		# except Exception as e:
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)