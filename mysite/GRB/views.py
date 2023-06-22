"""
Este módulo contiene importaciones.
"""
from django.shortcuts import render, redirect, reverse
from .models import TRADES, CUENTAS, TRADEIMAGE, IMAGE
from .forms import TradeForm, CuentaForm

# from .forms import ImagenForm
# from django.http import Http404
# from django.http import JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseForbidden

# import os
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.models import User
from .forms import CustomAuthForm
from django.core.files.storage import default_storage

# from django.core.files.base import ContentFile
# from django.contrib import messages
# from django.shortcuts import get_object_or_404
# from django.contrib.auth.models import User
from datetime import datetime
import uuid
from django.db.models import Sum
# from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.forms import UserCreationForm



@csrf_protect
def custom_login(request):
    """
    Vista para la página "custom_login".
    """
    if request.user.is_authenticated:
        return redirect("seleccionar_cuenta")

    if request.method == "POST":
        form = CustomAuthForm(request, request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                request.session["user_id"] = user.id

            url = reverse("seleccionar_cuenta")
            return redirect(url)
    else:
        form = CustomAuthForm(request)

    return render(request, "paginas/login.html", {"form": form})

@csrf_protect
def logout_view(request):
    """
    Vista para la página "logout_view".
    """
    logout(request)
    if not request.user.is_authenticated:
        return redirect("login")
    

@csrf_protect
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige al usuario al formulario de inicio de sesión después del registro exitoso
    else:
        form = UserCreationForm()
    return render(request, 'paginas/register.html', {'form': form})
# def inicio(request):
#     return render(request, "paginas/inicio.html")

@csrf_protect
def nosotros(request):
    """
    Vista para la página "Nosotros".
    """
    return render(request, "paginas/nosotros.html")

@csrf_protect
def seleccionar_cuenta(request):
    """
    Vista para la página "seleccionar_cuenta".
    """     
    if not request.user.is_authenticated:
        return redirect("login")
    return render(request, "cuentas/seleccionar_cuenta.html")

@csrf_protect
def lista_cuentas(request, id_tipo_cuenta):
    """
    Vista para la página "lista_cuentas".
    """
    if not request.user.is_authenticated:
        return redirect("login")
    request.session["id_tipo_cuenta"] = id_tipo_cuenta
    cuentas = CUENTAS.objects.filter(
        user=request.user, id_tipo_cuenta_id=id_tipo_cuenta
    )
    return render(request, "cuentas/cuentas.html", {"cuentas": cuentas})

@csrf_protect
def lista_trades_de_cuentas(request, id_cuenta):
    """
    Vista para la página "lista_cuentas_id".
    """
    if not request.user.is_authenticated:
        return redirect("login")    
    request.session["id_cuenta"] = id_cuenta
    cuenta = CUENTAS.objects.get(id_cuenta=id_cuenta)
    cuentas = CUENTAS.objects.all()
    trades = TRADES.objects.filter(id_cuenta_id=id_cuenta)
    user = request.user  # Obtiene el objeto de usuario autenticado
    

    id_tipo_cuenta = request.session["id_tipo_cuenta"]
    formulario = CuentaForm(request.POST or None, id_tipo_cuenta=id_tipo_cuenta, instance=cuenta)
    if formulario.is_valid():
        cuenta = formulario.save(commit=False)         

    beneficio_total = TRADES.objects.filter(id_cuenta_id=id_cuenta).aggregate(total_beneficio_real=Sum('beneficio_real'))['total_beneficio_real']
    if beneficio_total is None:
        beneficio_total = 0
    else:
        beneficio_total = round(beneficio_total, 2)

    porcentaje_beneficio_total = TRADES.objects.filter(id_cuenta_id=id_cuenta).aggregate(total_porcentaje_beneficio_real=Sum('porcentaje_beneficio_real'))['total_porcentaje_beneficio_real']
    if porcentaje_beneficio_total is None:
        porcentaje_beneficio_total = 0
    else:
        porcentaje_beneficio_total = round(porcentaje_beneficio_total, 2)
    
    cuenta_inicial = cuenta.cuenta
    comision = cuenta.comision
    swap = cuenta.swap

    capital_actual = 0

    if beneficio_total is not None:
        capital_actual += beneficio_total

    # if porcentaje_beneficio_total is not None:
    #     capital_actual += porcentaje_beneficio_total  

    if comision is not None:
        capital_actual += comision

    if swap is not None:
        capital_actual += swap

    if isinstance(user, User):  # Check if user is your custom User model
        cuenta.user = user
    cuenta.capital_actual = cuenta_inicial + capital_actual  
    cuenta.id_tipo_cuenta_id = id_tipo_cuenta
    if 0 < cuenta.riesgo_operacion < 1:
                    cuenta.nivel_riesgo = "Muy Conservador"
    elif cuenta.riesgo_operacion == 1:
                    cuenta.nivel_riesgo = "Optimo"
    elif 1 < cuenta.riesgo_operacion < 1.5:
                    cuenta.nivel_riesgo = "Bueno"
    elif 1.5 <= cuenta.riesgo_operacion <= 2:
                    cuenta.nivel_riesgo = "Moderado"
    elif 2 < cuenta.riesgo_operacion < 3:
                    cuenta.nivel_riesgo = "Riesgoso"
    elif cuenta.riesgo_operacion >= 3:
                    cuenta.nivel_riesgo = "Muy Riesgoso"
    else:
                    cuenta.nivel_riesgo = "N/A"
    cuenta.save()
    
    n_registros = trades.filter(
        resultado__in=[
            "Stop Loss",
            "Take Profit",
            "Break Even",
            "Cierre Manual en Positivo",
            "Cierre Manual en Negativo",
        ]
    ).count()
    o_restantes = int(cuenta.n_operaciones) - n_registros
    exist_row = trades.count()

    if o_restantes < 0:
        mensaje_error = f"Error: la cuenta ya tiene {abs(o_restantes)} operaciones con 'Programada' o 'Stop Loss'. No se pueden agregar más."
        context = {
            "cuentas": cuentas,
            "lista_trades_de_cuentas": trades,
            "mensaje_error": mensaje_error,
        }
    else:
        cuenta.operaciones_restantes = o_restantes
        nivel_riesgo = cuenta.nivel_riesgo
        
        cuenta.save()
        context = {
            "cuentas": cuentas,
            "lista_trades_de_cuentas": trades,
            "exist_row": exist_row,
            "beneficio_total": beneficio_total,
            "porcentaje_beneficio_total": porcentaje_beneficio_total,
            "capital_actual": capital_actual,
            "formulario": formulario,
            "id_cuenta": id_cuenta,
            "nivel_riesgo": nivel_riesgo,
        }

    return render(request, "cuentas/trades/trades.html", context)

@csrf_protect
def crear_cuentas(request, id_tipo_cuenta):
    if not request.user.is_authenticated:
        return redirect("login")
    
    error_message = ""
    cuentas = CUENTAS.objects.all()
    user = request.user   
    request.session["id_tipo_cuenta"] = id_tipo_cuenta 
    try:
        formulario = CuentaForm(request.POST or None, id_tipo_cuenta=id_tipo_cuenta, initial={'user': user})
      
        if request.method == "POST" and formulario.is_valid():
            
            cuenta = formulario.save(commit=False)
            cuenta.id_tipo_cuenta_id = id_tipo_cuenta
            cuenta.riesgo_operacion = float(formulario.cleaned_data.get("riesgo_operacion"))
            cuenta.n_operaciones = formulario.cleaned_data.get("n_operaciones")
            
            try:                
                if id_tipo_cuenta == 1:
                    cuenta.cuenta_seleccionada = formulario.cleaned_data.get("cuenta")
                    cuenta.capital_actual = cuenta.cuenta_seleccionada
                elif id_tipo_cuenta == 2:
                    cuenta.cuenta_ingresada = formulario.cleaned_data.get("cuenta")
                    cuenta.capital_actual = cuenta.cuenta_ingresada

                cuenta.operaciones_restantes = cuenta.n_operaciones

                if 0 < cuenta.riesgo_operacion < 1:
                    cuenta.nivel_riesgo = "Muy Conservador"
                elif cuenta.riesgo_operacion == 1:
                    cuenta.nivel_riesgo = "Optimo"
                elif 1 < cuenta.riesgo_operacion < 1.5:
                    cuenta.nivel_riesgo = "Bueno"
                elif 1.5 <= cuenta.riesgo_operacion <= 2:
                    cuenta.nivel_riesgo = "Moderado"
                elif 2 < cuenta.riesgo_operacion < 3:
                    cuenta.nivel_riesgo = "Riesgoso"
                elif cuenta.riesgo_operacion >= 3:
                    cuenta.nivel_riesgo = "Muy Riesgoso"
                else:
                    cuenta.nivel_riesgo = "N/A"
                  # Asignar el valor a la variable nivel_riesgo
               
               
                if isinstance(user, User):
                    cuenta.user = user

                cuenta.save()
                url = reverse("lista_cuentas", args=[id_tipo_cuenta])
                return redirect(url)

            except Exception as e:
                error_message = "Ocurrió un error al procesar los datos del formulario: {}".format(str(e))
      
        context = {
            "cuentas": cuentas,
            "formulario": formulario,
            "id_tipo_cuenta": id_tipo_cuenta,
            "error_message": error_message,
            "user_value": str(user),          
        }
        return render(request, "cuentas/crear_cuentas.html", context)
    except Exception as e:
        error_message = "Se produjo un error al crear la cuenta: {}".format(str(e))
        context = {
            "cuentas": cuentas,
            "formulario": None,
            "id_tipo_cuenta": id_tipo_cuenta,
            "error_message": error_message,
            "user_value": str(user),
        }
        return render(request, "cuentas/crear_cuentas.html", context)

# def editar_cuentas(request, id_cuenta):
#     """
#     Vista para la página "editar_cuentas".
#     """
#     if not request.user.is_authenticated:
#         return redirect("login")
#     cuentas = CUENTAS.objects.get(id_cuenta=id_cuenta)
#     formulario = CuentaForm(request.POST or None, instance=cuentas)
#     return render(request, "cuentas/editar_cuentas.html", {"formulario": formulario})
@csrf_protect
def eliminar_cuenta(request, id_cuenta, id_tipo_cuenta):
    """
    Vista para la página "eliminar_cuenta".
    """
    request.session["id_tipo_cuenta"] = id_tipo_cuenta
    cuentas = CUENTAS.objects.get(id_cuenta=id_cuenta)
    cuentas.delete()
    url = reverse(
        "lista_cuentas", args=[id_tipo_cuenta]
    )  # obtén la URL de la vista lista_de_trades
    return redirect(url)


@csrf_protect
def crear(request):
    """
    Vista para la página "crear".
    """
    if not request.user.is_authenticated:
        return redirect("login")

    cuentas = CUENTAS.objects.all()
    formulario = TradeForm(request.POST or None, request.FILES or None)

    if formulario.is_valid():
        trade = formulario.save(commit=False)

        # Obtener la cuenta del nuevo trade
        id_cuenta = request.session.get('id_cuenta')
        
        try:
            cuenta = CUENTAS.objects.get(id_cuenta=id_cuenta)
        except ObjectDoesNotExist:
            error_message = "La cuenta no existe"
            context = {
                "cuentas": cuentas,
                "formulario": formulario,
                "error_message": error_message,
            }
            return render(request, "cuentas/trades/crear.html", context)

        # Obtener el número de registros de resultados
        n_registros = TRADES.objects.filter(id_cuenta_id=id_cuenta).filter(
            resultado__in=[
                "Stop Loss",
                "Take Profit",
                "Break Even",
                "Cierre Manual en Positivo",
                "Cierre Manual en Negativo",
            ]
        ).count()

        # Verificar si se puede crear un nuevo registro
        if n_registros >= int(cuenta.n_operaciones):
            error_message = "Ha superado el máximo de operaciones recomendadas"
            context = {
                "cuentas": cuentas,
                "formulario": formulario,
                "error_message": error_message,
            }
            return render(request, "cuentas/trades/crear.html", context)

        trade.id_cuenta_id = id_cuenta  # Asignar el id_cuenta_id al objeto trade
        trade.save()  # Guardar el trade en la base de datos

        return redirect("editar", trade.id)

    context = {"cuentas": cuentas, "formulario": formulario}
    return render(request, "cuentas/trades/crear.html", context)


@csrf_protect
def editar(request, id):
    """
    Vista para la página "editar".
    """
    try:
        if not request.user.is_authenticated:
            return redirect("login")

        request.session["id"] = id
        trade = TRADES.objects.get(id=id)
        cuentas = CUENTAS.objects.all()
        get_id_trade_images = TRADEIMAGE.objects.filter(trade_id=id)
        recorre_clase_image = [(trade_image.image, trade_image)
                               for trade_image in get_id_trade_images]

        # Formatear la fecha del objeto trade
        trade_fecha_str = trade.fecha.strftime("%d/%m/%Y")
        trade.fecha = datetime.strptime(trade_fecha_str, "%d/%m/%Y").date()

        formulario = TradeForm(request.POST, request.FILES, instance=trade)
        if request.method == "POST" and formulario.is_valid():  
                try:    
                   
                    # Obtener la cuenta del nuevo trade
                    id_cuenta = request.session.get('id_cuenta')
                    # Obtiene los datos que se ingresan y luego los guarda en la base de datos asociándolos al trade
                    if request.FILES:                   
                        for image in request.FILES.getlist('image'):
                            titulo = request.POST.get('titulo')
                            descripcion = request.POST.get('descripcion')

                            img = IMAGE.objects.create(image=image, titulo=titulo, descripcion=descripcion)
                            # Crear una nueva instancia de TradeImage y guardarla en la base de datos
                            new_trade_image = TRADEIMAGE(trade=trade, image=img)
                            new_trade_image.save()
                    # trade_image_ids = []
                    # Actualizar los títulos, descripciones y las imágenes existentes                  
                    for image, trade_image in recorre_clase_image:                       
                        titulo = request.POST.get(f'titulo_{trade_image.id}')
                        descripcion = request.POST.get(f'descripcion_{trade_image.id}')
                        if request.FILES.get(f'image_{trade_image.id}'):
                            image_file = request.FILES.get(f'image_{trade_image.id}')
                            # Eliminar la imagen anterior
                            default_storage.delete(trade_image.image.image.path)
                            # Guardar la nueva imagen en el sistema de archivos
                            # image_name = f'{str(uuid.uuid4())}.{image_file.name.split(".")[-1]}'                          
                            image_path = default_storage.save(f'imagenes/{image_file.name}', image_file)
                            trade_image.image.image = image_path
                        trade_image.image.titulo = titulo
                        trade_image.image.descripcion = descripcion
                        # trade_image_ids.append(trade_image.id)
                        trade_image.image.save()

                    trade.id_cuenta_id = id_cuenta  # Asignar el id_cuenta_id al objeto trade
                    trade = formulario.save()                   
                 
                    return redirect("editar", trade.id)
                except Exception as e:
                     error_message = "Se produjo un error al procesar los datos del formulario: {}".format(str(e))
        else:
            formulario = TradeForm(instance=trade)

        error_message = ""
        context = {
            "cuentas": cuentas,
            "formulario": formulario,
            "recorre_clase_image": recorre_clase_image,
            "error_message": error_message
               
        }
        return render(request, "cuentas/trades/editar.html", context)

    except Exception as e:
        error_message = "Se produjo un error al procesar los datos del formulario: {}".format(str(e))

    context = {"error_message": error_message}
    return render(request, "cuentas/trades/editar.html", context)




@csrf_protect
def eliminar(request, id):
    """
    Elimina Trade completo
    """
    trade = TRADES.objects.get(id=id)
    id_cuenta = trade.id_cuenta_id

    # Eliminar las imágenes asociadas a la tabla tradeimage
    trade_images = TRADEIMAGE.objects.filter(trade=trade)
    for trade_image in trade_images:
        # Eliminar la imagen del sistema de archivos
        default_storage.delete(trade_image.image.image.name)
        # Eliminar la instancia de TradeImage
        trade_image.delete()
        # Eliminar la instancia de Image correspondiente a la imagen eliminada de TradeImage
        trade_image.image.delete()
    # Eliminar el trade
    trade.delete()

    url = reverse("lista_trades_de_cuentas", args=[id_cuenta])
    return redirect(url)


def eliminar_imagen(request, image_id):
    """
    Elimina una imagen, titulo y descripcion recientemente guardada.
    """
    try:
        image = IMAGE.objects.get(id=image_id)
        # Eliminar la imagen del sistema de archivos
        default_storage.delete(image.image.path)
        # Eliminar la imagen de la base de datos
        image.delete()
    except ObjectDoesNotExist:
        pass
    # Redirigir al usuario a la página anterior
    return redirect(request.META.get('HTTP_REFERER', '/'))


