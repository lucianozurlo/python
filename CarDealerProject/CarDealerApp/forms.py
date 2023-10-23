from django import forms
from .models import Auto

class AutoForm(forms.ModelForm):
    class Meta:
        model = Auto
        fields = [
            'id', 
            'marca', 
            'modelo', 
            'condicion', 
            'precio', 
            'precioNegociable', 
            'anio', 
            'km', 
            'tipo', 
            'combustible', 
            'motor', 
            'transmision', 
            'color', 
            'descripcion', 
            'cuerpo', 
            'localidad', 
            'provincia', 
            'imagen', 
        ]

    # Defino widgets con clases CSS para cada campo
    marca = forms.ChoiceField(
        choices=Auto.MARCA_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Marca')
    modelo = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Modelo')
    condicion = forms.ChoiceField(
        choices=Auto.CONDICION_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Condición')
    precio = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-light w-100 me-2 mb-2'}),
        label='Precio (en u$s)')
    precioNegociable = forms.BooleanField(
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input mt-1 mb-4'}),
        label='Precio negociable', required=False)
    anio = forms.ChoiceField(
        choices=Auto.RANGO_DE_ANIOS, 
        required=True,
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Año')
    km = forms.DecimalField(
        widget=forms.NumberInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Kilometraje')
    tipo = forms.ChoiceField(
        choices=Auto.TIPO_CHOICES, required=True, 
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Tipo')
    combustible = forms.ChoiceField(
        choices=Auto.COMBUSTIBLE_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Combustible')
    motor = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Motor', required=False)
    transmision = forms.ChoiceField(
        choices=Auto.TRANSMISION_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Transmisión')
    color = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Color', required=False)
    descripcion = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Descripcion', required=False)
    cuerpo = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Cuerpo', required=False)
    localidad = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Localidad')
    provincia = forms.ChoiceField(
        choices=Auto.PROVINCIA_CHOICES, 
        required=True, 
        widget=forms.Select(attrs={'class': 'form-select form-select-light mt-2 mb-3'}),
        label='Provincia')
    imagen = forms.ImageField(
        widget=forms.FileInput(attrs={'class': 'form-control form-control-light mt-2 mb-3'}),
        label='Foto', required=False)


class FormBuscarAutos(forms.Form):
    marca = forms.ChoiceField(
        choices=[('', '--- Buscá marca ---')] + list(Auto.MARCA_CHOICES),
        widget=forms.Select(attrs={'class': 'btn btn-link dropdown-toggle ps-2 ps-sm-3'}),
        required=False)
    modelo = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Modelo: (ej: Bora)','class': 'form-control'}), required=False)
    condicion = forms.ChoiceField(
        choices=[('', '--- Buscá condición ---')] + list(Auto.CONDICION_CHOICES),
        widget=forms.Select(attrs={'class': 'btn btn-link dropdown-toggle ps-2 ps-sm-3'}),
        required=False)
    tipo = forms.ChoiceField(
        choices=[('', '--- Buscá tipo ---')] + list(Auto.TIPO_CHOICES),
        widget=forms.Select(attrs={'class': 'btn btn-link dropdown-toggle ps-2 ps-sm-3'}),
        required=False)
