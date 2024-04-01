from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.generic.base import View
from django.db.models import Q
from xhtml2pdf import pisa
import datetime
from datetime import date
from django.http import JsonResponse
from django.shortcuts import redirect
from django.db.models import Q

from apps.entidades.utils import link_callback
from .models import Jornada, Solicitud
from apps.entidades.mixins import ValidarUsuario

class TodasLasJornadas(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, pk, *args, **kwargs):
		try:
			jornada = Jornada.objects.filter(jefe_comunidad__zona = pk).order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de Jornadas por zonas',
				'logo_img': '{}'.format('static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'jornada': jornada,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todas_jornadas.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Jornada.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)
		
class TodasLasSolicitudes(View):
	# permission_required = 'anuncios.requiere_secretria'

	@method_decorator(login_required)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)
	
	def get(self, request, *args, **kwargs):
		try:
			solicitudes = Solicitud.objects.all().order_by('-id')
			formato_fecha = datetime.datetime.now().strftime("%d/%m/%Y")
			context = {
				'report_title': 'Listado de solicitudes',
				'logo_img': '{}'.format('static/images/logo.jpg'),
				'user': f'{request.user.get_full_name()}',
				'solicitudes': solicitudes,
				'date': formato_fecha,
				'request':request,
			}
			template_path= get_template('reportes/todas_solicitudes.html')
			html = template_path.render(context)
			response = HttpResponse(content_type='application/pdf')
			pisa.CreatePDF(html, dest=response, link_callback=link_callback)
			return response
		except Solicitud.DoesNotExist:
			return redirect('vista')
		except Exception as e:
			return JsonResponse({'error': str(e)}, safe=False)