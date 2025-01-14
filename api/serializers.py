from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Doctor,Patient,PatientHistory,Hospital


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Patient
        fields = ["id","name","user"]

class CreatePatienSerialzier(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = "__all__" 

class PatientHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHistory
        fields = "__all__"


class DoctorSerialzier(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta:
        model = Doctor
        fields = ['name','user']

    
class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = "__all__"
