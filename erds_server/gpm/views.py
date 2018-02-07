from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, precipitation time serie will be available through thiss app!")