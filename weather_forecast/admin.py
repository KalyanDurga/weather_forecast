from django.contrib import admin

# Register your models here.
from weather_forecast.models import *

admin.site.register(WeatherData)
admin.site.register(UserQuery)