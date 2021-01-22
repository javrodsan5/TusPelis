#encoding:utf-8
from django import forms

GENEROS = [
    ('Aventura', 'Aventura'), ('Acción', 'Acción'), ('Fantasía', 'Fantasía'), ('Ciencia ficción', 'Ciencia ficción'), ('Crimen', 'Crimen'), ('Familia', 'Familia'),
    ('Animación', 'Animación'), ('Comedia', 'Comedia'), ('Historia', 'Historia'), ('Terror', 'Terror'), ('Suspense', 'Suspense'), ('Bélica', 'Bélica'),
    ('Drama', 'Drama'), ('Misterio', 'Misterio'), ('Música', 'Música'), ('Romance', 'Romance')]

GENEROSID = [
    ('Aventura', 'Aventura'), ('Acción', 'Acción'), ('Fantasía', 'Fantasía'), ('Ciencia ficción', 'Ciencia ficción'), ('Crimen', 'Crimen'), ('Familia', 'Familia'),
    ('Animación', 'Animación'), ('Comedia', 'Comedia'), ('Historia', 'Historia'), ('Terror', 'Terror'), ('Suspense', 'Suspense'), ('Bélica', 'Bélica'),
    ('Drama', 'Drama'), ('Misterio', 'Misterio'), ('Música', 'Música'), ('Romance', 'Romance')]

class PeliculaPorActorForm(forms.Form):
    actores = forms.CharField(label="Actor", widget=forms.TextInput(), required=True)

class PeliculaPorGeneroForm(forms.Form):
    genero = forms.CharField(label="Genero", widget=forms.Select(choices=GENEROS), required=True)

class PeliculaPorGeneroWhooshForm(forms.Form):
    genero = forms.CharField(label="Genero", widget=forms.Select(choices=GENEROSID), required=True)


    