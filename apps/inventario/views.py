from datetime import date
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.contrib import messages
from django.views.generic import (
	UpdateView,
	ListView,
	CreateView,
	DetailView,
	View
)

from .models import Producto, Inventario
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
		inventario = Inventario.objects.filter(producto_id=producto.pk, f_vencimiento__gt=date.today(), stock__gt=0).order_by('f_vencimiento')
		if inventario:
			context["inventario"] = inventario

		if producto:
			for i in Inventario.objects.filter(producto_id=producto.pk).order_by('f_vencimiento'):
				historial = Historial.objects.filter(producto__producto__id=i.producto.pk).order_by('-pk')
				if historial:
					context["historial"] = historial
			
		context["sub_title"] = "Detalles del producto"
		return context