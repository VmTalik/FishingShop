from store.models import Manufacturer, RodType, Rod
from store.serializers import ManufacturerSerializer, RodTypeSerializer, RodSerializer
from rest_framework.viewsets import ModelViewSet
from django.shortcuts import render


def index(request):
    return render(request, 'store/index.html')


def manufacturers(request):
    return render(request, 'store/manufacturers.html')


def catalog_summer(request):
    return render(request, 'store/catalog-summer.html')


def rod_type(request):
    return render(request, 'store/rod-type.html')


def rods(request, rod_type_id):
    current_rods = Rod.objects.filter(rod_type_id=rod_type_id)
    manufacturers = Manufacturer.objects.all()
    context = {'current_rods': current_rods, 'manufacturers': manufacturers}
    return render(request, 'store/rods.html', context)


def rod(request, rod_type_id, rod_id):
    current_rod = Rod.objects.get(pk=rod_id)
    context = {'current_rod': current_rod}
    return render(request, 'store/rod.html', context)


class ManufacturerViewSet(ModelViewSet):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer


class RodTypeViewSet(ModelViewSet):
    queryset = RodType.objects.all()
    serializer_class = RodTypeSerializer


class RodViewSet(ModelViewSet):
    queryset = Rod.objects.all()
    serializer_class = RodSerializer
