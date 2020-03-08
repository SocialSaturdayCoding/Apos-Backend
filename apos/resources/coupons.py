from datetime import datetime

from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource, abort, reqparse

from apos.extensions import db
from apos.models import Coupon

parser = reqparse.RequestParser()
parser.add_argument('deliverer', type=str, required=True)
parser.add_argument('coupon', type=str, required=True)
parser.add_argument('deadline', type=datetime.fromtimestamp)


class CouponListResource(Resource):
    @jwt_required
    def get(self):
        coupons = Coupon.query.all()
        return [coupon.serialize for coupon in coupons]

    @jwt_required
    def put(self):
        args = parser.parse_args()
        coupon = Coupon(deliverer=args['deliverer'],
                        coupon=args['coupon'],
                        deadline=args['deadline'],
                        creator_id=get_jwt_identity())
        db.session.add(coupon)
        db.session.commit()
        return coupon.serialize, 201


class CouponResource(Resource):
    @jwt_required
    def delete(self, coupon_id):
        coupon = Coupon.query.get(coupon_id)
        if not coupon:
            abort(404, message=f"Coupon {coupon_id} does not exist")
        db.session.delete(coupon)
        db.session.commit()
        return '', 204
