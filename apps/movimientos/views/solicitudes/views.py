
import json
from datetime import date
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.core.serializers.json import DjangoJSONEncoder
from django.views.generic import (
	TemplateView,
	ListView,
	UpdateView,
	DetailView,
	View
)
from ...forms import SolicitudForm, BeneficiadoForm

from ...models import Solicitud, TipoMov, DetalleSolicitud, Historial
from apps.inventario.models import Inventario, Producto
from apps.entidades.models import Beneficiado,Perfil
# # Create your views here.

class SolicitudesMed(TemplateView):
	template_name = 'pages/movimientos/solicitudes/listado_solicitudes_med.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		solicitudes = Solicitud.objects.all().order_by('-pk')

		context["sub_title"] = "Solicitudes de medicamentos"
		context['solicitudes'] = solicitudes
		return context

class EditarSolicitud(SuccessMessageMixin, UpdateView):
	template_name = 'pages/movimientos/solicitudes/editar_solicitud_de_med.html'
	model = Solicitud
	form_class = SolicitudForm
	success_massage = 'La solicitud ha sido modificada correctamente'
	# permission_required = 'anuncios.requiere_secretria'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			with transaction.atomic():
				vents = json.loads(request.POST['vents'])

				solicitud = self.get_object()
				solicitud.descripcion = vents['descripcion']
				solicitud.beneficiado_id = vents['beneficiado']
				solicitud.recipe = request.FILES['recipe']
				solicitud.proceso_actual = vents['proceso_actual']
				solicitud.tipo_solicitud = vents['tipo_solicitud']
				solicitud.estado = vents['estado']
				solicitud.save()

				for det in vents['det']:
					producto = Producto.objects.filter(pk=det['id']).first()
					inventario = Inventario.objects.filter(producto_id=producto.pk).first()
					inventario.save()

					detalle = DetalleSolicitud.objects.filter(solicitud=self.get_object()).first()
					detalle.solicitud = solicitud
					detalle.producto = inventario
					detalle.cant_solicitada = det['cantidad']
					detalle.cant_entregada = det['cantidad_entregada']
					detalle.save()

				# 	perfil = Perfil.objects.filter(usuario=request.user).first()
				# 	movimiento = {
				# 		'tipo_mov': tipo_ingreso,
				# 		'perfil': perfil,
				# 		'producto': producto,
				# 		'cantidad': det['cantidad']
				# 	}
				# 	Historial().crear_movimiento(movimiento)

					messages.success(request,'Solicitud de medicamento registrado correctamente')
					data['response'] = {'title':'Exito!', 'data': 'Solicitud de medicamento registrado correctamente', 'type_response': 'success'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_detail(self):
		data = []
		try:
			for i in DetalleSolicitud.objects.filter(solicitud_id=self.get_object().id):
				item = i.producto.toJSON()
				item['cantidad'] = i.cant_solicitada
				item['cantidad_entregada'] = i.cant_entregada
				item['nombre'] = i.producto.producto.nombre
				item['id'] = i.producto.producto.pk
				item['text'] = i.producto.producto.nombre
				item['lote'] = i.producto.lote
				item['id_inventario'] = i.producto.pk
				item['producto'] = i.producto.producto.toJSON()
				data.append(item)
		except:
			pass
		return data

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Modificar solicitud"
		context["form_b"] = BeneficiadoForm()
		context['det'] = json.dumps(self.get_detail(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
		return context

# class DetalleMiSolicitudOnline(DetailView):
# 	template_name = 'pages/movimientos/solicitudes_online/detalle_solicitud_med_online.html'
# 	# permission_required = 'anuncios.requiere_secretria'
# 	model = Solicitud
# 	context_object_name = 'solicitud'

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context["sub_title"] = "Detalle de mi solicitud"
# 		return context
	
# class RegistrarMiSolicitud(TemplateView):
# 	template_name = 'pages/movimientos/solicitudes_online/registrar_mi_solicitud_de_med.html'
# 	# permission_required = 'anuncios.requiere_secretria'
# 	object = None

# 	@method_decorator(csrf_exempt)
# 	def dispatch(self, request, *args, **kwargs):
# 		return super().dispatch(request, *args, **kwargs)

# 	def post(self, request, *args, **kwargs):
# 		data = {}
# 		try:
# 			with transaction.atomic():
# 				vents = json.loads(request.POST['vents'])

# 				solicitud = Solicitud()
# 				solicitud.fecha_soli = date.today()
# 				solicitud.descripcion = vents['descripcion']
# 				solicitud.beneficiado_id = vents['beneficiado']
# 				solicitud.recipe = request.FILES['recipe']
# 				solicitud.proceso_actual = solicitud.FaseProceso.AT_CLIENTE
# 				solicitud.tipo_solicitud = solicitud.TipoSoli.ONLINE
# 				solicitud.estado = solicitud.Status.EN_PROCRESO 
# 				solicitud.save()

# 				for det in vents['det']:
# 					producto = Producto.objects.filter(pk=det['id']).first()
# 					inventario = Inventario.objects.filter(producto_id=producto.pk).order_by('f_vencimiento').first()
# 					inventario.save()

# 					detalle = DetalleSolicitud()
# 					detalle.solicitud = solicitud
# 					detalle.producto = inventario
# 					detalle.cant_solicitada = det['cantidad']
# 					detalle.save()

# 				# 	perfil = Perfil.objects.filter(usuario=request.user).first()
# 				# 	movimiento = {
# 				# 		'tipo_mov': tipo_ingreso,
# 				# 		'perfil': perfil,
# 				# 		'producto': producto,
# 				# 		'cantidad': det['cantidad']
# 				# 	}
# 				# 	Historial().crear_movimiento(movimiento)

# 					messages.success(request,'Solicitud de medicamento registrado correctamente')
# 					data['response'] = {'title':'Exito!', 'data': 'Solicitud de medicamento registrado correctamente', 'type_response': 'success'}
# 		except Exception as e:
# 			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
# 			data['error'] = str(e)
# 		return JsonResponse(data, safe=False)

# 	def get_context_data(self, **kwargs):
# 		context = super().get_context_data(**kwargs)
# 		context["sub_title"] = "Registrar ingreso"
# 		context["form"] = SolicitudForm(user=self.request.user)
# 		context["form_b"] = BeneficiadoForm()
# 		return context
	
class RegistrarBeneficiado(View):
	# permission_required = 'anuncios.requiere_secretria'
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			if not Beneficiado.objects.filter(cedula=request.POST['cedula']):
				beneficiado = Beneficiado()
				beneficiado.nacionalidad = request.POST['nacionalidad'] 
				beneficiado.cedula = request.POST['cedula'] 
				beneficiado.nombres = request.POST['nombres'] 
				beneficiado.apellidos = request.POST['telefono'] 
				beneficiado.genero = request.POST['genero'] 
				beneficiado.f_nacimiento = request.POST['f_nacimiento'] 
				beneficiado.embarazada = request.POST.get('embarazada') == 'on'
				beneficiado.zona_id = request.POST['zona'] 
				beneficiado.direccion = request.POST['direccion']
				beneficiado.perfil_id	 = request.user.perfil.pk
				beneficiado.save()
				data['response'] = {'title':'Exito!', 'data': 'El beneficiado se registro correctamente', 'type_response': 'success'}
			else:
				data['response'] = {'title':'Ocurrió un error!', 'data': 'El beneficiado ya existe', 'type_response': 'danger'}
				# 	data['response'] = {'title': 'Exito!', 'data':'Compra registrada correctamente', 'type_response': 'success'}
		except Exception as e:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
