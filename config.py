from katagawa.kg import Katagawa

from schema.config import Guild


class Config:
    def __init__(self, bot):
        dsn = f'postgresql://beattie:passwd@localhost/config'
        self.db = Katagawa(dsn)
        self.bot = bot
        self.bot.loop.create_task(self.db.connect())

    def __del__(self):
        self.bot.loop.create_task(self.db.close())

    async def get(self, key, default=None):
        async with self.db.get_session() as s:
            query = s.select(Guild).where(Guild.id == key)
            guild = await query.first()
            if guild:
                return {k.name: v for k, v in guild.to_dict().items()}
            else:
                return default

    async def set(self, gid, **kwargs):
        async with self.db.get_session() as s:
            s.merge(Guild(id=gid, **kwargs))

    async def add(self, gid, **kwargs):
        async with self.db.get_session() as s:
            s.add(Guild(id=gid, **kwargs))

    async def remove(self, gid):
        async with self.db.get_session() as s:
            await s.execute(f'delete from guild where id = {gid}')
