from flask_bcrypt import generate_password_hash, check_password_hash

from extensions import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def hash_password(self):
        self.password = generate_password_hash(self.password).decode('utf8')

    def check_password(self, password):
        return check_password_hash(self.password, password)

    @property
    def serialize(self):
        return {'id': self.id, 'username': self.username}


class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship('User', backref='orders')
    location = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, nullable=False)
    description = db.Column(db.Text, nullable=True)
    title = db.Column(db.String, nullable=False)
    deliverer = db.Column(db.String, nullable=False)
    arrival = db.Column(db.DateTime, nullable=True)


class Item(db.Model):
    __tablename__ = 'items'
    __table_args = (db.UniqueConstraint('order_id', 'user_id'),)

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    order = db.relationship('Order', backref='items')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref='items')
    name = db.Column(db.String, nullable=False)
    # tip in percent
    tip_percent = db.Column(db.Integer, nullable=True)
    # tip in cents
    tip_absolute = db.Column(db.Integer, nullable=True)
    price = db.Column(db.Integer, nullable=True)


class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    creator = db.relationship('User', backref='coupons')
    deliverer = db.Column(db.String, nullable=False)
    coupon = db.Column(db.String, nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)

    @property
    def serialize(self):
        item = {
            'id': self.id,
            'deliverer': self.deliverer,
            'coupon': self.coupon,
        }
        if self.deadline:
            item['deadline'] = str(self.deadline)
        return item