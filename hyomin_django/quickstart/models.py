from django.db import models

class KrWeather(models.Model):
    w_area = models.CharField(max_length=100)
    w_curr = models.CharField(max_length=100)
    w_cute = models.CharField(max_length=100)
    w_pcute = models.CharField(max_length=100)
    w_rain = models.CharField(max_length=100)
    w_snow = models.CharField(max_length=100)
    w_humi = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'kr_weather'


class MyKrWeather(models.Model):
    id = models.IntegerField(primary_key=True)
    w_area = models.TextField()
    w_curr = models.TextField()
    w_cute = models.TextField()
    w_pcute = models.TextField()
    w_rain = models.TextField()
    w_snow = models.TextField()
    w_humi = models.TextField()

    class Meta:
        managed = False
        db_table = 'my_kr_weather'


class MyPit(models.Model):
    id = models.IntegerField(primary_key=True)
    iname = models.TextField()
    iprice = models.TextField()
    ireview = models.TextField()

    class Meta:
        managed = False
        db_table = 'my_pit'


class Pit(models.Model):
    iname = models.CharField(max_length=100)
    iprice = models.CharField(max_length=100)
    ireview = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'pit'
