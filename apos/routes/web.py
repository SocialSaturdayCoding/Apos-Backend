"""Web Routes."""

from masonite.routes import Get, Post, Put, Patch, Delete

ROUTES = [
    Post('/api/v1/auth', 'AuthController@show'),

    Get('/api/v1/orders', 'OrderController@list'),
    Put('/api/v0/orders', 'OrderController@create'),

    Get('/api/v1/orders/@id', 'OrderController@get'),
    Patch('/api/v1/orders/@id', 'OrderController@edit'),
    Delete('/api/v1/orders/@id', 'OrderController@delete'),

    Put('/api/v1/orders/@order/items', 'ItemController@create'),
    Get('/api/v1/orders/@order/items/@id', 'ItenController@get'),
    Patch('/api/v1/orders/@order/items/@id', 'ItenController@edit'),
    Delete('/api/v1/orders/@order/items/@id', 'ItenController@delete'),

    Get('/coupons', 'CouponController@list'),
    Put('/coupons', 'CouponController@create'),
    Delete('/coupons/@id', 'CouponController@delete'),
]
