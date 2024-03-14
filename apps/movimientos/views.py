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

from .models import Ingreso
# Create your views here.

class ListadoIngresos(ListView):
	context_object_name = 'ingresos'
	template_name = 'pages/movimientos/ingresos/listado_ingresos.html'
	# permission_required = 'anuncios.requiere_secretria'
	model= Ingreso
	ordering = ['-id']
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Listado de ingresoss"
		return context

class DetalleIngreso(DetailView):
	template_name = 'pages/movimientos/ingresos/detalle_ingreso.html'
	# permission_required = 'anuncios.requiere_secretria'
	model = Ingreso
	context_object_name = 'ingreso'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context["sub_title"] = "Detalles del ingreso"
		return context