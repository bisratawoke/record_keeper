from rest_framework import serializers
class CreatePatientDto(serializers.Serializer):
    doctor = serializers.IntegerField()
    name = serializers.CharField()


