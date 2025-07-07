from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello Django 유튜브 크리에이터 웹사이트")