from django.contrib import admin
from .models import Auto

@admin.register(Auto)
class AutoAdmin(admin.ModelAdmin):
    list_display = (
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
        'usuario'
    )
    ordering = (
        'marca', 
        'modelo', 
        'condicion', 
        'precio',
    )
    search_fields = (
        'marca', 
        'modelo', 
        'condicion',
        'tipo', 
        'combustible',
        'provincia', 
    )