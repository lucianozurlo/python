from django.urls import path
from accounts import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.login_request, name="IniciarSesion"),
    path('logout/', LogoutView.as_view(template_name="accounts/logout.html"), name='CerrarSesion'),
    path('nuevo-usuario/', views.nuevo_usuario, name="NuevoUsuario"),
    path('mi-perfil/', views.mi_perfil, name="MiPerfil"),
    path('mi-contrasena/', views.MiContrasena.as_view(), name="MiContrasena"),
]