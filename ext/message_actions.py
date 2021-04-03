import discord
from discord.ext import commands
import lib.bing as bing
import asyncio
from lib.load_var import get_var
import re
from urllib.parse import urlparse
import random


MUDAE = get_var('MUDAE')
POKEMON_CHANNEL = get_var('POKEMON_CHANNEL')
PSYDUCK_ID = get_var('PSYDUCK_ID')
KOIKINGU_ID = get_var('KOIKINGU_ID')
GRRPIN_ID = get_var('GRRPIN_ID')
BLURRYCOP_ID = get_var('BLURRYCOP_ID')
LOVE_ID = get_var('LOVE_ID')
GHOSTHUG_ID = get_var('GHOSTHUG_ID')
VIPS = get_var('VIPS')
CAPS_CHAN = get_var('CAPS_CHAN')
LANG_CHANS = get_var('LANG_CHANS')
PRES_CHAN = get_var('PRES_CHAN')

EMOJI_RE = re.compile(r'\W*:\w+:\W*')

bingtranslate = bing.BingTranslate()


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
        # Keep the bot from triggering himself
        if message.author == self.bot.user:
            return

        # Keep the bot from treating commands, might be useless
        if message.content.startswith(self.bot.command_prefix):
            return

        # Handle the calls of on_message actions
        await asyncio.wait([
            poke_react(message, self.bot),
            auto_language_flag(message),
            capital_letters_cop(message, self.bot),
            hearts_on_presentation(message),
            hearts_on_bisou(message, self.bot),
        ])


def setup(bot):
    bot.add_cog(MessagesCog(bot))


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
    """Add the flag react in language channels if the message is not french.

    Args:
        message: The message that was just posted on the channel
    """
    if str(message.channel) in LANG_CHANS:

        if EMOJI_RE.match(message.content):
            return

        # Check if there is an url in the phrase
        words = message.content.split()
        if any(is_url(word) for word in words):
            return

        # Add flag only if message not from french
        translation, src_lang = bingtranslate.translate(message.content, 'fr')
        if src_lang != 'Français':
            await message.add_reaction('\U0001f6a9')


async def capital_letters_cop(message, bot):
    """React to uncapitalized messages in spicy_capitals, except for VIP people.

    When people post messages with less than a certain amount of capitalized
    words, we react to them with blurry cop emoji.

    Args:
        message: The message that was just posted on the channel
    """
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
        await message.add_reaction(get_emoji(BLURRYCOP_ID, bot))


async def hearts_on_bisou(message, bot):
    """React to messages containing "bisou" with full of hearts emojis.

    Args:
        message: The message that was just posted on the channel
    """
    if 'bisou' in message.content.lower():
        bisous = random.sample(['🧡', '💛', '💚', '💙', '💜', '🖤', '🤎',
                                '🤍', '💕', '💞', '💓', '💗', '💖', '♥️',
                                get_emoji(LOVE_ID, bot),
                                get_emoji(GHOSTHUG_ID, bot)],
                               3)
        for bisou in bisous:
            await message.add_reaction(bisou)


async def poke_react(message, bot):
    """Reacts to what Mudae returned from te pokeroulette.

    Args:
        message: The message that was just posted on the channel
    """
    channel = str(message.channel)
    author = str(message.author)
    body = message.content

    # Interract with bot Muade if she spoke pokemon channel
    if author != MUDAE or channel != POKEMON_CHANNEL:
        return

    if 'psyduck' in body.lower():
        await message.add_reaction(get_emoji(PSYDUCK_ID, bot))

    if 'magikarp' in body.lower():
        await message.add_reaction(get_emoji(KOIKINGU_ID, bot))

    if 'uncommon nothing' in body or 'maintenance' in body:
        await message.add_reaction(get_emoji(GRRPIN_ID, bot))


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
