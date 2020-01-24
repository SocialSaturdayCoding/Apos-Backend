"""Web Routes."""

from masonite.routes import Get, Post, Put, Patch, Delete

from app.resources.CouponResource import CouponResource
from app.resources.ItemResource import ItemResource
from app.resources.OrderResource import OrderResource

ROUTES = [
    Post('/api/v1/auth', 'AuthController@show'),

    OrderResource('/api/v1/orders').routes(),
    ItemResource('/api/v1/orders/@order_id/items').routes(),
    CouponResource('/api/v1/coupons').routes(),
]
