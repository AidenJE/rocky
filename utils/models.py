from gino import Gino

db = Gino()


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.BigInteger(), primary_key=True)


class MemberJoinLog(db.Model):
    __tablename__ = "memberjoinlogs"

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    member_id = db.Column(db.BigInteger(), db.Foreignkey('members.id'), nullable=False)
    join_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())


class MemberLeaveLog(db.Model):
    __tablename__ = "memberleavelogs"
    
    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    member_id = db.Column(db.BigInteger(), db.ForeignKey('members.id'), nullable=False)
    leave_date = db.Column(db.DateTime(), nullable=False, server_default=db.func.now())
