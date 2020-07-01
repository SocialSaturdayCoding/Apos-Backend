from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse

from apos.extensions import db
from apos.models import Item, Order

item_create_parser = reqparse.RequestParser()
item_create_parser.add_argument('name', type=str, required=True)
item_create_parser.add_argument('tip_percent', type=int, required=False)
item_create_parser.add_argument('tip_absolute', type=int, required=False)
item_create_parser.add_argument('price', type=int, required=False) # Why is the price false?

item_patch_parser = reqparse.RequestParser()
item_patch_parser.add_argument('name', type=str, required=False)
item_patch_parser.add_argument('tip_percent', type=int, required=False)
item_patch_parser.add_argument('tip_absolute', type=int, required=False)
item_patch_parser.add_argument('price', type=int, required=False)



class ItemListResource(Resource):
    @jwt_required
    def get(self, order_id):
        items = Item.query.filter_by(order_id=order_id).all()
        return [item.serialize for item in items]

    @jwt_required
    def put(self, order_id):
        args = item_create_parser.parse_args()
        order = Order.query.get(order_id)
        if order.deadline < datetime.utcnow():
            abort(422, message="The order is expired, so no items can be added")
        if args.get("tip_absolute", None) and args.get("tip_percent", None):
            abort(422, message="The tip can only be provided in percent OR absolute value")
        item = Item(order_id=order_id, user_id=get_jwt_identity(), **args)
        db.session.add(item)
        db.session.commit()
        return item.serialize, 201


class ItemUserListResource(Resource):
    @jwt_required
    def get(self):
        items = Item.query.filter_by(user_id=get_jwt_identity()).all()
        return [item.serialize for item in items]


class ItemResource(Resource):
    @jwt_required
    def get(self, order_id, item_id):
        item = Item.query.filter_by(order_id=order_id, id=item_id).first()
        if not item:
            abort(404, message=f"Item {item_id} does not exist for order {order_id}")
        return item.serialize

    @jwt_required
    def delete(self, order_id, item_id):
        item = Item.query.filter_by(order_id=order_id, id=item_id).first()
        if not item:
            abort(404, message=f"Item {item_id} does not exist for order {order_id}")
        if item.order.deadline < datetime.utcnow():
            abort(422, message="The order is expired, so no items can be deleted")
        db.session.delete(item)
        db.session.commit()
        return '', 204

    @jwt_required
    def patch(self, order_id, item_id):
        args = item_patch_parser.parse_args()
        args = {k:v for k,v in args.items() if v is not None}
        item = Item.query.filter_by(id=item_id, order_id=order_id).first()
        if item.order.deadline < datetime.utcnow():
            abort(422, message="The order is expired, so no items can be modified")
        item.update(args)
        if item.tip_absolute and item.tip_percent:
            abort(422, message="The tip can only be provided in percent OR a absolute value. Take care that not both are set in the db.")
        db.session.commit()
        return item.serialize
