from django import forms
from .models import Ingreso

class IngresoForm(forms.ModelForm):
	class Meta:
		model = Ingreso
		fields = '__all__'