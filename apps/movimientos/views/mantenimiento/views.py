from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.generic import (
	UpdateView,
	ListView,
	CreateView,
	DetailView,
	View, 
	TemplateView
)
from apps.movimientos.models import TipoMov
from apps.movimientos.forms import FormTipoMovi

class ListadoTipoMovi(ListView):
	model = TipoMov
	context_object_name = 'tipo_movimiento'
	template_name = "pages/mantenimiento/tipo_movi.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		# Aquí puedes agregar datos adicionales al contexto
		context["sub_title"] = "Listado de tipos de movimientos"
		return 
	
class RegistrarTipoInsu(View):

	@method_decorator(csrf_exempt)
	def dispatch(self, request, *args, **kwargs):
		return super().dispatch(request, *args, **kwargs)

	def post(self, request, *args, **kwargs):
		data = {}
		try:
			action = request.POST['action']

			if action == 'nuevo_tipo_movi':
				form = FormTipoMovi(request.POST)

				if form.is_valid():
					form.save()
					data['response'] = {'title':'Exito!', 'data': 'Tipo de insumo registrado correctamente.', 'type_response': 'success'}
				else:
					data['response'] = {'title':'Ocurrió un error!', 'data': 'Ocurrió un error inesperado.', 'type_response': 'danger'}

		except Exception as e:
			data['error'] = str(e)
		return JsonResponse(data, safe=False)