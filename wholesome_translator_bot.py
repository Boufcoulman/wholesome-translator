"""Discord bot that interacts with the Wholesome discord."""
import logging
import asyncio
import toml

import discord

import bing

log = logging.getLogger(__name__)
log.addHandler(logging.StreamHandler())

var_path = "config.toml"
try:
    config_vars = toml.load(var_path)
except FileNotFoundError:
    print("File {0} not found :(.)".format(var_path))
    raise

TOKEN = config_vars['DISCORD_TOKEN']
MUDAE = config_vars['MUDAE']
POKEMON_CHANNEL = config_vars['POKEMON_CHANNEL']
PSYDUCK_ID = config_vars['PSYDUCK_ID']
KOIKINGU_ID = config_vars['KOIKINGU_ID']
GRRPIN_ID = config_vars['GRRPIN_ID']
BLURRYCOP_ID = config_vars['BLURRYCOP_ID']
VIPS = config_vars['VIPS']
CAPS_CHAN = config_vars['CAPS_CHAN']
LANG_CHANS = config_vars['LANG_CHANS']
PRES_CHAN = config_vars['PRES_CHAN']


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
        hearts_on_presentation(message),
    ])


@client.event
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


async def hearts_on_presentation(message):
    """Add heart reactions in presentation channel.

    Args:
        message: The message that was just posted on the channel
    """
    if str(message.channel) == str(PRES_CHAN):
        hearts = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤎', '🤍']
        for heart in hearts:
            await message.add_reaction(heart)


async def auto_language_flag(message):
    """Add the flag react in language channels.

    Args:
        message: The message that was just posted on the channel
    """
    if str(message.channel) in LANG_CHANS:
        await message.add_reaction('\U0001f6a9')


async def capital_letters_cop(message):
    """React to uncapitalized messages in spicy_capitals, except for VIP people.

    When people post messages with less than a certain amount of capitalized
    words, we react to them with blurry cop emoji.

    Args:
        message: The message that was just posted on the channel

    """
    if str(message.channel) != CAPS_CHAN or str(message.author) in VIPS:
        return

    words = message.content.split()
    min_count = sum(word.upper() != word for word in words)
    threshold = 0.25

    if min_count / len(words) > threshold:
        blurry_cop_emoji = discord.utils.get(
            client.emojis,
            id=int(BLURRYCOP_ID),
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
