from apps.entidades.mixins import ValidarUsuario
from django.db.models import Q

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
	