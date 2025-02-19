from django.http import HttpResponse
from django.shortcuts import render

def SurveysHome(request):
    return HttpResponse("Домашняя страница")
