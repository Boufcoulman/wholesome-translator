"""Discord bot that interacts with the Wholesome discord."""
import logging
import os
import asyncio

import discord
from dotenv import load_dotenv

import bing

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())


load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MUDAE = os.getenv('MUDAE')
POKEMON_CHANNEL = os.getenv('POKEMON_CHANNEL')
PSYDUCK_ID = os.getenv('PSYDUCK_ID')
KOIKINGU_ID = os.getenv('KOIKINGU_ID')
GRRPIN_ID = os.getenv('GRRPIN_ID')
FLOUCOP_ID = os.getenv('FLOUCOP_ID')
VIP = os.getenv('VIP')
CAPS_CHAN = os.getenv('CAPS_CHAN')


client = discord.Client()
# Define nomber of message kept in scrutation
client.max_messages = 5000

bingtranslate = bing.BingTranslate()


@client.event
async def on_ready():
    """Indique que le bot s'est correctement connecté."""
    log.info(f'{client.user} is connected\n')


@client.event
async def on_message(message):
    """Se déclenche dès qu'un message est posté.

    Args:
        message: The message that was just posted on the channel
    """
    # Keep the bot from triggering himself
    if message.author == client.user:
        return

    # Handle the calls of on_message actions
    await asyncio.wait([
        poke_react(message),
        auto_language_flag(message),
        capital_letters_cop(message),
    ])


@ client.event
async def on_reaction_add(reaction, user):
    """Se déclenche dès qu'un utilisateur ajoute une réaction.

    Args:
        reaction: the reaction that was added to the bot's message
        user: the user that added the reaction
    """
    # Keep the bot from triggering himself
    if user == client.user:
        return

    # If reaction is the red flag ':triangular_flag_on_post:'
    if ascii(reaction.emoji) == r"'\U0001f6a9'":

        # Message source
        src_msg = reaction.message.content

        # Getting translation infos
        translated_text = bingtranslate.translate(src_msg, 'fr')
        src_lang = bingtranslate.language(src_msg)[0].upper()

        # Send traduction to private message of the user reacting
        await user.create_dm()
        await user.dm_channel.send(
            f"'{src_msg}'\ntraduit du '{src_lang}' en\n'{translated_text}'",
        )


async def auto_language_flag(message):
    """Add the flag react in language channels.

    Args:
        message: The message that was just posted on the channel
    """
    language_channels = [
        'chit-chat-in-love-and-joy',
        'charla-en-amor-y-alegria',
        'diskussion-in-liebe-und-freude',
        'worldwide-shitpostingue',
    ]
    if str(message.channel) in language_channels:
        await message.add_reaction('\U0001f6a9')


async def capital_letters_cop(message):
    """React to uncapitalized messages in spicy_capitals, except for VIP people.

    When people post messages with less than a certain amount of capitalized
    words, we react to them with blurry cop emoji.

    Args:
        message: The message that was just posted on the channel

    """
    if str(message.channel) != CAPS_CHAN or str(message.author) == VIP:
        return

    words = message.content.split()
    min_count = sum(word.upper() != word for word in words)
    threshold = 0.25

    if min_count / len(words) > threshold:
        blurry_cop_emoji = discord.utils.get(
            client.emojis,
            id=int(FLOUCOP_ID),
        )
        await message.add_reaction(blurry_cop_emoji)


async def poke_react(message):
    """Reacts to what Mudae returned from te pokeroulette.

    Args:
        message: The message that was just posted on the channel
    """
    channel = str(message.channel)
    author = str(message.author)

    # Interract with bot Muade if she spoke pokemon channel
    if author != MUDAE or channel != POKEMON_CHANNEL:
        return

    if 'psyduck' in message.content.lower():
        koin_emoji = discord.utils.get(client.emojis, id=int(PSYDUCK_ID))
        await message.add_reaction(koin_emoji)

    if 'magikarp' in message.content.lower():
        koikingu_emoji = discord.utils.get(
            client.emojis,
            id=int(KOIKINGU_ID),
        )
        await message.add_reaction(koikingu_emoji)

    if 'uncommon nothing' in message.content:
        grrpin_emoji = discord.utils.get(client.emojis, id=int(GRRPIN_ID))
        await message.add_reaction(grrpin_emoji)


if __name__ == '__main__':
    client.run(TOKEN)
