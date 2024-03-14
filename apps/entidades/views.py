from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class Inicio(TemplateView):
    template_name = 'pages/dashboard/inicio.html'

class landing(TemplateView):
    template_name = 'landingPage/landing.html'