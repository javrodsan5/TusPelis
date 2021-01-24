#encoding:utf-8

from django.db import models

class Actor(models.Model):
    nombre = models.TextField(verbose_name='Nombre', unique=True)
    linkActor = models.TextField(verbose_name='Link actor')
    fechaNacimiento = models.TextField(verbose_name='Fecha de nacimiento')
    lugarNacimiento = models.TextField(verbose_name='Lugar de nacimiento')
    foto = models.ImageField(verbose_name='Foto')
    biografia = models.TextField(verbose_name='Biografia')
      
    def __str__(self):
        return self.nombre 

class Genero(models.Model):
    nombre = models.TextField(verbose_name='Genero', unique=True)

    def __str__(self):
        return self.nombre 

class Personal(models.Model):
    nombre = models.TextField(verbose_name='Personal', unique=True)
    puesto = models.TextField(verbose_name='Puesto', default='productor')

    def __str__(self):
        return self.nombre 

class Pelicula(models.Model):
    titulo = models.TextField(verbose_name='Titulo', unique=True)
    sinopsis = models.TextField(verbose_name='Sinopsis')
    actores = models.ManyToManyField(Actor)
    personal = models.ManyToManyField(Personal)
    duracion = models.TextField(verbose_name='Duracion')
    generos = models.ManyToManyField(Genero)
    linkPelicula = models.TextField(verbose_name='Link de la pelicula')
    portada = models.ImageField(verbose_name='Portada')

      
    def __str__(self):
        return self.titulo 