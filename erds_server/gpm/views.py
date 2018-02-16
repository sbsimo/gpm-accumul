from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse


def index(request):
    return HttpResponse("Hello, precipitation time serie will be available through this app!")


def time_series(request, lon, lat, time_period_hours):
    print(lon)
    print(lat)
    print(time_period_hours)

    lon_f = float(lon)
    if lon_f < -180 or lon_f > 180:
        return HttpResponseBadRequest('Longitude value {} is not in the valid range -180 --> 180'.format(lon))

    lat_f = float(lat)
    if lat_f < -60 or lat_f > 60:
        return HttpResponseBadRequest('Latitude value {} is not in the valid GPM range -60 --> 60'.format(lat))

    hours = int(time_period_hours)

    return JsonResponse({'precipitation in mm': [34.5, 89.3, 23.8, lon_f, lat_f, hours]})
