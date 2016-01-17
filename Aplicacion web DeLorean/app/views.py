#-*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from models import Page,Incidencias,Guardar
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import redirect
import xml.etree.ElementTree as etree
from xml.etree import ElementTree
from django.utils import feedgenerator
import urllib

@csrf_exempt
# Create your views here.
def main(request):
	if request.method == "GET":
		lista = ''
		ListaIncidencias = ''
		lista = Page.objects.all()
		rss = 'Canal rss'
		canalrss = 'rss'
		ListaIncidencias= Incidencias.objects.all()[:10]
		if request.user.is_authenticated():
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			response = render_to_response('index.html', {'canalrss':canalrss,'rss':rss,'Incidencias_menu':'Incidencias','I':'Cierre de','formulario':bienvenido,'salir':salir,'Titulo1':'Paginas de Usuario ',
														'Paginas':lista,'Incidences':ListaIncidencias,'10_Incidencias':'10 Primeras Incidencias del día'}, context_instance=RequestContext(request))
			
		else:
			bienvenido = formulario_bienvenido()
			response = render_to_response('index.html', {'canalrss':canalrss,'rss':rss,'Incidences':ListaIncidencias,'Incidencias_menu':'Incidencias',
											'I':'Inicio de','formulario':bienvenido,'Titulo1':'Paginas de Usuario','10_Incidencias':'10 Primeras Incidencias del día','Paginas':lista}, context_instance=RequestContext(request))
		return HttpResponse(response)

	elif request.method == "POST":
		username = request.POST['nombreusuario']
		password = request.POST['contrasena']
		user = authenticate(password=password, username=username)
		if user :
			if user.is_active:
				login(request, user)
				try:
					Page.objects.get(recursop=username)
					return redirect('/')
				except Page.DoesNotExist:
					Titulo = 'Pagina de ' + username
					p = Page(recursop = username, titulo=Titulo,contenido= "No se ha especificado")
					p.save()	
					return redirect('/')
			else:
				return redirect('/')
		else:
			return redirect('/')
@csrf_exempt
def logout_view(request):
	logout(request)
	# Redirect to a success page.
	return redirect('/')




def formulario_cambio():
	formulario = "<form id = form1 action='' method='POST'>"
	formulario += "<br/>TITULO PERSONAL: <input type='text' name='Titulo'>"
	formulario += "<br/>Descripcion: <input type='text' name='Descripcion'>"
	formulario += "<input type='submit' value='Enviar'></form>"
	return(formulario)

def formulario_bienvenido():
	bienvenido = "<form id=form1 method='POST' action='loguear'> \
				<p><label>Nick<input type='text' class='fields' name='nombreusuario' />\
				</label><label>Pass<input type='password' class='fields' name='contrasena' />\
				<input type='submit' class='submit_button' name='Submit' value='Entrar' />\
				</label></p></form>"
	return(bienvenido)

@csrf_exempt
def usuario (request,recurso):
	if request.method == "GET":
		Objetos = Page.objects.get(recursop=recurso)
		Titulo =Objetos.titulo +' Descripcion: '+ Objetos.contenido
		rss = 'Canal rss'
		canalrss = Objetos.recursop+'/rss'
		incidencias = Guardar.objects.filter(Usuario = recurso)[:10]
		ListaIncidencias = []
		for i in incidencias:
			ListaIncidencias += Incidencias.objects.filter(id = i.Id_incidencia)
		if request.user.is_authenticated():
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			Inicio = 'Cierre de'
		else:
			bienvenido = formulario_bienvenido()
			salir = ''
			Inicio = 'Inicio de'
		respuesta = ''
		if request.user.username == recurso:
			respuesta = formulario_cambio()
		response = render_to_response('index.html', {'canalrss':canalrss,'rss':rss,'Incidencias_menu':'Incidencias','salir':salir,'formulario':bienvenido,'I':'Cierre','INICIO':'Inicio','Titulo':Titulo,'Personaliza':respuesta,
								'incidencias_usuario':ListaIncidencias}, context_instance=RequestContext(request))
		return HttpResponse(response)
	elif request.method == 'POST':
		CambiaTitulo = request.POST['Titulo']
		Cambiadesc = request.POST['Descripcion']
		p = Page.objects.get(recursop=recurso)
		p.titulo = CambiaTitulo
		p.contenido = Cambiadesc
		p.save()
		return redirect('/' + recurso)

@csrf_exempt
def Ayuda(request):
	if request.user.is_authenticated():
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			Inicio = 'Cierre de '
	else:
		bienvenido = formulario_bienvenido()
		salir = ''
		Inicio = 'Inicio de '
	Titulo = 'Instrucciones de uso de Delorean'
	parrafada ='Usa el Menu disponible a la izquierda para moverte por las diferentes paginas del sitio '
	parrafadaIni ='Inicio: Se muestran las paginas de Usuario disponibles con un link el propietario y la Descripción elegida por él, además de las 10 primeras incidencias del canal '
	parrafadaTodas ='Todas: Pagina con todas las Incidencias desde la última actualización se ofrece un filtro abajo a la izquierda con diferentes campos'
	parrafadaInci = 'Incidencias : Pagina privada con todas las Incidencias se oferta el número total de incidencias un opción de guardar incidencia y un boton de recarga para actualizarlas'
	parrafadarss = 'Canales rss : Tanto en la pagina principal como en las paginas de usuario se da la opción a mostrarlas a modo de canal rss para ello hay un botón extra en el menu de la izquierda'

	response = render_to_response('index.html', {'parrafadaIni':parrafadaIni,'parrafadaTodas':parrafadaTodas,'parrafadaInci':parrafadaInci,'parrafadarss':parrafadarss,
										'Titulo':Titulo,'Incidencias_menu':'Incidencias','I':Inicio,'salir':salir,'formulario':bienvenido,'INICIO':'Inicio', 'ayuda': parrafada},
									 			  context_instance=RequestContext(request))
	return HttpResponse(response)

def usuario_rss(request,resource):
	context = {}

	record = Page.objects.get(recursop=resource)
	incidencias = Guardar.objects.filter(Usuario = resource)
	Lista = ''
	for i in incidencias:
		ListaIncidencias = Incidencias.objects.get(id = i.Id_incidencia)
		Lista +='<b>Incidencia</b>' + ' Tipo:'+ListaIncidencias.tipo +" " +' Provincia: '+ ListaIncidencias.provincia +" "
		Lista +=' Carretera: '+ ListaIncidencias.carretera +" "+' Publicada en:' +ListaIncidencias.fechahora+ ' '+ ListaIncidencias.nivel+' '
		Lista +=ListaIncidencias.carretera +' '+ListaIncidencias.inicial+' '+ListaIncidencias.final+' '+ListaIncidencias.sentido+' '+ListaIncidencias.hacia+'<br></br>'

	feed = feedgenerator.Rss201rev2Feed(
		title='Titulo: '+record.titulo,
		link= '',
		description='Descripcion: '+record.contenido,
		language=u"en",
	)

	feed.add_item(
		title=" INCIDENCIAS",
		link='',
		description= Lista,
	)
	str = feed.writeString('utf-8')
	
	return HttpResponse(str)

def principal_rss(request):

	lista = Incidencias.objects.all()[:10]
	ListaIncidencias= ''
	if lista!=False:
		for i in lista:
			ListaIncidencias +='Incidencia ' + ' Tipo:'+i.tipo +" " +' Provincia:'+ i.provincia +" "
			ListaIncidencias +=' Carretera: '+ i.carretera +" "+' Publicada en:' +i.fechahora+ ' '+ i.nivel+' '
			ListaIncidencias +=i.carretera +' '+i.inicial+' '+i.final+' '+i.sentido+' '+i.hacia+'<br></br>'
	
	lista = Page.objects.all()
	ListaEntera= ''
	for i in lista:
		ListaEntera += '<b>'+'Titulo: '+'</b>'+ i.titulo +'<br></br>'
		ListaEntera += '<b>'+ 'Nick: '+'</b>' + i.recursop +'<br></br>'
		ListaEntera += '<b>'+'Descripcion: '+'</b>'+i.contenido +'<br></br>'+'</p>'

	feed = feedgenerator.Rss201rev2Feed(
		title='DeLorean',
		link= '',
		description= '',
		language=u"en",
	)
	
	feed.add_item(
		title=" Paginas de usuario",
		link='http://localhost:1234/',
		description= ListaEntera,
	)

	feed.add_item(
		title=" INCIDENCIAS",
		link='http://localhost:1234/incidencias',
		description= ListaIncidencias,
	)
	str = feed.writeString('utf-8')
	
	return HttpResponse(str)




@csrf_exempt
def formulariotodas():
	formulario1 = "<form action='' method='POST'>"
	formulario1 += "Filtro de busqueda </br>"
	formulario1 += "Tipo: <input type='text' name='Tipo'>"
	formulario1 += "<input type='submit' value='Filtrar'></form>"
	formulario2 = "<form action='' method='POST'>"
	formulario2 += "Provincia: <input type='text' name='Provincia'>"
	formulario2 += "<input type='submit' value='Filtrar'></form>"
	formulario3 = "<form action='' method='POST'>"
	formulario3 += "Hacia: <input type='text' name='Hacia'>"
	formulario3 += "<input type='submit' value='Filtrar'></form><br></br>"
	return (formulario1 + formulario2 +formulario3)

@csrf_exempt
def boton():
	formulario = "<form action='/todas' method='GET'>"
	formulario += "<input type='submit' value='Volver a todas las incidencias'></form>"
	return(formulario)
def seleccion():
	formulario = "<form action='' method='POST'>"
	formulario += "<input type='submit' value='I.id'></form>"
	return(formulario)

@csrf_exempt
def Todas(request):
	if request.method == 'GET':
		if request.user.is_authenticated():
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			Inicio = 'Cierre de '
		else:
			bienvenido = formulario_bienvenido()
			salir = ''
			Inicio = 'Inicio de'
		Inc = Incidencias.objects.all()
		if len(Inc)==0:
			CogerIncidencias()
		filtro  =formulariotodas()
		parrafada = 'Todas las Incidencias'
		ListaIncidencias = Incidencias.objects.all()
	else:
		if 'Tipo' in request.POST:
			Tipo = request.POST['Tipo'].upper()
			Tipo = " "+Tipo+" "
			ListaIncidencias= Incidencias.objects.filter(tipo=Tipo)	
		elif 'Provincia' in request.POST:
			Provincia = request.POST['Provincia'].upper()
			Provincia = " "+Provincia+" "
			ListaIncidencias = Incidencias.objects.filter(provincia=Provincia)
		elif 'Hacia' in request.POST:
			Hacia = request.POST['Hacia'].upper()
			Hacia = " "+Hacia+" "
			ListaIncidencias = Incidencias.objects.filter(hacia=Hacia)
		if request.user.is_authenticated():
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			Inicio = 'Cierre de '
		else:
			bienvenido = formulario_bienvenido()
			salir = ''
			Inicio = 'Inicio de'
		filtro  =formulariotodas()
		parrafada = 'Incidencias Filtradas'
	response = render_to_response('index.html', {'Personaliza':filtro,'Incidencias_menu':'Incidencias','I':Inicio,'salir':salir,'formulario':bienvenido,'INICIO':'Inicio',
									 'Titulo1': parrafada,'incidencias_usuario':ListaIncidencias},
									 			  context_instance=RequestContext(request))
	return HttpResponse(response)

@csrf_exempt
def CogerIncidencias():

	url ='http://www.dgt.es/incidencias.xml'
	abrir_url = urllib.urlopen(url)
	xml_content = ElementTree.parse(abrir_url)
	for node in xml_content.getiterator('incidencia'):
		a = node[0].text
		b = node[1].text
		c = node[2].text
		d = node[3].text
		if node[4].text != None:
			e = node[4].text
		else:
			e = 'No hay informacion'
		f = node[5].text
		g = node[6].text
		h = node[7].text
		if node[8].text != None:
			i = node[8].text
		else:
			i = 'No hay informacion'
		if node[9].text != None:
			j = node[9].text
		else:
			j = 'No hay informacion'
		if node[10].text != None:
			k = node[10].text
		else:
			k = 'No hay informacion'
		l = node[11].text
		if node[12].text != None:
			m = node[12].text
		else:
			m= 'No hay informacion'
		Incs = Incidencias(tipo = a ,autonomia = b ,provincia =c,matricula = d,causa=e,poblacion=f,fechahora=g,
						nivel=h,carretera=i,inicial=j,final=k,sentido=l,hacia=m)
		Incs.save()

@csrf_exempt
def privado(request):
	parrafada = 'No puedes acceder sin loguearte'
	salir='<li><a href="/">Volver a Inicio</a></li>'
	response = render_to_response('index.html', {'I':'Vuelve e inicia ','salir':salir, 'ayuda':parrafada},
									 			  context_instance=RequestContext(request))
	return HttpResponse(response)


@csrf_exempt
def incidencias(request):
	if request.user.is_authenticated():
		if request.method == 'GET':
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			Inicio = 'Cierre de '
			parrafada = 'Pagina privada de Incidencias, usa el botón para ver las últimas incidencias'
			Text ='Para Guardar una incidencia selecciona y pulsa ENTER'
			formulario = "<form action='' method='POST'>"
			formulario += "<input type='submit' name = 'Refresh' value='Recargar Incidencias'></form>"
			lista = Incidencias.objects.all()
			Total = 'Total de incidencias :  '
			totalincidencias = len(lista)
			response = render_to_response('index.html', {'Recarga':formulario,'Incidencias_menu':'Incidencias','I':Inicio,'salir':salir,'formulario':bienvenido,'INICIO':'Inicio',
									 'Total':Total,'numero':totalincidencias,'Titulo1': parrafada,'Titulo': Text,'incidencias_seleccion':lista},
									 			  context_instance=RequestContext(request))
			return HttpResponse(response)
		else:
			if 'Refresh' in request.POST:
				p=Incidencias.objects.all()
				p.delete()
				CogerIncidencias()
			else:
				Id = request.POST.getlist('Incidence')
				for i in range(len(Id)):
					p=Guardar(Id_incidencia=Id[i],Usuario=request.user.username)
					p.save()

		return redirect('/incidencias')
	else:
		return redirect('/privado')
