"""
Este módulo contiene importaciones.
"""
# Importaciones de Django
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponseBadRequest, HttpResponseForbidden, HttpResponse, JsonResponse, HttpResponseServerError
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_protect
from django.core.files.storage import default_storage
from django.conf import settings
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from django.urls import resolve

# Importaciones de terceros
from paypal.standard.forms import PayPalPaymentsForm

# Importaciones de tu aplicación
from .models import TRADES, CUENTAS, TRADEIMAGE, IMAGE, PARCIALES, TRADEPARCIALES
from .forms import TradeForm, CuentaForm, ParcialesForm
from .forms import CustomAuthForm


# Importaciones estándar de Python
import json
import requests
from typing import Any, Union
from decimal import Decimal
from django.utils.text import slugify
import os
import shutil
from datetime import datetime
import uuid


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
      
    cuentas = CUENTAS.objects.filter(
        user=request.user, id_tipo_cuenta_id=id_tipo_cuenta        
    )    
    mensajes = messages.get_messages(request)
    return render(request, "cuentas/cuentas.html", {"cuentas": cuentas,"id_tipo_cuenta": id_tipo_cuenta,"mensajes": mensajes })

@csrf_protect
def lista_trades_de_cuentas(request, id_cuenta):
    if not request.user.is_authenticated:
        return redirect("login")
       
    cuenta = CUENTAS.objects.get(id_cuenta=id_cuenta)
    cuentas = CUENTAS.objects.all()
    # trades = TRADES.objects.filter(id_cuenta_id=id_cuenta)
    trades = TRADES.objects.filter(id_cuenta=id_cuenta, estado='activo')
    trades_eliminados = TRADES.objects.filter(id_cuenta=id_cuenta, estado='eliminado')
    user = request.user

    mensaje_error = ""
    id_tipo_cuenta = cuenta.id_tipo_cuenta_id
    id_cuenta = cuenta.id_cuenta   
    formulario = CuentaForm(request.POST or None, id_tipo_cuenta=id_tipo_cuenta, instance=cuenta)

    if formulario.is_valid():
        cuenta = formulario.save(commit=False)
    
    beneficio_total = TRADES.objects.filter(id_cuenta_id=id_cuenta).aggregate(total_beneficio_real=Sum('beneficio_real'))['total_beneficio_real']
    beneficio_total = beneficio_total or 0
    beneficio_total = round(beneficio_total, 2)

    porcentaje_beneficio_total = TRADES.objects.filter(id_cuenta_id=id_cuenta).aggregate(total_porcentaje_beneficio_real=Sum('porcentaje_beneficio_real'))['total_porcentaje_beneficio_real']
    porcentaje_beneficio_total = porcentaje_beneficio_total or 0
    porcentaje_beneficio_total = round(porcentaje_beneficio_total, 2)
    
    cuenta_inicial = Decimal(cuenta.cuenta) if cuenta.cuenta is not None else Decimal(0)
    comision = cuenta.comision
    swap = cuenta.swap

    capital_actual = 0

    if beneficio_total is not None:
        capital_actual += beneficio_total

    if comision is not None:
        capital_actual += comision

    if swap is not None:
        capital_actual += swap

    if isinstance(user, User):
        cuenta.user = user

    cuenta.capital_actual = cuenta_inicial + capital_actual
    cuenta.resultado_cuenta = cuenta.resultado_cuenta
    
    # if formulario.has_changed() and 'comision' in formulario.changed_data:
    #     messages.info(request, "Comisión ha sido actualizada.")

    # if formulario.has_changed() and 'swap' in formulario.changed_data:
    #     messages.info(request, "Swap ha sido actualizado.")

    # if formulario.has_changed() and 'resultado_cuenta' in formulario.changed_data:
    #     messages.info(request, "El resultado de su cuenta ha sido actualizado.")
    #     messages.get_messages(request).used = True
    
   
    cuenta.save()
    n_registros = trades.filter(
        resultado__in=[
            "Stop Loss",
            "Cierre Manual en Negativo",
        ]
    ).count()

    n_operaciones = cuenta.n_operaciones.strip() if cuenta.n_operaciones else ""
    o_restantes = int(n_operaciones) - n_registros if n_operaciones else 0

    exist_row = trades.count()
    
    if exist_row == 0:
        cuenta.comision = 0
        cuenta.swap = 0
        mensaje_error = "Agrega tu primer Trade!"
    cuenta.operaciones_restantes = o_restantes   
   
    if o_restantes == 1:  
        mensaje_error = f"Precaución: Ya tienes {abs(int(cuenta.n_operaciones)) - abs(int(o_restantes))} trades en stoploss, dale una vuelta a tu estrategia"
   
    elif o_restantes == 0:        
        mensaje_error = f"Precaución: Ya tienes {abs(int(cuenta.n_operaciones)) - abs(int(o_restantes))} trades en stoploss, Lo más probable hayas perdido tu challenge :("
   
    elif o_restantes < 0:        
        mensaje_error = f"Precaución: La cuenta se ha excedido con {abs(int(o_restantes))} trade en negativo. Lo más probable hayas perdido tu challenge :("
  
    trades_page = resolve(request.path_info).url_name
    context = {          
        "mensaje_error": mensaje_error,
        "cuentas": cuentas,
        "lista_trades_de_cuentas": trades,
        "lista_trades_eliminados": trades_eliminados,
        "exist_row": exist_row,
        "beneficio_total": beneficio_total,
        "porcentaje_beneficio_total": porcentaje_beneficio_total,
        "capital_actual": capital_actual,
        "formulario": formulario, 
        "id_tipo_cuenta": id_tipo_cuenta, 
        "o_restantes": o_restantes,
        "trades_page": trades_page,
        "id_cuenta":id_cuenta    
    }
    
    cuenta.save() 
    return render(request, "cuentas/trades/trades.html", context)

@csrf_protect
def crear_cuentas(request, id_tipo_cuenta):
    if not request.user.is_authenticated:
        return redirect("login")

    error_message = ""
    info_message = ""
    cuentas = CUENTAS.objects.all()
    user = request.user

    try:
        formulario = CuentaForm(request.POST or None, id_tipo_cuenta=id_tipo_cuenta, initial={'user': user, 'resultado_cuenta': 'En proceso'})

        if request.method == "POST" and formulario.is_valid():
            cuenta = formulario.save(commit=False)
            cuenta.id_tipo_cuenta_id = id_tipo_cuenta
            cuenta.riesgo_operacion = float(formulario.cleaned_data.get("riesgo_operacion"))
            cuenta.n_operaciones = formulario.cleaned_data.get("n_operaciones")
            cuenta.resultado_cuenta = "Ongoing"
        
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
                info_message = "Se ha agregado una nueva cuenta."
                cuenta.save()
                messages.info(request, info_message)
                url = reverse("lista_cuentas", args=[id_tipo_cuenta])
                return redirect(url)

            except Exception as e:
                error_message = f"Ocurrió un error al procesar los datos del formulario: {str(e)}"

    except Exception as e:
        error_message = f"Se produjo un error al crear la cuenta: {str(e)}"

    context = {
        "cuentas": cuentas,
        "formulario": formulario,
        "id_tipo_cuenta": id_tipo_cuenta,
        "error_message": error_message,
        "info_message": info_message,
        "user_value": str(user),
        
    }

    return render(request, "cuentas/crear_cuentas.html", context)
      
  
    


@csrf_protect
def eliminar_cuenta(request, id_cuenta, id_tipo_cuenta):
    """
    Vista para la página "eliminar_cuenta".
    """
    
    cuentas = CUENTAS.objects.get(id_cuenta=id_cuenta)
    cuentas.delete()
    delete_message = "Se ha eliminado una cuenta."             
    messages.info(request, delete_message)
    url = reverse(
        "lista_cuentas", args=[id_tipo_cuenta]
    )  # obtén la URL de la vista lista_de_trades
    return redirect(url)

# def handle_error(request, template_name, error_message):
#     cuentas = CUENTAS.objects.all()
#     context = {
#         "cuentas": cuentas,
#         "error_message": error_message,
#     }
#     return render(request, template_name, context)

def crear(request, id_cuenta):
    if not request.user.is_authenticated:
        return redirect("login")

    error_message = ""
    cuentas = CUENTAS.objects.all()

    try:
        cuenta = CUENTAS.objects.get(id_cuenta=id_cuenta)
        id_cuenta = cuenta.id_cuenta
        id_tipo_cuenta = cuenta.id_tipo_cuenta_id
        formulario = TradeForm(request.POST or None, request.FILES or None)

        if formulario.is_valid():
            trade = formulario.save(commit=False)
            trade.fecha_updated = timezone.now()
            trade.id_cuenta_id = id_cuenta
            trade.save()

            messages.info(request, "Se ha agregado un nuevo trade")
            return redirect("editar", trade.id)

    except ObjectDoesNotExist:
        error_message = "La cuenta no existe"
    except Exception as e:
        # Obtener los campos obligatorios del formulario
        campos_obligatorios = [field.label for field in formulario if field.required]
        campos_obligatorios_str = ", ".join(campos_obligatorios)
        error_message = f"Ocurrió un error al procesar los datos del formulario. Campos obligatorios: {campos_obligatorios_str}"

    context = {
        "cuentas": cuentas,
        "formulario": formulario,
        "id_cuenta": id_cuenta,
        "id_tipo_cuenta": id_tipo_cuenta,
        "error_message": error_message,
    }

    return render(request, "cuentas/trades/crear.html", context)


@csrf_protect
def editar(request, id):
    """
    Vista para la página "editar".
    """
    try:
        if not request.user.is_authenticated:
            return redirect("login")

        trade_id = id       
        trade = TRADES.objects.get(id=id)    
        # El formato desde forms se presenta al usuario dd-mm-YYYY pero por la vista se envia en formato YYYY-mm-dd
        trade_fecha_str = trade.fecha.strftime("%Y-%m-%d")
        trade.fecha = datetime.strptime(trade_fecha_str, "%Y-%m-%d").date() 
        estado  = trade.estado         
        cuentas = CUENTAS.objects.all()       
        id_cuenta = trade.id_cuenta_id   
        cuenta = CUENTAS.objects.get(id_cuenta=id_cuenta)
        id_tipo_cuenta = cuenta.id_tipo_cuenta_id
        filtra_trade_image = TRADEIMAGE.objects.filter(trade_id=id)
        recorre_clase_image = [(trade_image.image, trade_image) for trade_image in filtra_trade_image]

        formulario = TradeForm(request.POST, request.FILES, instance=trade)
      
        if request.method == "POST" and formulario.is_valid():         
          
            try:
                if request.FILES:
                    # Crea y guarda las imágenes y los datos ingresados en la base de datos
                    for image in request.FILES.getlist('image'):
                        titulo = request.POST.get('titulo')
                        descripcion = request.POST.get('descripcion')
                       
                        img = IMAGE.objects.create(image=image, titulo=titulo, descripcion=descripcion)
                       
                        new_trade_image = TRADEIMAGE(trade=trade, image=img)
                        new_trade_image.save()

                        username = request.user.username
                        user_folder = os.path.join('imagenes', slugify(username + str(request.user.id)), str(cuenta.n_login), str(trade.id))
                        os.makedirs(user_folder, exist_ok=True)
                        image_filename = os.path.join(user_folder, image.name)

                        if username == request.user.username:
                            with open(image_filename, 'wb') as file:
                                for chunk in image.chunks():
                                    file.write(chunk)

                        img.image = image_filename
                        img.save()

                for image, trade_image in recorre_clase_image:
                    titulo = request.POST.get(f'titulo_{trade_image.id}')
                    descripcion = request.POST.get(f'descripcion_{trade_image.id}')

                    if request.FILES.get(f'image_{trade_image.id}'):
                        image_file = request.FILES.get(f'image_{trade_image.id}')
                        default_storage.delete(trade_image.image.image.path)
                        username = request.user.username
                        user_folder = os.path.join('imagenes', slugify(username + str(request.user.id)), str(cuenta.n_login), str(trade.id))
                        os.makedirs(user_folder, exist_ok=True)
                        image_filename = os.path.join(user_folder, image_file.name)

                        if username == request.user.username:
                            with open(image_filename, 'wb') as file:
                                for chunk in image_file.chunks():
                                    file.write(chunk)
                        trade_image.image.image = image_filename

                    trade_image.image.titulo = titulo
                    trade_image.image.descripcion = descripcion
                    trade_image.image.save()   

                    

                # if cuenta.resultado_cuenta == 'Stop Loss':
                #     n_operaciones = cuenta.n_operaciones.strip()
                #     o_restantes = int(n_operaciones) - 1
                #     cuenta.operaciones_restantes = int(o_restantes)                    
                #     cuenta.save()                       

                trade.fecha_updated =  timezone.now()      
                trade.id_cuenta_id = id_cuenta
                trade = formulario.save()

                update_message = "Trade actualizado."
                messages.info(request, update_message)
                return redirect("editar", trade.id)

            except Exception as e:
                error_message = f"Se produjo un error al procesar los datos del formulario: {str(e)}"
        else:
            formulario = TradeForm(instance=trade)

        trade_image_count = len(recorre_clase_image)# Cuenta la cantidad de imagenes ingresadas
        mensajes = messages.get_messages(request)
        error_message = ""
        context = {
            "cuentas": cuentas,
            "formulario": formulario,
            "recorre_clase_image": recorre_clase_image,
            "error_message": error_message,
            "mensajes": mensajes,
            "trade_id": trade_id,
            "trade_fecha_str": trade_fecha_str,
            "estado": estado,
            "id_cuenta": id_cuenta,
            "id_tipo_cuenta": id_tipo_cuenta,
            "trade_image_count": trade_image_count   
        }

        return render(request, "cuentas/trades/editar.html", context)

    except Exception as e:
        error_message = f"Se produjo un error al procesar los datos del formulario: {str(e)}"

    context = {"error_message": error_message}
    return render(request, "cuentas/trades/editar.html", context)


@csrf_protect
def clonar(request, id):
    trade_original = TRADES.objects.get(id=id)
    id_cuenta = trade_original.id_cuenta_id

    # Clona el trade
    nuevo_trade = TRADES(
    activo=trade_original.activo,
    orden=trade_original.orden,
    fecha=trade_original.fecha,
    fecha_updated=timezone.now(),  # Puedes ajustar esto según tus necesidades
    resultado=trade_original.resultado,
    beneficio_real=trade_original.beneficio_real,
    porcentaje_beneficio_real=trade_original.porcentaje_beneficio_real,
    id_cuenta=trade_original.id_cuenta,
    stoploss=trade_original.stoploss,
    takeprofit=trade_original.takeprofit,
    lotaje=trade_original.lotaje,
    ratio=trade_original.ratio,
    beneficio_esperado=trade_original.beneficio_esperado,
    utilidad_proyectada=trade_original.utilidad_proyectada,
)
    nuevo_trade.save()

    # Clona las imágenes asociadas
    for trade_image in TRADEIMAGE.objects.filter(trade=trade_original):
        nueva_imagen = IMAGE(
            image=trade_image.image.image,  # Ajusta el campo según tu modelo IMAGE
            titulo=trade_image.image.titulo,
            descripcion=trade_image.image.descripcion,
        )
        nueva_imagen.save()

        nuevo_trade_image = TRADEIMAGE(trade=nuevo_trade, image=nueva_imagen)
        nuevo_trade_image.save()
        info_message = "Se ha clonao un trade"         
        messages.info(request, info_message)

    # Redirige a la página de edición del nuevo trade   
    return redirect("lista_trades_de_cuentas", id_cuenta=id_cuenta)

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
    delete_message = "Trade eliminado permanentemente."             
    messages.info(request, delete_message)
    # # Redirigir a la página lista_trades_de_cuentas
    # url = reverse("lista_trades_de_cuentas", args=[id_cuenta])  # obtén la URL de la vista lista_trades_de_cuentas
    # return redirect(url)  
    return redirect("lista_trades_de_cuentas", id_cuenta=id_cuenta)

def reciclar(request, id):
    trade = TRADES.objects.get(id=id)
    id_cuenta = trade.id_cuenta_id

    # Actualizar el estado del trade a "eliminado"
    trade.estado = 'eliminado'
    trade.save()

    reciclar_message = "Trade enviado a la papelera."
    messages.info(request, reciclar_message)

    return redirect("lista_trades_de_cuentas", id_cuenta=id_cuenta)

def restaurar(request, id):
    trade = TRADES.objects.get(id=id)
    id_cuenta = trade.id_cuenta_id

    # Actualizar el estado del trade a "eliminado"
    trade.estado = 'activo'
    trade.save()

    restaurar_message = "Trade restaurado"
    messages.info(request, restaurar_message)

    return redirect("trash", id_cuenta=id_cuenta)



def trash(request, id_cuenta):       
    if not request.user.is_authenticated:
        return redirect("login")   
    
    cuenta = CUENTAS.objects.get(id_cuenta=id_cuenta)
    cuentas = CUENTAS.objects.all()
    id_tipo_cuenta = cuenta.id_tipo_cuenta_id    
    lista_trades_eliminados = TRADES.objects.filter(id_cuenta=id_cuenta, estado='eliminado')   
    mensaje_error = ""    
    trash_page = resolve(request.path_info).url_name
    context = {          
        "mensaje_error": mensaje_error,
        "cuentas": cuentas,
        "lista_trades_eliminados": lista_trades_eliminados,
        "id_tipo_cuenta": id_tipo_cuenta,
        "trash_page": trash_page,
        "id_cuenta": id_cuenta 
    }

    return render(request, "cuentas/trades/trash.html", context)

def eliminar_imagen(request, image_id):
    """
    Elimina una imagen, título y descripción recientemente guardada.
    """
    try:
        image = IMAGE.objects.get(id=image_id)
        
        # Obtener la ruta de la carpeta padre de la imagen
        parent_folder = os.path.dirname(image.image.path)
        
        # Eliminar la imagen del sistema de archivos
        default_storage.delete(image.image.path)
        
        # Eliminar la imagen de la base de datos
        image.delete()
        
        # Eliminar la carpeta si está vacía
        if not os.listdir(parent_folder):
            shutil.rmtree(parent_folder)
        
        delete_message = "Se ha eliminado un registro de tu trade."             
        messages.info(request, delete_message)
    except ObjectDoesNotExist:
        pass
    
    # Redirigir al usuario a la página anterior
    return redirect(request.META.get('HTTP_REFERER', '/'))


def get_pip_value(base_currency, quote_currency):
    url = f"https://api.forexfeed.net/pip-value?symbol={base_currency}{quote_currency}&lotSize=100000"
    response = requests.get(url, timeout=10)  # Set the timeout value in seconds
    data = response.json()
    
    return JsonResponse(data)


@csrf_protect
def update_cell(request, id_tipo_cuenta, id_cuenta):
    if request.method == "POST":
        field_name = request.POST.get("field_name")
        field_value = request.POST.get("field_value")
        selected_option = request.POST.get("selected_option")

        try:
            # Busca el objeto en base a los parámetros de la URL
            cuenta = CUENTAS.objects.get(id_tipo_cuenta=id_tipo_cuenta, id_cuenta=id_cuenta)

            # Crea una instancia del formulario
            form = CuentaForm(instance=cuenta, id_tipo_cuenta=id_tipo_cuenta)

            # Actualiza los campos necesarios
            setattr(cuenta, field_name, field_value)
            setattr(cuenta, "resultado_cuenta", selected_option)

            # Guarda los cambios en la base de datos
            cuenta.save()

            # Devuelve una respuesta JSON indicando el resultado de la operación
            response_data = {
                "success": True,
                "message": "Cell updated successfully",
                "html": form.fields[field_name].widget.render(field_name, field_value),
            }
            return JsonResponse(response_data)
        except ObjectDoesNotExist:
            # Si el objeto no existe, devuelve un error
            response_data = {
                "success": False,
                "message": "Object does not exist",
            }
            return JsonResponse(response_data)

    # Si se accede por un método diferente a POST, devuelve un error
    response_data = {
        "success": False,
        "message": "Invalid request method",
    }
    return JsonResponse(response_data)


@csrf_protect
def editar_cuentas(request, id_tipo_cuenta, id_cuenta):
    """
    Vista para la página "editar_cuentas".
    """   
    cuentas = CUENTAS.objects.get(id_cuenta=id_cuenta)  
    formulario = CuentaForm(request.POST or None, id_tipo_cuenta=id_tipo_cuenta, instance=cuentas)
    error_message = ""
    context = {
        "formulario": formulario,
        "id_tipo_cuenta": id_tipo_cuenta,
        "error_message": error_message,
    }

    if formulario.is_valid() and request.method == "POST":       
        try:            
            formulario.save() 
           
            return redirect('cuentas')
        except Exception as e:
                    error_message = "Error {}".format(str(e))
    
    return render(request, "cuentas/editar_cuentas.html", context)

def crear_parciales(request):
    id_trade = request.session.get('id')
    formulario_p = ParcialesForm(request.POST or None, request.FILES or None)
    
    if request.method == 'POST' and formulario_p.is_valid():     
        parciales_obj = formulario_p.save()
        trade = TRADES.objects.get(id=id_trade)
        tradeparciales = TRADEPARCIALES(trade=trade, id_parciales=parciales_obj)
            
        tradeparciales.save()
        return redirect("editar", trade.id)
    
    context = {"formulario_p": formulario_p, "id_trade": id_trade}
    return render(request, "cuentas/trades/editar.html", context)

@csrf_protect
def gopro(request):
    """
    Vista para la página "paypal".
    """
    if not request.user.is_authenticated:
        return redirect("login")

    selected_plan = request.POST.get('plan', 'mensual')
    if selected_plan == 'mensual':
        # Código para el plan mensual
        amount = '5.95'
    elif selected_plan == 'anual':
        # Código para el plan anual
        amount = '3.95'
    else:
        # Plan no seleccionado o valor no válido, manejar el error adecuadamente
        return HttpResponse("Error: Plan no seleccionado o valor no válido.")

    host = request.get_host()
    paypal_dict = {
        'business': settings.PAYPAL_RECEIVER_EMAIL,
        'amount': amount,
        'item_name': 'Product 1',  # Puedes cambiar esto al nombre de tu producto
        'invoice': str(uuid.uuid4()),
        'currency_code': 'USD',  # Puedes cambiar esto a la moneda deseada
        'notify_url': f'http://{host}{reverse("paypal-ipn")}',
        'return': f'http://{host}{reverse("paypal-return")}',
        'cancel_return': f'http://{host}{reverse("paypal-cancel")}',
    }
    form = PayPalPaymentsForm(initial=paypal_dict)
    context = {'form': form, 'amount':amount}
    return render(request, "paginas/gopro.html", context)



def paypal_return(request):
    messages.success(request, '¡Bienvenido a Yorunal Up Pro!')
    return redirect('gopro')

def paypal_cancel(request):
    messages.warning(request, 'Tu orden ha sido cancelada, vuelve a intentarlo')
    return redirect('gopro')