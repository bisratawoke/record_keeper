from rest_framework import serializers

class CreatePatientHistoryDto(serializers.Serializer):
    description = serializers.CharField()
    