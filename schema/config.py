from asyncqlio.orm.schema.column import Column
from asyncqlio.orm.schema.table import table_base
from asyncqlio.orm.schema.types import BigInt, Boolean, Text

Table = table_base()


class Guild(Table):
    id = Column(BigInt, primary_key=True)
    cog_blacklist = Column(Text)
    welcome = Column(Text)
    farewell = Column(Text)
    prefix = Column(Text)
    twitter = Column(Boolean)


class Member(Table):
    guild_id = Column(BigInt, primary_key=True)
    id = Column(BigInt, primary_key=True)
    plonked = Column(Boolean)


class Channel(Table):
    id = Column(BigInt, primary_key=True)
    guild_id = Column(BigInt)
    plonked = Column(Boolean)
