from django.urls import path
from .views import vista, landing

urlpatterns = [
    path('vista/', vista.as_view()),
    path('landing/', landing.as_view()),
]
