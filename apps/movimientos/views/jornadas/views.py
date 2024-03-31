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
from django.template.loader import render_to_string
from apps.movimientos.email_utils import EmailThread
from django.db.models import Q

from django.views.generic import (
	TemplateView,
	ListView,
	UpdateView,
	DetailView,
	View
)

from apps.movimientos.models import Jornada, DetalleJornada,DetalleIventarioJornada
from apps.inventario.models import Producto, Inventario
from apps.entidades.models import Comunidad
from django.contrib.auth.models import User

from apps.movimientos.forms import MiJornadaForm,ComunidadForm, JornadaEditForm

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
		
class DetalleJornadaView(ValidarUsuario, TemplateView):
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
	
class EditarJornada(ValidarUsuario, SuccessMessageMixin, UpdateView):
	permission_required = 'movimientos.change_jornada'
	template_name = 'pages/jornadas/modificar_jornada.html'
	model = Jornada
	form_class = JornadaEditForm
	success_massage = 'La jornada ha sido modificada correctamente'
	# permission_required = 'anuncios.requiere_secretria'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		if not request.user.perfil.rol == 'AD':
			return redirect('listado_jornadas')
		return super().dispatch(request, *args, **kwargs)

	def producto_proximo_a_vencer(self, producto):
		# Obtiene la fecha actual
		hoy = date.today()
		# Busca en el inventario del producto aquellos que estén próximos a vencer
		inventarios_proximos = producto.inventario.filter(f_vencimiento__gt=hoy, stock__gt=0).order_by('f_vencimiento')
		return inventarios_proximos

	def descontar_stock(self, inventario, cantidad, detalle):
		detjornada = DetalleIventarioJornada()
		detjornada.detjornada = detalle
		detjornada.inventario = inventario
		
		if inventario.stock >= cantidad:
			inventario.stock -= cantidad
			inventario.comprometido += cantidad
			detjornada.cantidad = cantidad
			detjornada.save()
			inventario.save()
			return 0 # Indica que no hay cantidad restante
		else:
			restante = cantidad - inventario.stock
			detjornada.cantidad = inventario.stock
			detjornada.save()
			inventario.comprometido += inventario.stock
			inventario.stock = 0
			inventario.save()
			return restante # Indica que no hay cantidad restante
		
	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])
			jornada = self.get_object()
			jornada.descripcion = vents['descripcion']
			jornada.encargados = vents['encargados']
			jornada.fecha_jornada = vents['fecha_jornada']
			jornada.estado = vents['estado']
			jornada.jefe_comunidad = jornada.jefe_comunidad

			if vents['estado'] == 'AP':
					jornada.proceso_actual = Jornada.FaseProceso.ALMACENISTA
			elif vents['estado'] == 'RE':
				jornada.motivo_rechazo = vents['motivo_rechazo']
				jornada.proceso_actual = Jornada.FaseProceso.FINALIZADO
			jornada.save()

			DetalleIventarioJornada.objects.filter(detjornada__jornada=self.get_object()).delete()
			DetalleJornada.objects.filter(jornada=self.get_object()).delete()

			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['id']).first()

				detalle = DetalleJornada() 
				detalle.jornada = jornada
				detalle.producto = producto
				detalle.cant_solicitada = det['cantidad']
				detalle.cant_aprobada = det['cant_aprobada']
				detalle.save()

				if vents['estado'] == 'AP':
					cantidad_restante = det['cantidad_entregada']
					while cantidad_restante > 0:
						inventarios_proximos = self.producto_proximo_a_vencer(producto)
						if inventarios_proximos.exists():
							# Asume que se descontará del primer inventario próximo a vencer
							inventario = inventarios_proximos.first()
							cantidad_restante = self.descontar_stock(inventario, cantidad_restante, detalle)
						else:
							# Si no hay inventarios próximos a vencer, se detiene el proceso
							break
					producto.contar_productos()
					# # # enviando el correo de registro
					# Cargar la plantilla HTML
					usuario = User.objects.filter(username=f'{jornada.jefe_comunidad.nacionalidad}{jornada.jefe_comunidad.cedula}').first()
					html_content = render_to_string('templates/email/email_jornada_apro.html', {'correo': usuario.email, 'nombres': usuario.perfil.nombres, 'apellidos':  usuario.perfil.apellidos})
					# Configurar el correo electrónico
					subject, from_email, to = 'SU JORNADA HA SIDO PROCESADA CON EXITO', 'FARMACIA COMUNITARIA ASIC LEONIDAS RAMOS', usuario.email
					text_content = f'Su solicitud de jornada fue aprobada para la fecha:{jornada.fecha_jornada}.'
					EmailThread(subject, text_content, from_email, [to], False, html_content).start()
			messages.success(request,'Solicitud de jornada modificado correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Solicitud de jornada modificado correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_det(self):
		det = []
		try:
			for i in DetalleJornada.objects.filter(jornada=self.get_object()):
				item = i.producto.toJSON()
				item['cantidad'] = i.cant_solicitada
				item['cant_aprobada'] = i.cant_aprobada
				item['nombre'] = i.producto.nombre
				item['id'] = i.producto.pk
				item['text'] = i.producto.nombre
				det.append(item)
		except:
			pass
		return det
	
	def get_comunidad(self):
		comunidad = []
		try:
			for c in self.get_object().comunidad.all():
				item = c.toJSON()
				comunidad.append(item)
		except:
			pass
		return comunidad

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['rol'] = self.request.user.perfil.rol
		context["sub_title"] = "Modificar Jornada"
		context['det'] = json.dumps(self.get_det(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
		context['comunidad'] = json.dumps(self.get_comunidad(),  sort_keys=True,indent=1, cls=DjangoJSONEncoder)
		context['jefe_comunidad'] = self.get_object().jefe_comunidad.pk
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
	
class BuscarBeneficiadoComunidadModificacionView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST['action']
		jefe_comunidad = request.POST.get('jefe_comunidad')
		if action == 'search_beneficiados':
			data = []
			ids_exclude = json.loads(request.POST.get('ids'))
			comunidad = Comunidad.objects.filter(Q(nombres__icontains=request.POST.get('term')) | Q(cedula__icontains=request.POST.get('term')), jefe_comunidad_id=jefe_comunidad)
			for i in comunidad.exclude(pk__in=ids_exclude)[0:10]:
				item = i.toJSON()
				item['text'] = i.nombres
				item['id'] = i.pk
				data.append(item)

		elif action == 'search_beneficiados_table':
			data = []
			ids_exclude = json.loads(request.POST.get('ids'))
			comunidad = Comunidad.objects.filter(jefe_comunidad_id=jefe_comunidad)
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