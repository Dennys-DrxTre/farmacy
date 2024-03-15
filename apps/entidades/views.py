from django.shortcuts import render
from django.views.generic import TemplateView, CreateView
from apps.entidades.models import Perfil, Persona, User
from .forms import PerfilForm
from django.urls import reverse_lazy

# Create your views here.

class Inicio(TemplateView):
    template_name = 'pages/dashboard/inicio.html'

class landing(TemplateView):
    template_name = 'landingPage/landing.html'

class RegistrarPerfil(CreateView):
    model = Perfil
    form_class = PerfilForm
    template_name = 'pages/entidades/registrar_perfil.html'
    success_url = reverse_lazy('vista')