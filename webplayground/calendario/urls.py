from django.urls import path
from . import views

urlpatterns = [
    path('calendario/', views.mostrar_calendario_por_anyo, name='calendario'),
]