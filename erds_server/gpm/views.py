from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, precipitation time serie will be available through thiss app!")


def time_series(request, lon, lat, time_period_hours):
    print(lon)
    return HttpResponse("Hello, precipitation time serie will be available through thiss app!")