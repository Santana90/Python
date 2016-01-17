#-*- encoding: utf-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response
from models import Page
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse,HttpResponseNotFound,HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.template.loader import get_template
from django.template import Context
from django.template import RequestContext
from django.shortcuts import redirect
@csrf_exempt
# Create your views here.
def main(request):
	if request.method == "GET":
		if request.user.is_authenticated():
			bienvenido = '<p>Bienvenid@ '+ str(request.user.username)+"</p>"
			salir = '<p class="bye">   Cerrar sesion</p>'
			response = render_to_response('index.html', {'I':'Cierre','formulario':bienvenido,'salir':salir,'Titulo1':'10 Últimas Incidencias '}, context_instance=RequestContext(request))
			return HttpResponse(response )
		else:
			formulario = "<form id='form1' method='POST' action='loguear'> \
						<p><label>Nick<input type='text' class='fields' name='nombreusuario' />\
						</label><label>Pass<input type='password' class='fields' name='contrasena' />\
						<input type='submit' class='submit_button' name='Submit' value='Entrar' />\
						</label></p></form>"
			response = render_to_response('index.html', {'I':'Inicio','formulario':formulario,'Titulo1':'10 Últimas Incidencias '}, context_instance=RequestContext(request))
			return HttpResponse(response)

	elif request.method == "POST":
		username = request.POST['nombreusuario']
		password = request.POST['contrasena']
		user = authenticate(password=password, username=username)
		if user is not None:
			if user.is_active:
				login(request, user)
				response = render_to_response('index.html', {'I':'Inicio','Titulo1':'10 Últimas Incidencias '}, context_instance=RequestContext(request))
				return HttpResponse(response)
			else:
				return HttpResponse('You are inactive')
		else:
			response = render_to_response('index.html', {'I':'Inicio','formulario':formulario}, context_instance=RequestContext(request))
			return HttpResponse(response + 'pass o Nick incorrectos')
def logout_view(request):
	logout(request)
	# Redirect to a success page.
	return redirect('/')

def usuario (request,recurso):
	if request.method == "GET":
		print 'pa lade pacoooo'
		try:
			if request.user.username == recurso:
				record = Page.objects.filter(recursop=recurso)
				formulario = "<form action='' method='POST'>"
				formulario += "<br/>Contenido: <input type='text' name='Titulo'  value='" + record.contenido + "'>"
				formulario += "<input type='submit' value='Cambiar'></form>"
				response = render_to_response('index.html', {'I':'Cierre','Titulo':'pagina de','Personaliza':formulario}, context_instance=RequestContext(request))
			return HttpResponse(response)
		except Page.DoesNotExist:
			mispaginas = Page.objects.filter(user=recurso)
			if request.user.is_authenticated():
				Respuesta = "Pagina de :"
				formulario = "<form action='' method='POST'>"
				formulario += "<br/>Contenido: <input type='text' name='Titulo'>"
				formulario += "<input type='submit' value='Enviar'></form>"
			else:
				formulario = ""
				Respuesta = "Estas entrando como invitado logueate"
			return HttpResponseNotFound(Respuesta)
	else:
		response = render_to_response('index.html', {'I':'Cierre'}, context_instance=RequestContext(request))
		return HttpResponse(response)
