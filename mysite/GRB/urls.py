from django.urls import path
from . import views
from django.conf import settings
from django.contrib.staticfiles.urls import static



urlpatterns = [
     # Otras URLs de tu proyecto...
  
    # path('', views.inicio, name='inicio'),
    # path('cuentas/', views.login, name='login'), 
    path('', views.custom_login, name='login'),
    path('cuentas/logout/', views.logout_view, name='logout'),  
    path('cuentas/seleccionar_cuenta', views.seleccionar_cuenta, name='seleccionar_cuenta'),

    path('cuentas/<int:id_tipo_cuenta>/', views.lista_cuentas, name='lista_cuentas'),
    path('cuentas/<int:id_tipo_cuenta>/crear_cuentas', views.crear_cuentas, name='crear_cuentas'),
    path('cuentas/<int:id_cuenta>/trades/', views.lista_trades_de_cuentas, name='lista_trades_de_cuentas'), # views.lista_trades_de_cuentas se va a buscar la clase en views.py y name='lista_trades_de_cuentas' se utiliza para el redireccionamiento en los html con href
    # path('cuentas/editar_cuentas/<int:id_cuenta>', views.editar_cuentas, name='editar_cuentas'),  
    path('cuentas/<int:id_tipo_cuenta>/eliminar_cuenta/<int:id_cuenta>',views.eliminar_cuenta, name='eliminar_cuenta'), 


    path('cuentas/trades/crear/', views.crear, name='crear'),
    path('cuentas/trades/editar/<int:id>', views.editar, name='editar'),  
    path('cuentas/eliminar/<int:id>',views.eliminar, name='eliminar'),  
    path('eliminar-imagen/<int:image_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    # path('cuentas/<int:id_cuenta>/trades/', views.editar_cuentas_beneficios_totales, name='editar_cuentas_beneficios_totales'),  

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
