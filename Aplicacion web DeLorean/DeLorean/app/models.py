from django.db import models

# Create your models here.

class Page(models.Model):

	recursop = models.TextField(max_length=30)
	contenido = models.TextField()
	user = models.TextField(max_length = 30)