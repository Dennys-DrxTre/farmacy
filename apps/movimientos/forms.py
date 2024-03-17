from django import forms
from .models import Ingreso, Solicitud, TipoMov
from apps.entidades.models import Beneficiado

class IngresoForm(forms.ModelForm):
	tipo_ingreso = forms.ModelChoiceField(queryset=TipoMov.objects.filter(operacion=TipoMov.Operacion.SUMA))	
	class Meta:
		model = Ingreso
		fields = '__all__'

class MiSolicitudForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(MiSolicitudForm, self).__init__(*args, **kwargs)
        if user is not None:
            self.fields['beneficiado'].queryset = Beneficiado.objects.filter(perfil__cedula=user.perfil.cedula)

    class Meta:
        model = Solicitud
        fields = ['descripcion', 'recipe', 'beneficiado']

class SolicitudForm(forms.ModelForm):
	class Meta:
		model = Solicitud
		fields = '__all__'
        
class BeneficiadoForm(forms.ModelForm):
	class Meta:
		model = Beneficiado
		fields = '__all__'