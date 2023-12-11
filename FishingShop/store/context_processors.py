from .basket import Basket
from store.models import FishingSeason


def basket(request):
    return {'basket': Basket(request)}


def fishing_seasons(request):
    return {'fishing_seasons': FishingSeason.objects.all()}
