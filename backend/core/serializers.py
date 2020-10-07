from rest_framework.serializers import ModelSerializer

from core.models import Car


class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
