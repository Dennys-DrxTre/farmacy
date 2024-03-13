from django.urls import path
from .views import vista
urlpatterns = [
    path('vista/', vista.as_view()),
]
