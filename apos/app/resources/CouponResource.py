from masonite.api.resources import Resource
from masonite.api.serializers import JSONSerializer

from app.Coupon import Coupon


class CouponResource(Resource, JSONSerializer):
    model = Coupon
    methods = ['create', 'index', 'delete']
