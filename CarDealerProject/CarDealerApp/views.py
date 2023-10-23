from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Auto, Comentario
from .forms import *


class AutoCreateView(LoginRequiredMixin, CreateView):
    model = Auto
    template_name = 'CarDealerApp/AutoCreateView.html'
    success_url = reverse_lazy('ListadoAutos')

    def get_form_class(self):
        return AutoForm

    def form_valid(self, form):
        form.instance.usuario_id = self.request.user.id

        if 'imagen' in self.request.FILES:
            form.instance.imagen = self.request.FILES['imagen']

        return super().form_valid(form)
    
class AutoListView(ListView):
    model = Auto
    template_name = 'CarDealerApp/AutoListView.html'
    context_object_name = 'autos'

    def get_queryset(self):
        return Auto.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['no_autos'] = not self.get_queryset().exists()
        return context

class AutoDetailView(LoginRequiredMixin, DetailView):
    model = Auto
    template_name = 'CarDealerApp/AutoDetailView.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comentarios'] = Comentario.objects.filter(auto=self.object)
        return context

class CustomUserPassesTestMixin(UserPassesTestMixin):
    def handle_no_permission(self):
        if self.raise_exception:
            return HttpResponseForbidden()
        else:
            return redirect_to_login(self.request.get_full_path())

class AutoUpdateView(CustomUserPassesTestMixin, UpdateView):
    model = Auto
    template_name = 'CarDealerApp/AutoUpdateView.html'
    success_url = reverse_lazy('ListadoAutos')
    form_class = AutoForm 

    def get_form(self, form_class=None):
        form = super().get_form(form_class)

        form.fields['marca'].choices = Auto.MARCA_CHOICES
        form.fields['condicion'].choices = Auto.CONDICION_CHOICES
        form.fields['anio'].choices = Auto.RANGO_DE_ANIOS
        form.fields['tipo'].choices = Auto.TIPO_CHOICES
        form.fields['combustible'].choices = Auto.COMBUSTIBLE_CHOICES
        form.fields['transmision'].choices = Auto.TRANSMISION_CHOICES
        form.fields['provincia'].choices = Auto.PROVINCIA_CHOICES

        return form

    def test_func(self):
        # Se fija si el usuario es el creador del Auto o un superusuario
        auto = get_object_or_404(Auto, pk=self.kwargs['pk'])
        
        return self.request.user == auto.usuario or self.request.user.is_superuser


class AutoDeleteView(CustomUserPassesTestMixin, DeleteView):
    model = Auto
    template_name = 'CarDealerApp/AutoDeleteView.html'
    success_url = reverse_lazy('ListadoAutos')

    def test_func(self):
        auto = get_object_or_404(Auto, pk=self.kwargs['pk'])
        
        return self.request.user == auto.usuario or self.request.user.is_superuser

class LikeAutoView(LoginRequiredMixin, View):
    def post(self, request, auto_id):
        auto = Auto.objects.get(pk=auto_id)
        user = self.request.user 

        if user in auto.likes.all():
            auto.likes.remove(user)
        else:
            auto.likes.add(user)

        auto.save()

        return redirect(request.META.get('HTTP_REFERER'))

class NuevoComentarioView(LoginRequiredMixin, View):
    def post(self, request, auto_id):
        auto = Auto.objects.get(pk=auto_id)
        
        texto = request.POST.get('texto')
        if texto:
            comentario = Comentario(auto=auto, autor=request.user, texto=texto)
            comentario.save()
        
        return redirect('DetalleAuto', pk=auto_id)

class Vendedores(LoginRequiredMixin, View):
    def get(self, request):
        autos = Auto.objects.all()

        # Crea un diccionario para almacenar usuarios y sus autos
        vendedores = {}

        for auto in autos:
            usuario = auto.usuario

            # Si el usuario ya está en el diccionario, agrega el auto a su lista
            if usuario in vendedores:
                vendedores[usuario].append(auto)
            else:
                # Si el usuario no está en el diccionario, crea una nueva lista con el Auto
                vendedores[usuario] = [auto]

        return render(request, 'CarDealerApp/VendedoresView.html', {'vendedores': vendedores})

class MisPublicacionesView(LoginRequiredMixin, View):
    def get(self, request):
        mis_publicaciones = Auto.objects.filter(usuario=self.request.user)

        if mis_publicaciones.exists():
            return render(request, 'CarDealerApp/MisPublicacionesView.html', {'mis_publicaciones': mis_publicaciones})
        else:
            mensaje = "Todavía no publicaste nada."
            return render(request, 'CarDealerApp/MisPublicacionesView.html', {'mensaje': mensaje})

#Buscadores (filtros)
def buscarAutos(request):
    autos = []

    if request.method == 'POST':
        formBuscar = FormBuscarAutos(request.POST)

        if formBuscar.is_valid():
            datos = formBuscar.cleaned_data
            marca = datos.get("marca", "")
            modelo = datos.get("modelo", "")
            combustible = datos.get("combustible", "")
            condicion = datos.get("condicion", "")
            tipo = datos.get("tipo", "")
            provincia = datos.get("provincia", "")

            autos = Auto.objects.all()

            if marca:
                autos = autos.filter(marca=marca)
            if modelo:
                autos = autos.filter(modelo__icontains=modelo)
            if combustible:
                autos = autos.filter(combustible=combustible)
            if condicion:
                autos = autos.filter(condicion=condicion)
            if tipo:
                autos = autos.filter(tipo=tipo)
            if provincia:
                autos = autos.filter(provincia=provincia)

            return render(request, 'CarDealerApp/ResultadosBusqueda.html', {"autos": autos})

    else:
        formBuscar = FormBuscarAutos()

    return render(request, 'CarDealerApp/index.html', {"formBuscar": formBuscar, "autos": autos})

def AboutMe (request):
    return render(request, 'CarDealerApp/AboutMe.html')