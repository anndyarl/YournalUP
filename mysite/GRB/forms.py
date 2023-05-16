from django import forms
from django.forms.widgets import Select
from .models import TRADES, CUENTAS, IMAGE
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )


class TradeForm(forms.ModelForm):

    ACTIVO_CHOICES = (
        ('', '-----------'),
        ('EURUSD', 'EURUSD'),
        ('NZDUSD', 'NZDUSD'),
        ('AUDUSD', 'AUDUSD'),
    )
    ORDEN_CHOICES = (
        ('', '-----------'),
        ('Compra', 'Compra'),
        ('Venta', 'Venta'),
    )
    RESULTADO_CHOICES = (
        ('Programada', 'Programada'),
        ('Ejecución por Mercado', 'Ejecución por Mercado'),
        ('Take Profit', 'Take Profit'),
        ('Stop Loss', 'Stop Loss'),
        ('Break Even', 'Break Even'),
        ('Cierre Manual en Positivo', 'Cierre Manual en Positivo'),
        ('Cierre Manual en Negativo', 'Cierre Manual en Negativo')
    )



   
    activo = forms.ChoiceField(choices=ACTIVO_CHOICES, widget=Select())
    orden = forms.ChoiceField(choices=ORDEN_CHOICES, widget=Select(), required=False)   
    imagenes = forms.ImageField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    resultado = forms.ChoiceField(choices=RESULTADO_CHOICES, widget=Select(), required=False)
    beneficio_real = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)
    porcentaje_beneficio_real = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)
    id_cuenta = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

  
    class Meta:
        model = TRADES
        fields = '__all__'


class CuentaForm(forms.ModelForm):

    CUENTA_CHOICES = (
        ('', '-----------'),
        ('10000', '10.000'),
        ('25000', '25.000'),
        ('50000', '50.000'),
        ('100000', '100.000'),
        ('200000', '200.000'),
    )
    RIESGO_CHOICES = (
        ('', '-----------'),
        ('0.1', '0.1%'),
        ('0.2', '0.2%'),
        ('0.3', '0.3%'),
        ('0.4', '0.4%'),
        ('0.5', '0.5%'),
        ('1', '1%'),
        ('2', '2%'),
    )

    def __init__(self, *args, **kwargs):
        """
        Initializes the CuentaForm.

        Parameters:
        *args (tuple): Non-keyworded variable-length argument list.
        **kwargs (dict): Keyworded variable-length argument list.
        """
        id_tipo_cuenta = kwargs.pop('id_tipo_cuenta')
        # user_id = kwargs.pop('user_id')

        super().__init__(*args, **kwargs)
        if id_tipo_cuenta == 1:
            self.fields['cuenta'] = forms.ChoiceField(choices=self.CUENTA_CHOICES, widget=Select())
        else:
            self.fields['cuenta'] = forms.CharField(max_length=50, required=True)
        self.fields['riesgo_operacion'] = forms.ChoiceField(choices=self.RIESGO_CHOICES, widget=Select())

    comision = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    swap = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    user = forms.IntegerField(widget=forms.TextInput(attrs={"class": "form-control"})
)

    class Meta:
        """
        Meta class for CuentaForm.
        """
        model = CUENTAS
        fields = '__all__'



class ImageForm(forms.ModelForm):
          
    titulo = forms.CharField(required=False)
    descripcion = forms.CharField(required=False)

    class Meta:
        """
        Meta class for CuentaForm.
        """
        model = IMAGE
        fields = '__all__'


class TradeImageForm(forms.ModelForm):

    class Meta:
        """
        Meta class for CuentaForm.
        """
        model = IMAGE
        fields = '__all__'


