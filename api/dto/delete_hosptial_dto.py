from rest_framework import serializers

class DeleteHospitalDto(serializers.Serializer):
    id = serialziers.IntegerField()