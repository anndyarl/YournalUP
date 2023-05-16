# from django.http import HttpResponse
from django.shortcuts import render
from .models import Trade # Importamos el modelo Trade



def index(request):
    if request.method == 'POST':
        # Manejar los datos enviados en el formulario POST
        activo = request.POST.get('activo')
        orden = request.POST.get('orden')
        stoploss = request.POST.get('stoploss')
        takeprofit = request.POST.get('takeprofit')
        lotaje = request.POST.get('lotaje')
        ratio = request.POST.get('ratio')
        beneficio_esperado = request.POST.get('beneficioEsperado')
        utilidad_proyectada = request.POST.get('utilidadProyectada')
        
        # Validar que todos los campos se hayan ingresado
        error = None
        if not activo:
            error = 'El campo activo es obligatorio.'
        elif not orden:
            error = 'El campo orden es obligatorio.'
        elif not stoploss:
            error = 'El campo stoploss es obligatorio.'
        elif not takeprofit:
            error = 'El campo takeprofit es obligatorio.'
        elif not lotaje:
            error = 'El campo lotaje es obligatorio.'
        elif not ratio:
            error = 'El campo ratio es obligatorio.'
        elif not beneficio_esperado:
            error = 'El campo beneficio esperado es obligatorio.'
        elif not utilidad_proyectada:
            error = 'El campo utilidad proyectada es obligatorio.'
            
        # Si hay algún error, renderizar el formulario con un mensaje de error
        if error is not None:
            return render(request, 'gestion_trading/index.html', {'error': error})
        else:
            # Crear un objeto Trade y guardarlo en la base de datos
            trade = Trade(activo=activo, orden=orden, stoploss=stoploss, takeprofit=takeprofit, lotaje=lotaje, ratio=ratio, beneficio_esperado=beneficio_esperado, utilidad_proyectada=utilidad_proyectada)
            trade.save()
            
            # Renderizar la plantilla index.html con un mensaje de éxito
            mensaje = 'Orden agregado correctamente.'
            return render(request, 'gestion_trading/index.html', {'mensaje': mensaje})
    else:
        # Renderizar la plantilla index.html con un formulario vacío
        return render(request, 'gestion_trading/index.html')    