"""Discord bot that interacts with the Wholesome discord."""
import logging
import sys
import traceback

from discord.ext import commands
from lib.load_var import get_var
import discord

from lib.birthday_lib import init_birthday_db

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

TOKEN = get_var('DISCORD_TOKEN')
CMD_PREFIX = get_var('CMD_PREFIX', '%')

log.info('Initialisation de la base de données anniversaire...')
init_birthday_db()

log.debug('Creating bot...')
# Add intent in order to gather member datas
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)

# Commands extensions
initial_extensions = [
    'ext.miscellaneous_commands',
    'ext.translate_commands',
    'ext.birthday_commands',
    'ext.message_actions',
    'ext.reaction_actions',
]


@bot.event
async def on_ready():
    """Indicate that the bot correctly connected."""
    log.info(f'{bot.user} is connected\n')


if __name__ == '__main__':
    # Load of commands extentions
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception:
            print(f'Failed to load extension {extension}.', file=sys.stderr)
            traceback.print_exc()

    log.info('Starting bot...')
    bot.run(TOKEN, reconnect=True)
