from django.urls import path, include
from . import views
from paypal.standard.ipn import urls as paypal_urls
from django.conf import settings
from django.contrib.staticfiles.urls import static
from .views import register_view



urlpatterns = [
     # Otras URLs de tu proyecto...
  
    # path('', views.inicio, name='inicio'),
    # path('cuentas/', views.login, name='login'),     
    path('', views.custom_login, name='login'),   
    path('cuentas/logout/', views.logout_view, name='logout'),
    path('register/', register_view, name='register'),
    #CUENTAS
    path('cuentas/seleccionar_cuenta', views.seleccionar_cuenta, name='seleccionar_cuenta'),  
    path('cuentas/<int:id_tipo_cuenta>/', views.lista_cuentas, name='lista_cuentas'),
    path('cuentas/<int:id_tipo_cuenta>/crear_cuentas', views.crear_cuentas, name='crear_cuentas'),
    path('cuentas/<int:id_tipo_cuenta>/eliminar_cuenta/<int:id_cuenta>',views.eliminar_cuenta, name='eliminar_cuenta'), 
    path('cuentas/<int:id_tipo_cuenta>/update_cell/<int:id_cuenta>/', views.update_cell, name='update_cell'),
    path('cuentas/<int:id_tipo_cuenta>/editar_cuentas/<int:id_cuenta>/', views.editar_cuentas, name='editar_cuentas'), 

    #TRADES
    path('cuentas/<int:id_cuenta>/trades/', views.lista_trades_de_cuentas, name='lista_trades_de_cuentas'), 
    path('cuentas/trades/<int:id_cuenta>/crear/', views.crear, name='crear'),
    path('cuentas/trades/eliminar/<int:id>',views.eliminar, name='eliminar'), 
    path('cuentas/trades/reciclar/<int:id>',views.reciclar, name='reciclar'), 
    path('cuentas/trades/restaurar/<int:id>',views.restaurar, name='restaurar'), 
    path('cuentas/trades/editar/<int:id>', views.editar, name='editar'),      
    path('eliminar-imagen/<int:image_id>/', views.eliminar_imagen, name='eliminar_imagen'),
    path('cuentas/trades/clonar/<int:id>/', views.clonar, name='clonar'),    
    path('cuentas/<int:id_cuenta>/trash/', views.trash, name='trash'), 
     #PARCIALES
#     path('cuentas/trades/crear_parciales', views.crear_parciales, name='crear_parciales'),   
   #PAYMENTS
    path('gopro/', views.gopro, name='gopro'),
    path('paypal-return/', views.paypal_return, name='paypal-return'),
    path('paypal-cancel/', views.paypal_cancel, name='paypal-cancel'),    
#     path('paypal-ipn/', include(paypal_urls)),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
