from datetime import timedelta

from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse, abort

from apos.extensions import db
from apos.models import User

auth_parser = reqparse.RequestParser()
auth_parser.add_argument('username', type=str, required=True)
auth_parser.add_argument('password', type=str, required=True)


class Auth(Resource):
    def post(self):
        args = auth_parser.parse_args()
        user = User.query.filter_by(username=args['username']).first()
        if not user:
            abort(401)
        authorized = user.check_password(args['password'])
        if not authorized:
            abort(401)

        expires = timedelta(days=7)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        return {
                    'token': access_token,
                    'user': user.serialize
                }, 200


class Signup(Resource):
    def post(self):
        args = auth_parser.parse_args()
        user = User(username=args['username'], password=args['password'])
        user.hash_password()
        db.session.add(user)
        db.session.commit()
        return user.serialize, 201
