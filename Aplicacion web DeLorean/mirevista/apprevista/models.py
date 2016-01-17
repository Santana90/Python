from django.db import models
from django.contrib.auth.models import User

# Create your models here.

		
class Revista(models.Model):
		usuario = models.CharField(max_length=20)
		titulo = models.CharField(max_length=20)
		fecha = models.DateTimeField(auto_now=True)
		fondo = models.CharField(max_length=20)
		elegidas = models.CharField(max_length=20)
		
		def __str__(self):
			return self.titulo

class Canales(models.Model):

		url = models.CharField(max_length=20)
		
		def __str__(self):
			return self.url


