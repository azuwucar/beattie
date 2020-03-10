import discord
from discord.ext import menus
from discord.ext.menus import ListPageSource, MenuPages, button


class Paginator(MenuPages):
    """Paginates between a list of embeds."""

    def __init__(self, entries):
        super().__init__(source=PaginatorSource(entries), clear_reactions_after=True)


class PaginatorSource(menus.ListPageSource):
    def __init__(self, entries):
        super().__init__(entries, per_page=1)

    async def send_initial_message(self, ctx, channel):
        return await channel.send(embed=self.entries[0])

    async def format_page(self, menu, entries):
        return self.entries[menu.current_page]
