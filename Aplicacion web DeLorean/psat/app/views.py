from django.shortcuts import render,redirect,render_to_response
from django.template.loader import get_template
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from django.contrib.auth import login, authenticate, logout
from django.views.decorators.csrf import csrf_exempt

# Create your views here.


def main (request):
