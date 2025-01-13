from rest_framework import serializers

class UpdatePatientHistoryDto(serializers.Serializer):
    description = serializers.CharField()
    id = serializers.IntegerField()
