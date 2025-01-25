from django.shortcuts import render
from django.urls import reverse
from datetime import datetime
from django.template.loader import render_to_string
from django.templatetags.static import static  # Importar static para URLs relativas
from .models import CalendarioPersonalizadoHTML
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse


MESES = ['Enero', 'Febrero', 'Marzo', 'Abril', 'Mayo', 'Junio', 
         'Julio', 'Agosto', 'Septiembre', 'Octubre', 'Noviembre', 'Diciembre']

@login_required
def mostrar_calendario(request, anyo=None):
    """Vista para mostrar el calendario del anyo en curso o el especificado."""
    if anyo is None:
        anyo = datetime.now().year
    else:
        anyo = int(anyo)

    calendario = CalendarioPersonalizadoHTML()  
    meses = []  

    for mes in range(1, 13):
        mes_html = calendario.formatear_mes(anyo, mes)
        meses.append({
            'nombre': MESES[mes - 1],
            'html': mes_html
        })

    contexto = {
        'anyo': anyo,
        'meses': meses,
    }

    return render(request, 'calendario/calendario.html', contexto) 

@login_required
def mostrar_calendario_por_anyo(request, anyo=None):
    """Vista para mostrar el calendario del anyo especificado por el usuario, o el actual si no se especifica."""
    # Obtenemos el anyo desde el formulario (GET), o el actual si no se especifica
    anyo = request.GET.get('anyo', datetime.now().year)
    try:
        anyo = int(anyo)
    except ValueError:
        anyo = datetime.now().year

    calendario = CalendarioPersonalizadoHTML()
    meses = []

    for mes in range(1, 13):
        mes_html = calendario.formatear_mes(anyo, mes)
        meses.append({
            'nombre': MESES[mes - 1],
            'html': mes_html
        })

    contexto = {
        'anyo': anyo,
        'meses': meses,
    }

    return render(request, 'calendario/calendario.html', contexto)