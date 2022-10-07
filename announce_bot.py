"""Script to schedule in order to do recurrent actions.
"""
import requests
import json
import logging
from lib.load_var import get_var
import datetime
import lib.birthday_lib as bd_lib
from discord.ext import commands
import discord
import lib.gtranslate as translate

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

SERVER_ID = get_var('SERVER_ID')
BIRTHDAY_CHAN = get_var('BIRTHDAY_CHAN')
INSPIRE_CHAN = get_var('INSPIRE_CHAN')
BIRTHDAY_DB = get_var('BIRTHDAY_DB')

TOKEN = get_var('DISCORD_TOKEN')
CMD_PREFIX = get_var('CMD_PREFIX', '%')
log.debug('Creating bot...')

# Add intent in order to gather member datas
intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix=CMD_PREFIX, intents=intents)

# Get actual date
today = datetime.date.today()

# If we're on monday, Inspire
INSPIRE = today.weekday() == 0

DATABASE = bd_lib.DateDb(BIRTHDAY_DB)
with DATABASE:
    BD_USERS = DATABASE.get_birthdays(today)
    # Get list of user in current date
    # Get also 29-02 if it's the 28-02 and it's not a leap year
    if today.month == 2 and today.day == 28:
        if (today.year % 4) == 0:
            if (today.year % 100) == 0:
                if (today.year % 400) == 0:
                    leap = True
                else:
                    leap = False
            else:
                leap = True
        else:
            leap = False

        if not leap:
            # Add birthdays of people born a 29 of february
            BD_USERS += DATABASE.get_birthdays(datetime.date(1964, 2, 29))


@bot.event
async def on_ready():
    """Indicate that the bot correctly connected."""
    log.info(f'{bot.user} is connected\n')

    # Targetted server
    server = bot.get_guild(SERVER_ID)

    # Inspire if needed
    if INSPIRE:
        log.debug("Sending inspiring quote...")
        # Get inspiring quote
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']

        inspire_channel = server.get_channel(INSPIRE_CHAN)

        # Original quote
        await inspire_channel.send(quote)

        # Translated quote if translation is working
        quote_translation = translate.translate(quote, 'fr')
        if quote_translation is not None:
            await inspire_channel.send(quote_translation.msg)
        log.info("Inspiration delivered.")

    # Greetings for birthdays if needed
    if BD_USERS:
        log.info("Greeting birthdays...")

        bd_chan = server.get_channel(BIRTHDAY_CHAN)

        # Get user to mention
        user_mentions = [server.get_member(id).mention for id in BD_USERS]

        # Creating the message to send
        greeting_base = ("Aujourd'hui n'est pas n'importe quel jour puisque "
                         "c'est l'anniversaire de ")
        greeting_end = """ !!!\nJoyeux anniversaire 🎉✨🌈🎊🎂💖"""

        # User string depends on number of birthdays
        user_string = user_mentions[0]
        if len(BD_USERS) > 1:
            for user in user_mentions[1:-1]:
                user_string += f', {user}'
            user_string += f' et {user_mentions[-1]}'

        # Send happy birthday !
        await bd_chan.send(greeting_base + user_string + greeting_end)

        log.info("Happy birthdays delivered.")

    log.info("End of script.")
    await bot.close()

# If needed, connect the bot
if INSPIRE or BD_USERS:
    log.info('Starting bot...')
    bot.run(TOKEN)
else:
    log.info('Nothing to do. End of script.')
