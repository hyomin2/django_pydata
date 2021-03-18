# from django.contrib.auth.models import User, Group
from rest_framework import serializers
from hyomin_django.quickstart.models import MyKrWeather, MyPit



# class UserSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = User
#         fields = ['url', 'username', 'email', 'groups']


# class GroupSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = Group
#         fields = ['url', 'name']


class MyKrWeatherSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyKrWeather
        fields = ['id', 'w_area', 'w_curr', 'w_cute', 'w_pcute', 'w_rain', 'w_snow', 'w_humi']


class MyPitSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyPit
        fields = ['id', 'iname', 'iprice', 'ireview']