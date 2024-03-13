from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.

class vista(TemplateView):
    template_name = 'base/base.html'

class landing(TemplateView):
    template_name = 'landingPage/landing.html'