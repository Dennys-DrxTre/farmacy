from django import forms
from .models import Perfil

class PerfilForm(forms.ModelForm):
	class Meta:
		model = Perfil
		exclude = ['usuario']
		