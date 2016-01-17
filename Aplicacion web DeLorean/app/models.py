from django.db import models

# Create your models here.

class Page(models.Model):

	recursop = models.TextField(max_length=30)
	titulo = models.TextField()
	contenido = models.TextField(max_length = 30)

class Guardar(models.Model):
	Id_incidencia = models.IntegerField(primary_key=True)
	Usuario = models.TextField()

class Incidencias(models.Model):
	tipo=models.TextField()
	autonomia=models.TextField()
	provincia=models.TextField()
	matricula=models.TextField()
	causa=models.TextField()
	poblacion=models.TextField()
	fechahora=models.TextField()
	nivel =models.TextField()
	carretera=models.TextField()
	inicial=models.TextField()
	final=models.TextField()
	sentido=models.TextField()
	hacia=models.TextField()