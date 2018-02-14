from django.urls import path, re_path

from . import views

app_name = 'gpm'

urlpatterns = [
    path('', views.index, name='index'),
    re_path(r'^(?P<gibbone>\w+)/$', views.time_series, name='time_series')
]