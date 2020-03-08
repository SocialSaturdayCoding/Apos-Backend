from datetime import datetime

from flask_restful import Resource, abort, reqparse

from apos.extensions import db
from apos.models import Order

parser = reqparse.RequestParser()
parser.add_argument('location', type=str, required=True)
parser.add_argument('deadline', type=datetime.fromtimestamp)
parser.add_argument('description', type=str, required=False)
parser.add_argument('title', type=str, required=True)
parser.add_argument('deliverer', type=str, required=True)
parser.add_argument('arrival', type=datetime.fromtimestamp, required=False)


class OrderListResource(Resource):
    def get(self):
        orders = Order.query.all()
        return [order.serialize for order in orders]

    def put(self):
        args = parser.parse_args()
        order = Order(owner_id=1, **args) # TODO
        db.session.add(order)
        db.session.commit()
        return order.serialize, 201

class OrderResource(Resource):
    def get(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            abort(404, message=f"Order {order_id} does not exist")
        return order.serialize

    def delete(self, order_id):
        order = Order.query.get(order_id)
        if not order:
            abort(404, message=f"Coupon {order} does not exist")
        db.session.delete(order)
        db.session.commit()
        return '', 204

