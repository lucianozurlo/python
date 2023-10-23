from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Auto(models.Model):
    marca = models.CharField(max_length=30)
    modelo = models.CharField(max_length=50)
    condicion = models.CharField(max_length=20)
    precio = models.PositiveIntegerField()
    precioNegociable = models.BooleanField(default=True)
    anio = models.PositiveIntegerField()
    km = models.PositiveIntegerField()
    tipo = models.CharField(max_length=20)
    combustible = models.CharField(max_length=20)
    motor = models.CharField(max_length=30, blank=True)
    transmision = models.CharField(max_length=20)
    color = models.CharField(max_length=30, blank=True)
    descripcion = models.TextField(blank=True)
    cuerpo = models.TextField(blank=True)
    localidad = models.CharField(max_length=20, blank=True)
    provincia = models.CharField(max_length=20)
    imagen = models.ImageField(upload_to='autos/', blank=True, default=settings.DEFAULT_CAR)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(default=timezone.now)
    likes = models.ManyToManyField(User, related_name='auto_likes', blank=True)

    MARCA_CHOICES = (
        ('AC', 'AC'),
        ('Alfa Romeo', 'Alfa Romeo'),
        ('Aston Martin', 'Aston Martin'),
        ('Audi', 'Audi'),
        ('BMW', 'BMW'),
        ('Chevrolet', 'Chevrolet'),
        ('Citroën', 'Citroën'),
        ('Dodge', 'Dodge'),
        ('Ferrari', 'Ferrari'),
        ('Ford', 'Ford'),
        ('GMC', 'GMC'),
        ('Honda', 'Honda'),
        ('Hyundai', 'Hyundai'),
        ('Jeep', 'Jeep'),
        ('Kia', 'Kia'),
        ('Lamborghini', 'Lamborghini'),
        ('Lexus', 'Lexus'),
        ('Mercedes-Benz', 'Mercedes-Benz'),
        ('Mini', 'Mini'),
        ('Nissan', 'Nissan'),
        ('Peugeot', 'Peugeot'),
        ('Porsche', 'Porsche'),
        ('Renault', 'Renault'),
        ('Seat', 'Seat'),
        ('Toyota', 'Toyota'),
        ('Volkswagen', 'Volkswagen'),
        ('Volvo', 'Volvo')
    )

    CONDICION_CHOICES = (
        ('Nuevo', 'Nuevo'),
        ('Usado', 'Usado')
    )

    RANGO_DE_ANIOS = [(str(anio), str(anio)) for anio in range(2023, 1899, -1)]

    TIPO_CHOICES = (
        ('Sedán', 'Sedán'),
        ('SUV', 'SUV'),
        ('Wagon', 'Wagon'),
        ('Crossover', 'Crossover'),
        ('Coupé', 'Coupé'),
        ('Pickup', 'Pickup'),
        ('Sport Coupé', 'Sport Coupé'),
        ('Compacto', 'Compacto'),
        ('Convertible', 'Convertible'),
        ('Familiar MPV', 'Familiar MPV')
    )

    COMBUSTIBLE_CHOICES = (
        ('Diesel', 'Diesel'),
        ('Eléctrico', 'Eléctrico'),
        ('Hibrido', 'Hibrido'),
        ('Nafta', 'Nafta')
    )

    TRANSMISION_CHOICES = (
        ('Automática', 'Automática'),
        ('manual', 'Manual'),
    )

    PROVINCIA_CHOICES = [
        ('Buenos Aires', 'Buenos Aires'),
        ('CABA', 'CABA'),
        ('Catamarca', 'Catamarca'),
        ('Chaco', 'Chaco'),
        ('Chubut', 'Chubut'),
        ('Córdoba', 'Córdoba'),
        ('Corrientes', 'Corrientes'),
        ('Entre Ríos', 'Entre Ríos'),
        ('Formosa', 'Formosa'),
        ('Jujuy', 'Jujuy'),
        ('La Pampa', 'La Pampa'),
        ('La Rioja', 'La Rioja'),
        ('Mendoza', 'Mendoza'),
        ('Misiones', 'Misiones'),
        ('Neuquén', 'Neuquén'),
        ('Río Negro', 'Río Negro'),
        ('Salta', 'Salta'),
        ('San Juan', 'San Juan'),
        ('San Luis', 'San Luis'),
        ('Santa Cruz', 'Santa Cruz'),
        ('Santa Fe', 'Santa Fe'),
        ('Santiago del Estero', 'Santiago del Estero'),
        ('Tierra del Fuego', 'Tierra del Fuego'),
        ('Tucumán', 'Tucumán')
    ]

    def __str__(self):
        return self.marca
        
    def save(self, *args, **kwargs):
        if not self.imagen:
            self.imagen = settings.DEFAULT_CAR
        super(Auto, self).save(*args, **kwargs)

class Comentario(models.Model):
    auto = models.ForeignKey(Auto, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    fecha_publicacion = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.auto.marca}'
