from rest_framework import serializers


class UpdateHospitalDto(serializers.Serializer):
    name  = serializers.CharField()
    id = serializers.IntegerField()