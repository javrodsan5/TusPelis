from django.contrib import admin
from django.urls import path
from main import views, populate

urlpatterns = [
    path('', views.inicio),
    path('cargarBD/', populate.carga),
    path('cargarWhoosh/', populate.cargaWhoosh),
    path('peliculas/', views.list_peliculas),
    path('detallesPelicula/<int:id>', views.detallesPelicula),
    path('actores/', views.list_actores),
    path('detallesActor/<int:id>', views.detallesActor),
    path('generos/', views.list_generos),
    path('personal/', views.list_personal),
    path('peliculasPorActor/', views.pelicula_por_actor),
    path('peliculasPorGenero/', views.pelicula_por_genero),

    ]
