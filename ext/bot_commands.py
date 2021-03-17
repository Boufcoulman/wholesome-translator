import requests
import json
import discord
from discord.ext import commands
import lib.bing as bing


bingtranslate = bing.BingTranslate()


# def get_quote():
#     response = requests.get("https://zenquotes.io/api/random")
#     json_data = json.loads(response.text)
#     quote = json_data[0]['q'] + " -" + json_data[0]['a']
#     return(quote)


# async def inspire(message: discord.message) -> None:
#     """Send inspiring quote if the command $inspire is sent.
#
#     Args:
#         message: The message that was just posted
#     """
#     if message.content.startswith('$inspire'):
#         quote = get_quote()
#         await message.channel.send(quote)


class CommandsCog(commands.Cog, name="Bot commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def inspire(self, ctx) -> None:
        """Send inspiring quote.

        Args:
            message: The message that was just posted
        """
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote)


def setup(bot):
    bot.add_cog(CommandsCog(bot))


async def get_translated(message: discord.message) -> None:
    """Send translation to wanted langage.

    Args:
        message: The message that was just posted
        $translate target_langage content
    """
    pass


def translator(message: discord.message) -> str:
    """Translate content to target langage and return the translation.

    Args:
        message: The message that was just posted
        $translate target_langage content
    """
    pass


# async def command(message: discord.message) -> None:
#     """Handle several commands.
#
#     Args:
#         message: The message that was just posted
#     """
#     commands = {
#         '$inspire': inspire,
#         '$translate': translator,
#         # '$langage': get_langage_codes,
#     }
#
#     # If command starts with one of specified commands, execute it
#     for command, action in commands.items():
#         if message.content.startswith(command):
#             await action(message)
