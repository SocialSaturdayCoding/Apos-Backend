from masonite.api.resources import Resource
from masonite.api.serializers import JSONSerializer

from app.Item import Item


class CouponResource(Resource, JSONSerializer):
    model = Item
    methods = ['create', 'show', 'delete', 'update']
