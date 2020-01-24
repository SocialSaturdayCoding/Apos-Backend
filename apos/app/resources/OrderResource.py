from masonite.api.resources import Resource
from masonite.api.serializers import JSONSerializer

from app.Order import Order


class OrderResource(Resource, JSONSerializer):
    model = Order
