from rest_framework import serializers

class DeletePatientHistoryDto(serializers.Serializer):
    id = serializers.IntegerField()
