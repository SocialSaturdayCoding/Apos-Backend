from flask import Flask, jsonify, request, abort

app = Flask(__name__)
app.config.from_object('config.Config')
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False

from models import User, Item, Order, Coupon
from extensions import db

db.init_app(app)


@app.route('/api/v1/coupons', methods=['GET'])
def list_coupons():
    coupons = Coupon.query.all()
    return jsonify([coupon.serialize for coupon in coupons])


@app.route('/api/v1/coupons', methods=['PUT'])
def create_coupon():
    if not request.json:
        abort(400)
    if 'deliverer' not in request.json or type(request.json['deliverer']) != str:
        abort(400)
    if 'coupon' not in request.json or type(request.json['coupon']) != str:
        abort(400)
    coupon = Coupon(deliverer=request.json['deliverer'],
                    coupon=request.json['coupon'],
                    deadline=request.json.get('deadline', None),
                    creator_id=1)
    db.session.add(coupon)
    db.session.commit()
    return coupon.serialize, 201


@app.route('/api/v1/coupons/<int:coupon_id>', methods=['DELETE'])
def delete_coupon(coupon_id):
    coupon = Coupon.query.get(coupon_id)
    if not coupon:
        abort(404)
    db.session.delete(coupon)
    db.session.commit()
    return '', 204


if __name__ == '__main__':
    app.run()
