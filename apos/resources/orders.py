from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse

from apos.extensions import db
from apos.models import Order

parsers = {
    'normal': {
        'parser': reqparse.RequestParser(),
        'strict': True,
        },
    'lazy': {
        'parser': reqparse.RequestParser(),
        'strict': False,
        },
}

for mode in parsers.keys():
    parser = parsers[mode]['parser']
    strict = parsers[mode]['strict']

    parser.add_argument('location', type=str, required=(True and strict))
    parser.add_argument('deadline', type=datetime.fromtimestamp, required=(True and strict))
    parser.add_argument('description', type=str, required=(False and strict))
    parser.add_argument('title', type=str, required=(True and strict))
    parser.add_argument('deliverer', type=str, required=(True and strict))
    parser.add_argument('arrival', type=datetime.fromtimestamp, required=(False and strict))


class OrderListResource(Resource):
    @jwt_required
    def get(self):
        orders = Order.query.all()
        return [order.serialize for order in orders]

    @jwt_required
    def put(self):
        args = parsers['normal']['parser'].parse_args()
        order = Order(owner_id=get_jwt_identity(), **args)
        db.session.add(order)
        db.session.commit()
        return order.serialize, 201


class OrderActiveListResource(Resource):
    @jwt_required
    def get(self):
        orders = Order.query.filter(Order.deadline > datetime.now()).all()
        return [order.serialize for order in orders]


class OrderUserListResource(Resource):
    @jwt_required
    def get(self):
        orders = Order.query.filter(Order.owner == get_jwt_identity()).all()
        return [order.serialize for order in orders]


class OrderResource(Resource):
    @jwt_required
    def get(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            abort(404, message=f"Order {order_id} does not exist")
        return order.serialize

    @jwt_required
    def delete(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            abort(404, message=f"Coupon {order} does not exist")
        db.session.delete(order)
        db.session.commit()
        return '', 204

    @jwt_required
    def patch(self, order_id):
        args = parsers['lazy']['parser'].parse_args()
        args = {k:v for k,v in args.items() if v is not None}
        orders = Order.query.filter_by(id=order_id)
        orders.update(args)
        db.session.commit()
        return orders.first().serialize

