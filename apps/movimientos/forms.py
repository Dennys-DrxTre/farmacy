from django import forms
from .models import Ingreso, Solicitud, TipoMov

class IngresoForm(forms.ModelForm):
	tipo_ingreso = forms.ModelChoiceField(queryset=TipoMov.objects.filter(operacion=TipoMov.Operacion.SUMA))	
	class Meta:
		model = Ingreso
		fields = '__all__'

class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud
		fields = '__all__'

class FormTipoMovi(forms.ModelForm):
	class Meta:
		model = TipoMov
		fields = '__all__'