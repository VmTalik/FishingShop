from rest_framework.serializers import ModelSerializer
from store.models import Manufacturer, RodType, Rod


class ManufacturerSerializer(ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = '__all__'


class RodTypeSerializer(ModelSerializer):
    class Meta:
        model = RodType
        fields = '__all__'


class RodSerializer(ModelSerializer):
    class Meta:
        model = Rod
        fields = '__all__'
