# Create your views here.
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import REDIRECT_FIELD_NAME, login as auth_login, logout as auth_logout
from models import Revista
from models import Canales
import feedparser
@csrf_exempt
def main(request):
	if request.method == 'POST':
		print 'entro en el post'
		username = request.POST['username']
		print 'el username es: ' + username
		clave = request.POST['password']
		print 'el password es: ' + clave
		palabra = username
		user = authenticate(username=username, password=clave)
		if user is not None:
			print 'el usuario no es nulo'
			if user.is_active:
				print 'activo'
				auth_login(request,user)
				print 'he logueado' 
				bienvenido = 'Bienvenid@ ' + username + '!'
				salir = 'cerrar sesion'
				
				try:
					print 'entro try'
					probando = Revista.objects.get(usuario=username)
					print'ya tiene revista'
				except Revista.DoesNotExist:
					print 'excepcion'
					q = Revista(titulo = 'revista de ' + palabra,usuario = palabra)
					q.save()
					print 'guardo que te guardo'
				
				
				print 'cogo la lista de revistas'
				lista = Revista.objects.all()
				lista2 = Revista.objects.filter(usuario=palabra)
				titulo = 'Lista de Revistas'
				response = render_to_response('index.html', {'formulario':bienvenido,'salir':salir, 'lista': lista, 
								'lista2': lista2, 'titulocontenido': titulo}, context_instance=RequestContext(request))

				return HttpResponse(response)
			else:
				response= "<html><body>INCORRECTO</body></html>"
				return HttpResponse(response)
		else:
			print 'el usuario es nulo'

	else:
		user = request.user
		if user.is_authenticated():		
			bienvenido = 'Bienvenid@ ' + user.username + '!'
			salir = 'cerrar sesion'
				
			try:
				print 'entro try'
				probando = Revista.objects.get(usuario=user.username)
				print'ya tiene revista'
			except Revista.DoesNotExist:
				print 'excepcion'
				q = Revista(titulo = 'revista de ' + user.username,usuario = user.username)
				q.save()
				print 'guardo que te guardo'
			
				
			print 'cogo la lista de revistas'
			lista = Revista.objects.all()
			lista2 = Revista.objects.filter(usuario=user.username)
			titulo = 'Lista de Revistas'
			response = render_to_response('index.html', {'formulario':bienvenido,'salir':salir, 'lista': lista, 
								'lista2': lista2, 'titulocontenido': titulo}, context_instance=RequestContext(request))

			return HttpResponse(response)
		else:
			login = User.objects.all()
			lista = Revista.objects.all()
			fondo = 'blue'
			titulo = 'Lista de Revistas'
			formulario1='<form action="logear" method="post"><p>Usuario:<input id="id_username" type="text" name = "username" size="7"/></p><p>Password:<input id="id_password" type="password" name = "password"size="6"/></p><p><input type="submit" value="entrar"/></p></form>'
			response = render_to_response('index.html', {'formulario':formulario1, 'titulocontenido': titulo,  'lista': lista, 'fondo': fondo}, context_instance=RequestContext(request))
			print 'probando'
			return HttpResponse(response)



def usuario(request, resource):
	if request.method == 'POST':
		print 'entro en el post'
		print resource
		print request.POST
		if request.POST['titulo'] == 'blue' or request.POST['titulo'] == 'red' or request.POST['titulo'] == 'yellow' :
			print 'entro en estilo'
			estilo = request.POST['titulo']
			lista = Revista.objects.get(usuario=resource)
			lista.fondo = estilo
			lista.save()
			print estilo
		else:
			print 'entro en titulo'
			titulo = request.POST['titulo']
			lista = Revista.objects.get(usuario=resource)
			lista.titulo = titulo
			lista.save()
		lista = Revista.objects.filter(usuario=resource)
		formtitulo='<form action="" method="post"><p>Nuevo Titulo<input type="text" name = "titulo" size="9"/></p><p><input type="submit" value="cambiar"/></p></form>'
		formcss='<form action="" method="post"><p>Nuevo Estilo:</br><input type="radio" name="titulo" value="blue">Azul</p><p><input type="radio" name="titulo" value="red">Rojo</p><p><input type="radio" name="titulo" value="yellow">Amarillo</p></p><p><input type="submit" value="Elegir estilo"/></p></form>'

		

		response = render_to_response('index.html', {'titulolista': lista, 'formtitulo': formtitulo, 'formcss': formcss},
									 			  context_instance=RequestContext(request))
		return HttpResponse(response)
		
	else:
		print 'entro en usuario'
		print request.user.username
		print resource
		if request.user.username == resource:
			print 'es el mismo'
			#form titulo revista
			lista = Revista.objects.filter(usuario=resource)
			formtitulo='<form action="" method="post"><p>Nuevo Titulo: <input type="text" name = "titulo" size="9"/></p><p><input type="submit" value="cambiar"/></p></form>'
			
			formcss='<form action="" method="post"><p>Nuevo Estilo:</br><input type="radio" name="titulo" value="blue">Azul</p><p><input type="radio" name="titulo" value="red">Rojo</p><p><input type="radio" name="titulo" value="yellow">Amarillo</p></p><p><input type="submit" value="Elegir estilo"/></p></form>'

			response = render_to_response('index.html', {'titulolista': lista, 'formtitulo': formtitulo, 'formcss': formcss},
									 			  context_instance=RequestContext(request))
			return HttpResponse(response)
		else:
			print 'es visitante'
			lista = Revista.objects.filter(usuario=resource)
			response = render_to_response('index.html', {'titulolista': lista},
									 			  context_instance=RequestContext(request))
			return HttpResponse(response)

def salir(request):
	logout(request)
	return HttpResponseRedirect('/')


def canales(request):
	print 'entro a canales'
	if request.method == 'POST':
		link = request.POST['url']
		q = Canales(url = link)
		q.save()
		#lista = Canales.objects.get(id=1)
		#d = feedparser.parse(lista.url)
		#sol = d.entries[0].title
		
	formcanales='<form action="" method="post"><p>Nuevo canal (Url): <input type="text" name = "url" size="9"/></p><p><input type="submit" value="Anadir"/></p></form>'

	lista = Canales.objects.all()
	response = render_to_response('index.html', {'formcanales': formcanales, 'listacanales': lista},
									 			  context_instance=RequestContext(request))
	return HttpResponse(response)

def num(request, resource):
	#if request.method == 'POST':
	#	lista = Revista.objects.filter(usuario=request.user.username)
	#	lista.elegidas = resource

	#else: 
	lista = Canales.objects.get(id=resource)
	d = feedparser.parse(lista.url)
	i = 0
	prueba = ''
	while i < 10:
		sol = d.entries[i].title
		prueba = prueba + sol + '<br/>'
		i = i+1
	formnoticias='<form action="" method="post"><p><input type="submit" value="Elegir noticia"/></p></form>'
	iden = resource
	response = render_to_response('index.html', {'noticias': prueba, 'formnoticias': formnoticias, 'vinculo': iden},
									 			  context_instance=RequestContext(request))
	return HttpResponse(response)

def ayuda(request):
	parrafada = 'Mi revista funciona con usuarios logeados y no logeados. Los logeados tienen mas funciones que los no logeados. Sirve de noticias por canales rss a cada revista de usuario.'

	response = render_to_response('index.html', {'noticias': parrafada},
									 			  context_instance=RequestContext(request))
	return HttpResponse(response)




		
