from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.urls import reverse_lazy
from .forms import LoginForm, UserEditForm, UserRegisterForm, ChangePasswordForm
from .models import Avatar


def login_request(request):
    mensaje = ""

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        # Elimina todos los mensajes existentes
        for message in messages.get_messages(request):
            message.delete()

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f"Hola {username}!")
                return redirect('Home')
            else:
                form = LoginForm()
                messages.error(request, "Usuario o contraseña incorrectos")
                return render(request, "accounts/login.html", {"form": form})

        messages.error(request, "Usuario o contraseña incorrectos")

    form = LoginForm()
    return render(request, 'accounts/login.html', {"form": form})

def nuevo_usuario(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST, request.FILES)

        for message in messages.get_messages(request):
            message.delete()

        if form.is_valid():
            user_info = form.cleaned_data['username']
            form.save()

            avatar_image = form.cleaned_data.get('avatar', None)
            if not avatar_image:
                avatar_image = settings.DEFAULT_AVATAR

            # Intenta obtener o crear un objeto Avatar para el usuario
            try:
                avatar = Avatar.objects.get(user=form.instance)
            except Avatar.DoesNotExist:
                avatar = Avatar(user=form.instance, avatar=avatar_image)
            else:
                avatar.avatar = avatar_image
            avatar.save()

            messages.success(request, f"Nuevo usuario: {user_info}")

            return redirect('Home')

        messages.error(request, "Hubo un error al registrar el usuario")

    else:
        form = UserRegisterForm()

    return render(request, "accounts/nuevo-usuario.html", {"form": form})

@login_required
def mi_perfil(request):
    if request.method == "POST":
        form = UserEditForm(request.POST, request.FILES)
        
        if form.is_valid():
            user = request.user

            user.email = form.cleaned_data['email']
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']

            # Verificar si se ingresa un nuevo avatar
            if 'avatar' in request.FILES:
                # Si se ingresa un nuevo avatar, lo actualiza
                user.avatar.avatar = request.FILES['avatar']

            user.avatar.save()
            user.save()

            # Actualiza el valor de avatar_image en el contexto
            avatar_image = user.avatar.avatar.url if user.avatar.avatar else settings.DEFAULT_AVATAR

            return redirect('MiPerfil')

    else:
        avatar_image = request.user.avatar.avatar.url if request.user.avatar.avatar else settings.DEFAULT_AVATAR
        form = UserEditForm(
            initial={
                'email': request.user.email,
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
            }
        )

    return render(request, 'accounts/mi-perfil.html', {'form': form, 'avatar_image': avatar_image})

class MiContrasena(LoginRequiredMixin, View):
    template_name = "accounts/micontrasena.html"
    form_pass = ChangePasswordForm
    success_url = reverse_lazy("Inicio")

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_pass(user=request.user)})

    def post(self, request, *args, **kwargs):
        form = self.form_pass(request.user, request.POST)

        for message in messages.get_messages(request):
            message.delete()

        if form.is_valid():
            pass1 = form.cleaned_data.get("password1")
            pass2 = form.cleaned_data.get("password2")

            if pass1 == pass2:
                usuario = request.user
                usuario.set_password(pass1)
                usuario.save()
                # Vuelve a iniciar sesión con la nueva contraseña
                login(request, usuario)

                messages.success(request, f"Contraseña modificada con éxito.")
                return redirect('MiPerfil')

        return render(request, self.template_name, {"form": form})
