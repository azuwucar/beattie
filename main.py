import asyncio
import json
import sys

from bot import BeattieBot

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

with open('config.json') as file:
    config = json.load(file)

token = config['token']
prefix = ['>']

bot = BeattieBot(command_prefix=prefix)

for extension in ('default', 'rpg', 'eddb'):
    try:
        bot.load_extension(extension)
    except Exception as e:
        print(f'Failed to load extension {extension}\n{type(e).__name__}: {e}')

bot.run(token)
