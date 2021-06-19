import discord
from discord.ext import commands
import lib.gtranslate as translate
import asyncio
from lib.load_var import get_var
import re
from urllib.parse import urlparse
import random

# Channels
POKEMON_CHANNEL = get_var('POKEMON_CHANNEL')
CAPS_CHAN = get_var('CAPS_CHAN')
LANG_CHANS = get_var('LANG_CHANS')
PRES_CHAN = get_var('PRES_CHAN')

# Emojis
emoji_IDs = get_var('emoji_IDs')

# Users
VIPS = get_var('VIPS')
MUDAE = get_var('MUDAE')

EMOJI_RE = re.compile(r'\W*:\w+:\W*')


class MessagesCog(commands.Cog, name="Bot messages actions"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        """Triggered every time a message is posted.
        Various actions are realised depending on content,
        origin chan, author...

        Args:
            message: The message that was just posted on the channel
        """
        # Keep the bot from treating commands, might be useless
        if message.content.startswith(self.bot.command_prefix):
            return

        # Handle the calls of on_message actions
        on_message_handlers = [
            auto_language_flag,
            poke_react,
            capital_letters_cop,
            hearts_on_presentation,
            hearts_on_bisou,
            # hearts_on_jtm,
        ]
        await asyncio.wait(
            [handler(message, self.bot) for handler in on_message_handlers]
        )


async def hearts_on_presentation(message, bot):
    """Add heart reactions in presentation channel.

    Args:
        message: The message that was just posted on the channel
        bot: The bot
    """
    # Keep the bot from triggering himself
    if message.author == bot.user:
        return

    if str(message.channel) == str(PRES_CHAN):
        hearts = ['❤️', '🧡', '💛', '💚', '💙', '💜', '🖤', '🤎', '🤍']
        for heart in hearts:
            await message.add_reaction(heart)


async def auto_language_flag(message, bot):
    """Add the flag react in language channels if the message is not french.

    Args:
        message: The message that was just posted on the channel
        bot: The bot
    """
    if str(message.channel) in LANG_CHANS:

        if EMOJI_RE.match(message.content):
            return

        # Check if there is an url in the phrase
        words = message.content.split()
        if any(is_url(word) for word in words):
            return

        # Add flag only if message not from french
        translation = translate.translate(message.content, 'fr')
        if translation is not None and translation.lang != 'Français':
            await message.add_reaction('\U0001f6a9')


async def capital_letters_cop(message, bot):
    """React to uncapitalized messages in spicy_capitals, except for VIP people.

    When people post messages with less than a certain amount of capitalized
    words, we react to them with blurry cop emoji.

    Args:
        message: The message that was just posted on the channel
        bot: The bot
    """
    # Keep the bot from triggering himself
    if message.author == bot.user:
        return

    if str(message.channel) != CAPS_CHAN:
        return

    if 'bisou' in message.content.lower():
        return

    if message.author.id in VIPS:
        return

    words = message.content.split()
    min_count = sum(is_lowercase(word) for word in words)
    threshold = 0.25

    if min_count / len(words) > threshold:
        await message.add_reaction(get_emoji(emoji_IDs['BLURRYCOP_ID'], bot))


async def hearts_on_bisou(message, bot):
    """React to messages containing "bisou" with full of hearts emojis.

    Args:
        message: The message that was just posted on the channel
        bot: The bot
    """
    # Keep the bot from triggering himself
    if message.author == bot.user:
        return

    if 'bisou' in message.content.lower():
        bisous = random.sample(bisous_pool(bot), 3)
        for bisou in bisous:
            await message.add_reaction(bisou)


async def hearts_on_jtm(message, bot):
    """React to messages containing 'i love you' like sentences with emojis.

    Args:
        message: The message that was just posted on the channel
        bot: The bot
    """
    # Keep the bot from triggering himself
    if message.author == bot.user:
        return

    love_phrases = ["je t'aime", "jtm", "je vous aime"]
    if any(phrase in message.content.lower() for phrase in love_phrases):
        await asyncio.wait(
            [message.add_reaction(bisous) for bisous in bisous_pool(bot)]
        )


async def poke_react(message, bot):
    """Reacts to what Mudae returned from te pokeroulette.

    Args:
        message: The message that was just posted on the channel
        bot: The bot
    """
    # Keep the bot from triggering himself
    if message.author == bot.user:
        return

    channel = str(message.channel)
    author = str(message.author)

    # Interract with bot Muade if she spoke pokemon channel
    if author != MUDAE or channel != POKEMON_CHANNEL:
        return

    reaction_triggers = {
        'psyduck': 'PSYDUCK_ID',
        'magikarp': 'KOIKINGU_ID',
        'uncommon nothing': 'GRRPIN_ID',
        'maintenance': 'GRRPIN_ID',
        'pikachu': 'PIKAWOW_ID',
        'butterfree': 'BRETAGNE_ID'
    }

    for word, emoji_name in reaction_triggers.items():
        await poke_case(word, emoji_name, message, bot)


async def poke_case(word, emoji_name, message, bot):
    """Test if word is in message. If so add reaction identified by emoji_name.

    Args:
        words: The words to test
        emoji_name: The name of the emoji_id of the emoji we want to add.
        message: The message that was just posted on the channel
        bot: The bot
    """
    if word in message.content.lower():
        await message.add_reaction(get_emoji(emoji_IDs[emoji_name], bot))


def get_emoji(emoji_id: int, bot: commands.bot.Bot) -> discord.Emoji:
    """Get the emoji with given id.

    Args:
        emoji_id: ID of the emoji we want to fetch.

    Returns:
        the emoji code
    """
    return discord.utils.get(bot.emojis, id=emoji_id)


def is_url(string: str) -> bool:
    """Check if word should be considered to be a URL. This a simple check only.

    Args:
        string: the string to check for URL

    Returns:
        true if the word has a scheme and a domain
    """
    parsed = urlparse(string)
    return parsed.scheme and parsed.netloc


def is_lowercase(word: str) -> bool:
    """Check if word should be considered lowercase.

    Args:
        word: the string to check for lowercase

    Returns:
        true if the word is lowercase and is not an emoji or a link
    """
    lowercase = word.upper() != word
    emoji = EMOJI_RE.match(word)
    url = is_url(word)
    return lowercase and not emoji and not url


def bisous_pool(bot: commands.bot.Bot) -> list:
    """Return the bisous pool of emojis

    Args:
        bot: The bot

    Returns:
        list of kiss emojis
    """
    bisous = ['🧡', '💛', '💚', '💙', '💜', '🖤', '🤎',
              '🤍', '💕', '💞', '💓', '💗', '💖', '♥️',
              get_emoji(emoji_IDs['LOVE_ID'], bot),
              get_emoji(emoji_IDs['KOIDUCK_ID'], bot),
              get_emoji(emoji_IDs['GHOSTHUG_ID'], bot),
              get_emoji(emoji_IDs['PSYKORGASM_ID'], bot),
              get_emoji(emoji_IDs['BLUSH2_ID'], bot),
              get_emoji(emoji_IDs['BISOU_ID'], bot)]

    return bisous


def setup(bot):
    """Function run by The bot.load_extension() call from main file
    """
    bot.add_cog(MessagesCog(bot))
