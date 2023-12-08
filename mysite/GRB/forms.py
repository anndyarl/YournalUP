from django import forms
from django.forms.widgets import Select
from .models import TRADES, CUENTAS, IMAGE, PARCIALES, TRADEPARCIALES
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
    ('AUDCAD', 'AUDCAD'),
    ('AUDCHF', 'AUDCHF'),
    ('AUDJPY', 'AUDJPY'),
    ('AUDNZD', 'AUDNZD'),
    ('AUDUSD', 'AUDUSD'),
    ('CADCHF', 'CADCHF'),
    ('CADJPY', 'CADJPY'),
    ('CHFJPY', 'CHFJPY'),
    ('EURAUD', 'EURAUD'),
    ('EURCAD', 'EURCAD'),
    ('EURCHF', 'EURCHF'),
    ('EURDKK', 'EURDKK'),
    ('EURGBP', 'EURGBP'),
    ('EURHKD', 'EURHKD'),
    ('EURJPY', 'EURJPY'),
    ('EURNOK', 'EURNOK'),
    ('EURNZD', 'EURNZD'),
    ('EURPLN', 'EURPLN'),
    ('EURSEK', 'EURSEK'),
    ('EURTRY', 'EURTRY'),
    ('EURUSD', 'EURUSD'),
    ('GBPAUD', 'GBPAUD'),
    ('GBPCAD', 'GBPCAD'),
    ('GBPCHF', 'GBPCHF'),
    ('GBPDKK', 'GBPDKK'),
    ('GBPJPY', 'GBPJPY'),
    ('GBPNZD', 'GBPNZD'),
    ('GBPPLN', 'GBPPLN'),
    ('GBPSEK', 'GBPSEK'),
    ('GBPUSD', 'GBPUSD'),
    ('NZDCAD', 'NZDCAD'),
    ('NZDCHF', 'NZDCHF'),
    ('NZDJPY', 'NZDJPY'),
    ('NZDUSD', 'NZDUSD'),
    ('USDCAD', 'USDCAD'),
    ('USDCHF', 'USDCHF'),
    ('USDCZK', 'USDCZK'),
    ('USDDKK', 'USDDKK'),
    ('USDHKD', 'USDHKD'),
    ('USDHUF', 'USDHUF'),
    ('USDJPY', 'USDJPY'),
    ('USDMXN', 'USDMXN'),
    ('USDNOK', 'USDNOK'),
    ('USDPLN', 'USDPLN'),
    ('USDSEK', 'USDSEK'),
    ('USDSGD', 'USDSGD'),
    ('USDTRY', 'USDTRY'),
    ('USDZAR', 'USDZAR'),
    ('XAGUSD', 'XAGUSD'),
    ('XAUUSD', 'XAUUSD'),
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
    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), input_formats=['%d-%m-%Y'])# Este formato se muestra al usuario
    fecha_updated = forms.DateTimeField(required=False, widget=forms.HiddenInput())
    resultado = forms.ChoiceField(choices=RESULTADO_CHOICES, widget=Select(), required=False)
    beneficio_real = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)
    porcentaje_beneficio_real = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)
    id_cuenta = forms.IntegerField(required=False, widget=forms.TextInput(attrs={"class": "form-control"}))

  
    class Meta:
        model = TRADES
        # fields = '__all__'
        exclude = ['estado']


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
        ('0.4', '0.4%'),
        ('0.5', '0.5%'),
        ('1', '1%'),
        ('2', '2%'),
    )

    BROKER_CHOICES = (
    ('', '-----------'),
    ('FTMO', 'FTMO'),
    ('LITEFINANCE', 'LITEFINANCE'),
    ('ICMARKETS', 'ICMARKETS'),
    ('eToro', 'eToro'),
    ('Plus500', 'Plus500'),
    ('AvaTrade', 'AvaTrade'),
    ('XM', 'XM'),
    ('Interactive Brokers', 'Interactive Brokers'),
    ('TD Ameritrade', 'TD Ameritrade'),
    ('OANDA', 'OANDA'),
    ('FXCM', 'FXCM'),
    ('Pepperstone', 'Pepperstone'),
    ('Alpari', 'Alpari'),
    ('FBS', 'FBS'),
    ('HotForex', 'HotForex'),
    ('OctaFX', 'OctaFX'),
    ('RoboForex', 'RoboForex'),
    ('Binance', 'Binance'),
    ('BitMEX', 'BitMEX'),
    ('Bitfinex', 'Bitfinex'),
    ('Kraken', 'Kraken'),
    ('Coinbase', 'Coinbase'),
    ('XM', 'XM'),
    ('Libertex', 'Libertex'),
    ('EXXNESS', 'EXXNESS'),
    ('Otro', 'Otro'),

    )   
    RESULTADO_CUENTA_CHOICES = (      
        ('Ongoing', 'Ongoing'),
        ('Repeat', 'Repeat'),     
        ('Passed', 'Passed'),
        ('Not passed', 'Not passed'),       
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
            self.fields['cuenta'] = forms.ChoiceField(choices=self.CUENTA_CHOICES, widget=Select(), required=True)
            self.fields['riesgo_operacion'] = forms.ChoiceField(choices=self.RIESGO_CHOICES, widget=Select(), required=True)
        else:
            self.fields['cuenta'] = forms.DecimalField(max_digits=10, decimal_places=2, required=True)     
            self.fields['riesgo_operacion'] = forms.DecimalField(max_digits=2, decimal_places=1, required=True)   

        
        # self.fields['user'].required = True
        # self.fields['id_tipo_cuenta'].required = True
         
    broker = forms.ChoiceField(choices=BROKER_CHOICES, widget=forms.Select(), required=True)
    otro_broker = forms.CharField(max_length=100, required=False)  # Agrega este campo 
    comision = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    swap = forms.DecimalField(max_digits=10, decimal_places=2, required=False)
    resultado_cuenta = forms.ChoiceField(choices=RESULTADO_CUENTA_CHOICES, widget=forms.Select(), required=False)
    n_login = forms.CharField(max_length=12, required=True)  # Agrega este campo  

    def clean(self):
        cleaned_data = super().clean()
        selected_broker = cleaned_data.get('broker')
        otro_broker = cleaned_data.get('otro_broker')     
       
        if selected_broker == 'Otro' and not otro_broker:
            self.add_error('otro_broker', 'Por favor, ingresa el nombre del otro broker.')
        elif otro_broker:
            cleaned_data['broker'] = otro_broker 

        return cleaned_data


    class Meta:
        """
        Meta class for CuentaForm.
        """
        model = CUENTAS
        # fields = '__all__'
        exclude = ['operaciones_restantes', 'nivel_riesgo', 'capital_actual', 'id_tipo_cuenta','user']


class ImageForm(forms.ModelForm):
          
    titulo = forms.CharField(required=False)
    descripcion = forms.CharField(required=False)
    image = forms.ImageField(required=False)  
    class Meta:
        """
        Meta class for ImageForm.
        """
        model = IMAGE
        fields = '__all__'
        widgets = {
            'image': forms.ClearableFileInput(attrs={'multiple': True}),
        }



class ParcialesForm(forms.ModelForm):
          
    parciales = forms.DecimalField(max_digits=10, decimal_places=2, required=False, initial=0)
    class Meta:
        """
        Meta class for ImageForm.
        """
        model = PARCIALES
        fields = '__all__'


