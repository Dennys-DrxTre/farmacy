import json
from datetime import date
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
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
from django.views.generic import (
	TemplateView,
	ListView,
	UpdateView,
	DetailView,
	View
)

from apps.movimientos.models import Jornada

class MisSolicitudesJornadas(ValidarUsuario, TemplateView):
	permission_required = 'entidades.ver_mis_jornada_medicamentos'
	template_name = 'pages/movimientos/jornadas/mis_solicitudes_jornadas.html'
	# permission_required = 'anuncios.requiere_secretria'
	
	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		jornadas = Jornada.objects.filter(jefe_comunidad__cedula=self.request.user.perfil.cedula).order_by('-pk')
		context["sub_title"] = "Mis Solicitudes de Jornadas"	
		context['jornadas'] = jornadas
		return context