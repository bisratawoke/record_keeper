from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class DoctorSerialzier(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = ['name','user']
