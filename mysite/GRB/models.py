"""
Este módulo contiene las definiciones de los modelos utilizados en la aplicación.
"""
from django.db import models
from django.contrib.auth.models import User


# class CustomUserManager(BaseUserManager):
#     def create_user(self, username, password=None):
#         if not username:
#             raise ValueError('Los usuarios deben tener un nombre de usuario válido')

#         user = self.model(username=username)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, username, password):
#         user = self.create_user(username=username, password=password)
#         user.is_admin = True
#         user.save(using=self._db)
#         return user

# class CustomUser(AbstractBaseUser):
#     username = models.CharField(max_length=30, unique=True)
#     is_admin = models.BooleanField(default=False)

#     objects = CustomUserManager()

#     USERNAME_FIELD = 'username'

#     def __str__(self):
#         return self.username


class TIPOCUENTA(models.Model):
    """
    clase Modelo "TIPOCUENTA".
    """

    id_tipo_cuenta = models.IntegerField(primary_key=True)
    descripcion = models.CharField(
        max_length=100, verbose_name="Descripción", null=True
    )

    objects = models.Manager()

    def __str__(self):
        fila = (
            "Id Tipo Cuenta: "
            + str(self.id_tipo_cuenta)
            + "descripcion: "
            + self.descripcion
        )
        return fila


class CUENTAS(models.Model):
    """
    clase Modelo "CUENTAS".
    """

    id_cuenta = models.AutoField(primary_key=True)
    cuenta = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Cuenta", null=True
    )
    n_operaciones = models.CharField(
        max_length=100, verbose_name="Número de Operaciones", null=True
    )
    operaciones_restantes = models.CharField(
        max_length=100, verbose_name="Operaciones restantes", null=True
    )
    capital_riesgo = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Capital riesgo", null=True
    )
    riesgo_operacion = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Riesgo por operación", null=True
    )
    nivel_riesgo = models.CharField(
        max_length=100, verbose_name="Nivel de riesgo", null=True
    )
    capital_actual = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Capital actual", null=True
    )
    n_login = models.CharField(max_length=100, verbose_name="Login", null=True)
    id_tipo_cuenta = models.ForeignKey(
        TIPOCUENTA, on_delete=models.CASCADE, verbose_name="Id tipo cuenta", null=True
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Id Usuario",
        null=True,
        related_name="cuentas",
    )
    fecha_cuenta = models.DateTimeField(
        auto_now_add=True, verbose_name="Fecha Cuenta", null=True
    )
    comision = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Comisión", null=True
    )
    swap =  models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Swap", null=True
    )
    # beneficio_total = models.CharField(
    #     max_length=100, verbose_name="Beneficio Total", null=True
    # )
    

    objects = models.Manager()

    def __str__(self):
        fila = (
            "Cuenta: "
            + str(self.cuenta)
            + "Número de Operaciones: "
            + self.n_operaciones
            + "Operaciones Restantes: "
            + self.operaciones_restantes
            + "Capital Riesgo: "
            + str(self.capital_riesgo)
            + "Riesgo por operación: "
            + str(self.riesgo_operacion)
            + ", Nivel de Riesgo: "
            + self.nivel_riesgo
            + "Capital Actual: "
            + str(self.capital_actual)
            + "Usuario: "
            + str(self.user)          
            + "Comisión: "
            + str(self.comision)
            + "Swap "
            + str(self.swap)
        )
        return fila


class IMAGE(models.Model):
    """
    clase Modelo "IMAGE".
    """

    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to="imagenes/", verbose_name="Imagen", null=True)
    titulo = models.CharField(max_length=50, verbose_name="Titulo", null=True)
    descripcion = models.CharField(
        max_length=1000, verbose_name="Ingresa un Descripción", null=True
    )

    objects = models.Manager()

    def __str__(self):
        fila = "titulo: " + self.titulo + "descripcion: " + self.descripcion
        return fila

    def delete(self, using=None, keep_parents=False):
        self.image.storage.delete(self.image.name)
        super().delete()


# Create your models here.
class TRADES(models.Model):
    """
    clase Modelo "TRADES".
    """

    id = models.AutoField(primary_key=True)
    id_cuenta = models.ForeignKey(
        CUENTAS, on_delete=models.CASCADE, verbose_name="Id Cuenta", null=True
    )
    activo = models.CharField(max_length=100, verbose_name="Activo", null=True)
    orden = models.CharField(max_length=100, verbose_name="Orden", null=True)
    stoploss = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Stoploss", null=True
    )
    takeprofit = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Takeprofit", null=True
    )
    lotaje = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Lotaje", null=True
    )
    ratio = models.CharField(max_length=100, verbose_name="Ratio", null=True)
    beneficio_esperado = models.CharField(
        max_length=100, verbose_name="Beneficio esperado", null=True
    )
    utilidad_proyectada = models.CharField(
        max_length=100, verbose_name="Utilidad proyectada", null=True
    )
    resultado = models.CharField(max_length=100, verbose_name="Resultado", null=True)
    fecha = models.DateTimeField(max_length=10, verbose_name="Fecha", null=True)
    beneficio_real = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Beneficio Real", null=True
    )    
    porcentaje_beneficio_real = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Beneficio Real", null=True
    )   
    # imagenes = models.ManyToManyField(Image, blank=True, verbose_name="Imágenes", through='TradeImage', null=True)
    
    objects = models.Manager()

    def __str__(self):
        fila = (
            "activo: "
            + self.activo
            + "orden: "
            + self.orden
            + "stoploss: "
            + str(self.stoploss)
            + "takeprofit: "
            + str(self.takeprofit)
            + "lotaje: "
            + str(self.lotaje)
            + "ratio: "
            + self.ratio
            + "BeneficioEsperado: "
            + self.beneficio_esperado
            + "UtilidadProyectada: "
            + self.utilidad_proyectada
            + "Resultado: "
            + self.resultado
            + "Beneficio real: "
            + str(self.beneficio_real)
            + "porcentaje beneficio real: "
            + str(self.porcentaje_beneficio_real)        
        )
        return fila


class TRADEIMAGE(models.Model):
    """
    clase Modelo "TRADEIMAGE".
    """

    trade = models.ForeignKey(TRADES, on_delete=models.CASCADE)
    image = models.ForeignKey(IMAGE, on_delete=models.CASCADE)

    objects = models.Manager()

    def __str__(self):
        fila = "Trade: " + str(self.trade) + " - Imagen: " + str(self.image)
        return fila

    # image = models.ManyToManyField(Trades, blank=True, verbose_name="Imágenes")
    # titulo = models.CharField(max_length=50, verbose_name="Titulo", null=True)
    # comentario = models.CharField(max_length=1000, verbose_name="Comentario", null=True)

    # def __str__(self):
    #     fila = "titulo: " + self.titulo +  "comnetario: " + self.comentario
    #     return fila

    # def delete(self, using=None, keep_parents=False):
    #     for image in self.imagenes.all():
    #         image.delete()
    #     super().delete(using=using, keep_parents=keep_parents)
