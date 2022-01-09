from gino import Gino

db = Gino()


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.BigInteger(), primary_key=True)
