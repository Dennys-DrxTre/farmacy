from django import forms
from .models import Perfil, Zona

class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfil
		fields = '__all__'

class ZonaForm(forms.ModelForm):
	class Meta:
		model = Zona
		fields = '__all__'