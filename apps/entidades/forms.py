from django import forms
from .models import Perfil, Zona, LandingPage

class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfil
		fields = '__all__'

class ZonaForm(forms.ModelForm):
	class Meta:
		model = Zona
		fields = '__all__'

class FormLanding(forms.ModelForm):
	class Meta:
		model = LandingPage
		fields = '__all__'