import json
from datetime import date, datetime

from apps.entidades.mixins import ValidarUsuario
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.db import transaction
from django.contrib import messages
from django.shortcuts import render, redirect

from django.views.generic import (
	TemplateView,
	UpdateView,
	DetailView,
	View
)

from apps.movimientos.models import ContabilidadFisica, DetContabilidadFisica, InventarioContFisica
from apps.inventario.models import Producto, Inventario
from apps.entidades.models import Perfil
from django.contrib.auth.models import User

from apps.movimientos.forms import ContabilidadForm

class ListadoContabilidadFisica(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.view_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/listado_contabilidad_fisica.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		contabilidades_fisicas = ContabilidadFisica.objects.all().order_by('-pk')
		context["sub_title"] = "Listado de ajuste de inventario fisico"	
		context['contabilidades_fisicas'] = contabilidades_fisicas
		return context

class DetalleContabilidadFisica(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.view_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/detalle_contabilidad_fisica.html'
	# permission_required = 'anuncios.requiere_secretria'

	def get(self, request, pk, *args, **kwargs):
		context = {}
		try:
			contabilidad = ContabilidadFisica.objects.get(pk=pk)
			context['contabilidad'] = contabilidad
			context["sub_title"] = "Detalle de Inventario fisico"
			return render(request, self.template_name, context)
		except ContabilidadFisica.DoesNotExist:
			return redirect('listado_contabilidad_fisica')
	
	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = []
		# try:
		with transaction.atomic():
			pk = request.POST.get('pk')
			for i in InventarioContFisica.objects.filter(detcontabilidad_id=pk):
				item = i.toJSON()
				data.append(item)
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

class RegistrarContabilidadFisica(ValidarUsuario, TemplateView):
	permission_required = 'movimientos.add_contabilidadfisica'
	template_name = 'pages/contabilidad_fisica/registrar_contabilidad_fisica.html'
	object = None

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		with transaction.atomic():
			vents = json.loads(request.POST['vents'])
			contabilidad = ContabilidadFisica()
			contabilidad.proceso_actual = ContabilidadFisica.FaseProceso.ALMACENISTA
			contabilidad.estado = ContabilidadFisica.Status.EN_PROCRESO 
			contabilidad.save()

			for det in vents['det']:
				producto = Producto.objects.filter(pk=det['id']).first()

				detalle = DetContabilidadFisica()
				detalle.contabilidad_id = contabilidad.pk
				detalle.producto_id = producto.pk
				detalle.cantidad_contada = det['cantidad']
				detalle.cantidad_inventario = producto.total_stock
				detalle.save()

				for inv in det['inv']:
					det_inv = InventarioContFisica()
					det_inv.detcontabilidad_id = detalle.pk
					det_inv.inventario_id = inv['id']
					det_inv.cantidad_contada = inv['cantidad_contada']
					det_inv.cantidad_inventario = inv['stock']
					det_inv.save()

			messages.success(request,'Solicitud de jornada registrada correctamente')
			data['response'] = {'title':'Exito!', 'data': 'Solicitud de jornada registrada correctamente', 'type_response': 'success'}
		# except Exception as e:
		# 	data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Registrar Inventario fisico"
		# context["form"] = ContabilidadForm()
		return context
	
class BuscarProductosValidadosView(ValidarUsuario, View):
	permission_required = 'entidades.ver_inicio'

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		# try:
		action = request.POST['action']
		if action == 'cargar_productos':
			data = []
			productos = Producto.objects.filter(Q(comprometido__gt=0) | Q(total_stock__gt=0))
			for i in productos:
				item = i.toJSON()
				item['text'] = '{}'.format(i.nombre)
				item['tipo_insumo'] = i.tipo_insumo.nombre
				item['id'] = i.pk
				item['cantidad'] = 0
				item['inv'] = []
				for inventario in Inventario.objects.filter(Q(comprometido__gt=0) | Q(stock__gt=0), producto_id=i.pk).order_by('f_vencimiento'):
					item['inv'].append(inventario.toJSON())
				data.append(item)
		else:
			data['response'] = {'title':'Ocurrió un error!', 'data': 'Ha ocurrido un error en la solicitud', 'type_response': 'danger'}

		# except Exception as e:
		# 	data['error'] = str(e)
		return JsonResponse(data, safe=False)