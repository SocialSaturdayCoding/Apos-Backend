from faker import Faker

from apos.models import User, Coupon

fake = Faker()

user1 = {
    "id": 1,
    "username": fake.simple_profile()["username"],
    "password": fake.password()
}
user2 = {
    "id": 2,
    "username": "user2",
    "password": "user2pass"
}


def import_data(session):
    user = User(id=user1["id"], username=user1["username"], password=user1["password"])
    user.hash_password()
    session.add(user)
    user = User(id=user2["id"], username=user2["username"], password=user2["password"])
    user.hash_password()
    coupon = Coupon()
    session.add(user)
    session.commit()
