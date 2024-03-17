from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.views.generic import (
	UpdateView,
	ListView,
	CreateView,
	DetailView,
	View, 
	TemplateView
)
from .forms import FormLab, FormTipoInsu, FormAlmacen

from .models import Producto, Inventario, Laboratorio, TipoInsumo, Almacen
from apps.movimientos.models import Historial

# Create your views here.
class ListadoProcuctos(ListView):
	context_object_name = 'productos'
	template_name = 'pages/productos/listado_productos.html'
	# permission_required = 'anuncios.requiere_secretria'
	model= Producto
	ordering = ['-id']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de productos"
		return context
	
class DetalleProductoView(DetailView):
	template_name = 'pages/productos/detalle_producto.html'
	# permission_required = 'anuncios.requiere_secretria'
	model = Producto
	context_object_name = 'producto'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Aquí puedes agregar datos adicionales al contexto
		producto = Producto.objects.filter(pk=self.kwargs.get('pk')).first()
		inventario = Inventario.objects.filter(producto_id=producto.pk).order_by('f_vencimiento')
		if producto and inventario:
			for i in inventario:
				historial = Historial.objects.filter(producto__producto__id=i.producto.pk).order_by('-pk')
		context["historial"] = historial
		context["inventario"] = inventario
		context["sub_title"] = "Detalles del producto"
		return context
	

class Laboratorio(ListView):
	model = Laboratorio
	context_object_name = 'laboratorios'
	template_name = "pages/mantenimiento/listado_lab.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Aquí puedes agregar datos adicionales al contexto
		context["sub_title"] = "Listado de Laboratorios"
		return context
	
class RegistrarLab(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_lab':
				form = FormLab(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Laboratorio registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ListadoTiposInsumos(ListView):
	model = TipoInsumo
	context_object_name = 'insumos'
	template_name = "pages/mantenimiento/tipo_insu.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Aquí puedes agregar datos adicionales al contexto
		context["sub_title"] = "Listado de tipos de insumos"
		return context
	
class RegistrarTipoInsu(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_tipo_insu':
				form = FormTipoInsu(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Tipo de insumo registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)
	
class ListadoAlmacen(ListView):
	model = Almacen
	context_object_name = 'almacenes'
	template_name = "pages/mantenimiento/listado_almacen.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Aquí puedes agregar datos adicionales al contexto
		context["sub_title"] = "Listado de almacenes"
		return context

class RegistrarAlmacen(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_almacen':
				form = FormAlmacen(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Almacen registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)