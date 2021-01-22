# encoding:utf-8
from bs4 import BeautifulSoup
import urllib.request
import sqlite3
import lxml
import re, os, shutil
from datetime import datetime
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, DATETIME, ID, KEYWORD, STORED, NUMERIC
from whoosh.qparser import QueryParser, MultifieldParser, OrGroup
from main.models import Pelicula, Actor, Genero, Personal
from django.shortcuts import render, redirect
from main.forms import *


def pelicula_por_actor(request):
    
    formulario = PeliculaPorActorForm()
    peliculas=[]
    totalpeliculas=[]
    actores = ""
    if request.method=='POST':
        formulario = PeliculaPorActorForm(request.POST)
        if formulario.is_valid():
            actores = formulario.cleaned_data['actores']

    directorio = 'Index'
    ix = open_dir(directorio)
    with ix.searcher() as searcher:
        actor = "'" + actores + "'"
        query = QueryParser("actores", ix.schema).parse(actor)
        totalpeliculas =  searcher.search(query)
        for peli in totalpeliculas:
            peliculas.append(peli)
        return render(request, 'peliculasPorActor.html', {'formulario':formulario, 'peliculas':peliculas, 'actores':actores})

def pelicula_por_genero(request):
    
    formulario = PeliculaPorGeneroForm()
    peliculas=[]
    totalpeliculas=[]
    genero = ""
    if request.method=='POST':
        formulario = PeliculaPorGeneroForm(request.POST)
        if formulario.is_valid():
            genero = formulario.cleaned_data['genero']

    directorio = 'Index'
    ix = open_dir(directorio)
    with ix.searcher() as searcher:
        entry = "'" + genero + "'"
        query = QueryParser("genero", ix.schema).parse(entry)
        totalpeliculas = searcher.search(query, limit=20)
        for peli in totalpeliculas:
            peliculas.append(peli)
        return render(request, 'peliculasPorGenero.html', {'formulario':formulario, 'peliculas':peliculas, 'genero':genero})


def list_peliculas(request):
    peliculas = Pelicula.objects.all().order_by('titulo')
    return render(request, 'peliculas.html', {'peliculas':peliculas})

def detallesPelicula(request, id):
    pelicula = Pelicula.objects.get(id = id)
    return render(request, 'detallesPelicula.html', {'p':pelicula})

def list_actores(request):
    actores = Actor.objects.all().order_by('nombre')
    return render(request, 'actores.html', {'actores':actores})

def detallesActor(request, id):
    actor = Actor.objects.get(id = id)
    return render(request, 'detallesActor.html', {'actor':actor})

def list_generos(request):
    generos = Generos.objects.all().order_by('nombre')
    return render(request, 'generos.html', {'generos':generos})

def list_personal(request):
    personal = Personal.objects.all().order_by('nombre')
    return render(request, 'personal.html', {'personal':personal})

def inicio(request):
    return render(request, 'index.html')


def sobreMi(request):

    return render(request, 'sobreMi.html')