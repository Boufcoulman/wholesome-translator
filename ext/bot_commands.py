import requests
import json
import discord
from discord.ext import commands
import lib.bing as bing
from functools import reduce
from operator import add


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
        """Send inspiring quote ☄️
        """
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote)

    @commands.command()
    async def language(self, ctx) -> None:
        """Send list of language alias for "translate" command.
        """
        returned_table = []
        for code, lang in bing.translate_table.items():
            returned_table.append(f'{lang} : {code}\n')

        returned_table.sort()
        returned_message = reduce(add, returned_table)
        await ctx.author.send(returned_message)


def setup(bot):
    bot.add_cog(CommandsCog(bot))


async def get_translated(message: discord.message) -> None:
    """Send translation to wanted language.

    Args:
        message: The message that was just posted
        $translate target_language content
    """
    pass


def translator(message: discord.message) -> str:
    """Translate content to target language and return the translation.

    Args:
        message: The message that was just posted
        $translate target_language content
    """
    pass
