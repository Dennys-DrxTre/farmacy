from django import forms
from .models import Laboratorio, TipoInsumo, Almacen

class FormLab(forms.ModelForm):
	class Meta:
		model = Laboratorio
		fields = '__all__'

class FormTipoInsu(forms.ModelForm):
	class Meta:
		model = TipoInsumo
		fields = '__all__'
		
class FormAlmacen(forms.ModelForm):
	class Meta:
		model = Almacen
		fields = '__all__'