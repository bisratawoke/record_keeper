from rest_framework import serializers

class CreateAssetCategoryDto(serializers.Serializer):
    name = serializers.CharField(max_length=200)
