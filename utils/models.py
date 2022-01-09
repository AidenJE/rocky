from gino import Gino

db = Gino()


class Guild(db.Model):
   __tablename__ = "guilds" 

   id = db.Column(db.BigInteger(), primary_key=True)


class Member(db.Model):
    __tablename__ = "members"

    id = db.Column(db.BigInteger(), primary_key=True)


class GuildMember(db.Model):
    __tablename__ = "guildmembers"

    id = db.Column(db.BigInteger(), primary_key=True, autoincrement=True)
    guild_id = db.Column(db.BigInteger(), db.ForeignKey("members.id"), nullable=False)
    member_id = db.Column(db.BigInteger(), db.ForeignKey("guilds.id"), nullable=False)
