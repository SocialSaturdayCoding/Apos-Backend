from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse

from apos.extensions import db
from apos.models import Item, Order

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

    parser.add_argument('name', type=str, required=(True and strict))
    parser.add_argument('tip_percent', type=int, required=(False and strict))
    parser.add_argument('price', type=int, required=(False and strict))


class ItemListResource(Resource):
    @jwt_required
    def get(self, order_id):
        items = Item.query.filter_by(order_id=order_id).all()
        return [item.serialize for item in items]

    @jwt_required
    def put(self, order_id):
        args = parsers['normal']['parser'].parse_args()
        order = Order.query.get(order_id)
        if order.deadline < datetime.utcnow():
            abort(422, message="The order is expired, so no items can be added")
        item = Item(order_id=order_id, user_id=get_jwt_identity(), **args)
        db.session.add(item)
        db.session.commit()
        return item.serialize, 201

class ItemResource(Resource):
    @jwt_required
    def get(self, order_id, item_id):
        item = Item.query.filter_by(order_id=order_id, id=item_id).first()
        if not item:
            abort(404, message=f"Item {item_id} does not exist for order {order_id}")
        return item.serialize

    @jwt_required
    def delete(self, order_id, item_id):
        # Check if order is not expired TODO
        item = Item.query.filter_by(order_id=order_id, id=item_id).first()
        if not item:
            abort(404, message=f"Item {item_id} does not exist for order {order_id}")
        db.session.delete(item)
        db.session.commit()
        return '', 204

    @jwt_required
    def patch(self, order_id, item_id):
        # Check if order is not expired TODO
        args = parsers['lazy']['parser'].parse_args()
        args = {k:v for k,v in args.items() if v is not None}
        item = Item.query.filter_by(id=item_id, order_id=order_id)
        if item.first().order.deadline < datetime.utcnow():
            abort(422, message="The order is expired, so no items can be modified")
        item.update(args)
        db.session.commit()
        return item.first().serialize
