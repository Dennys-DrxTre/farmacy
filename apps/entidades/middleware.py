from django.http import HttpResponseRedirect
from django.template.loader import get_template
from django.contrib import messages

class TemplateErrorMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if response.status_code == 404:
            response = HttpResponseRedirect('/inicio/')
        return response