from django.urls import path
from . import views

urlpatterns = [
    path('', views.buscarAutos, name="Home"),
    path('crear-publicacion/', views.AutoCreateView.as_view(), name="CrearPublicacion"),
    path('listado-autos/', views.AutoListView.as_view(), name="ListadoAutos"),
    path('publicacion/<int:pk>/', views.AutoDetailView.as_view(), name="DetalleAuto"),
    path('editar-publicacion/<int:pk>/', views.AutoUpdateView.as_view(), name="EditarPublicacion"),
    path('borrar-publicacion/<int:pk>/', views.AutoDeleteView.as_view(), name="BorrarPublicacion"),
    path('like/<int:auto_id>/', views.LikeAutoView.as_view(), name='like'),
    path('nuevo-comentario/<int:auto_id>/', views.NuevoComentarioView.as_view(), name='NuevoComentario'),
    path('vendedores/', views.Vendedores.as_view(), name='Vendedores'),
    path('mis-publicaciones/', views.MisPublicacionesView.as_view(), name='MisPublicaciones'),
    path('about-me/', views.AboutMe, name='AboutMe')
]
