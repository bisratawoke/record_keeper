from rest_framework import serializers

class CreateHospitalDto(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    address = serializers.CharField(max_length=100)
  

