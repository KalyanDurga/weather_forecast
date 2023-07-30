# models.py
from django.db import models

class WeatherData(models.Model):
    location = models.CharField(max_length=100)
    temperature = models.FloatField()
    humidity = models.FloatField()
    weather_description = models.CharField(max_length=100)


class UserQuery(models.Model):
    location = models.CharField(max_length=100)
    question = models.TextField()
    ai_response = models.TextField()

    def __str__(self):
        return f"{self.location} - {self.question}"