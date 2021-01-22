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
from django.shortcuts import render, redirect
from main.models import Pelicula, Actor, Genero, Personal


urlGeneral = "https://www.themoviedb.org"
urlAventura = "https://www.themoviedb.org/genre/12-aventura/movie?language=es-ES"
urlAccion = "https://www.themoviedb.org/genre/28-accion/movie?language=es-ES"
urlFantasia = "https://www.themoviedb.org/genre/14-fantasia/movie?language=es-ES"
urlComedia = "https://www.themoviedb.org/genre/35-comedia/movie?language=es-ES"
urlAnimacion = "https://www.themoviedb.org/genre/16-animacion/movie?language=es-ES"
listaURLsPeliculas= [urlAventura, urlAccion, urlFantasia, urlComedia, urlAnimacion]



def get_peliculas():
    listaPeliculas= []
    for url in listaURLsPeliculas:
        openURL = urllib.request.urlopen(url)
        bs = BeautifulSoup(openURL, "lxml")
        res = bs.find("div", class_="results_page").find_all("div", class_=["card", "v4", "tight"])
        listaPeliculas.append(res)
    return listaPeliculas


def extraer_datos_peliculas():
    listaPel = get_peliculas()
    listaPeliculas = []
    for tipoPeliculas in listaPel:
        for pelicula in tipoPeliculas:
            linkP = pelicula.find("a")['href']
            linkPel= urlGeneral + linkP
             
            titulo = pelicula.find("div", class_="title").find("a").getText()
            if pelicula.find("div", class_="overview").find("p") is not None:
                sinopsis = pelicula.find("div", class_="overview").find("p").getText()
            else:
                sinopsis= "No existe sinopsis."
            openURL2 = urllib.request.urlopen(linkPel)
            bs2 = BeautifulSoup(openURL2, "lxml")
            dur = bs2.find("div", class_=["header_poster_wrapper", "false"]).find("div", class_="facts")
            if dur is not None:
                duracion = dur.find("span", class_="runtime").getText().replace(" ", "")
            else:
                duracion = "No se especifica"
            portada = urlGeneral + bs2.find("img", class_=["poster", "lazyload"]).get("data-srcset").split(",")[1][1:-3]
            listaActores = extraer_actores_pelicula(linkPel)
            listaPersonal = extraer_personal_pelicula(linkPel)
            listaGeneros= extraer_generos_pelicula(linkPel)
            listaPeliculas.append([titulo, portada, sinopsis, linkPel, duracion, listaActores, listaPersonal, listaGeneros])
      
    return listaPeliculas
            
def extraer_actores_pelicula(url):
    openURL2 = urllib.request.urlopen(url)
    bs2 = BeautifulSoup(openURL2, "lxml")
    listaActores = []
    actores= bs2.find("div", class_="white_column").find_all("li")[:3]
    for actor in actores:
        if actor.find("img") is not None:
            nombreActor = actor.find("p").find("a").getText()
            srcset = actor.find("img")['srcset'].split(",")[1][1:-3]
            imagen = urlGeneral+srcset
            linkActor = urlGeneral + actor.find("a")['href']
            
            openURL3 = urllib.request.urlopen(linkActor)
            bs3 = BeautifulSoup(openURL3, "lxml")
            edad = bs3.find("section", class_=["full_wrapper", "facts", "left_column"]).find_all("p")[3].getText().rstrip()[36:]
            lugarNacimiento = bs3.find("section", class_=["full_wrapper", "facts", "left_column"]).find_all("p")[4].getText().replace(" ", "").rstrip()[17:]
            if edad == "-":
                edad = "No se especifica"
            if lugarNacimiento == "-":
                lugarNacimiento = "No se especifica"
            biografia = bs3.find("div", class_=["biography", "true"]).find("p").getText()
            
            listaActores.append([nombreActor, imagen, linkActor, edad, lugarNacimiento, biografia])
    return listaActores

def extraer_personal_pelicula(urlPelicula):
    openURL4 = urllib.request.urlopen(urlPelicula)
    bs4 = BeautifulSoup(openURL4, "lxml")
    listaPersonal = []
    
    gente= bs4.find("ol", class_=["people", "no_image"]).find_all("li")[:3]
    
    for persona in gente:
        trabajador = persona.find("p").getText()
        if persona.find("p", class_="character") is not None:
            puesto = persona.find("p", class_="character").getText()
        else:
            puesto="Sin especificar"
        listaPersonal.append([trabajador, puesto])
        
    return listaPersonal

def extraer_generos_pelicula(urlPelicula):
    openURL5 = urllib.request.urlopen(urlPelicula)
    bs5 = BeautifulSoup(openURL5, "lxml")
    listaGeneros = []
    
    generos= bs5.find("span", class_="genres").find_all("a")
    for g in generos:
        genero = g.getText()
        listaGeneros.append(genero)
        
    return listaGeneros
 
#función auxiliar que hace scraping en la web y carga los datos en la base datos
def populateDB():
    #variables para contar el número de registros que vamos a almacenar
    num_peliculas = 0
    num_actores = 0
    num_generos = 0
    num_personal = 0
    
    #borramos todas las tablas de la BD
    Pelicula.objects.all().delete()
    Actor.objects.all().delete()
    Genero.objects.all().delete()
    Personal.objects.all().delete()


    listaPeliculas= extraer_datos_peliculas()
    for pelicula in listaPeliculas:
        if not Pelicula.objects.filter(titulo=pelicula[0]).exists():

            #Actores
            for actor in pelicula[5]:
                if not Actor.objects.filter(nombre = actor[0]).exists():
                    Actor.objects.create(nombre= actor[0],foto = actor[1], linkActor = actor[2], fechaNacimiento = actor[3], lugarNacimiento = actor[4], biografia=actor[5])
                    num_actores+=1

            #Generos
            for genero in pelicula[7]:
                if not Genero.objects.filter(nombre = genero).exists():
                    Genero.objects.create(nombre= genero)
                    num_generos+=1

            #Personal
            for personal in pelicula[6]:
                if not Personal.objects.filter(nombre = personal[0]).exists():
                    Personal.objects.create(nombre= personal[0], puesto=personal[1])
                    num_personal+=1
            
            #Pelicula
            p= Pelicula.objects.create(titulo= pelicula[0],portada= pelicula[1], sinopsis= pelicula[2], linkPelicula= pelicula[3], duracion= pelicula[4])
            p.save()
            for act in pelicula[5]:
                p.actores.add(Actor.objects.get(nombre=act[0]))
            for per in pelicula[6]:
                p.personal.add(Personal.objects.get(nombre=per[0]))
            for gen in pelicula[7]:
                p.generos.add(Genero.objects.get(nombre=gen))
            
            num_peliculas = num_peliculas + 1
    
 


    return ((num_peliculas, num_generos, num_actores , num_personal))
        
#carga los datos desde la web en la BD
def carga(request):
 
    if request.method=='POST':
        if 'Aceptar' in request.POST:
            num_peliculas, num_generos, num_actores , num_personal = populateDB()
            
            mensaje="Se han almacenado: " + str(num_peliculas) +" películas, " + str(num_generos) +" géneros, " + str(num_actores) +" actores, " + str(num_personal) +" trabajadores para películas."
            return render(request, 'cargaBD.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')


def soloNombres(lista):
    listaNombres=[]
    for elemento in lista:
        listaNombres.append(elemento[0].replace("'", ""))
    return listaNombres
    

def populateWhooshPeliculas():
    
    schemPeliculas = Schema(idPelicula=NUMERIC(stored=True), titulo=TEXT(stored=True), portada= STORED(), sinopsis= TEXT(stored=True), linkPelicula= TEXT(stored=True), duracion=TEXT(stored=True), actores = KEYWORD(stored=True, commas=True), personal = KEYWORD(stored=True, commas=True), genero = KEYWORD(stored=True, commas=True))

    if os.path.exists("Index"):
        shutil.rmtree("Index")
    os.mkdir("Index")
    

    ix = create_in("Index", schema=schemPeliculas)
    writer = ix.writer()
    listaPeliculas = extraer_datos_peliculas()
    numPeliculas=0
    for pelicula in listaPeliculas:
        writer.update_document(idPelicula =numPeliculas, titulo=pelicula[0], portada=pelicula[1], sinopsis=pelicula[2], linkPelicula=pelicula[3], duracion=pelicula[4], actores = soloNombres(pelicula[5]), personal = soloNombres(pelicula[6]), genero=pelicula[7])
        numPeliculas+=1
        print(numPeliculas)
    writer.commit()
    
    return numPeliculas

           
def cargaWhoosh(request):

    if request.method=='POST':
        if 'Aceptar' in request.POST:
            numPeliculas = populateWhooshPeliculas()

            mensaje="Se han almacenado: " + str(numPeliculas) +" películas."
            return render(request, 'cargaWhoosh.html', {'mensaje':mensaje})
        else:
            return redirect("/")
           
    return render(request, 'confirmacion.html')
