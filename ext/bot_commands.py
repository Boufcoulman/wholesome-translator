import requests
import json
from discord.ext import commands
import lib.bing as bing
from functools import reduce
from operator import add


bingtranslate = bing.BingTranslate()


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
        """Send list of language aliases for "translate" command 🏳️‍🌈
        """
        returned_table = []
        for code, lang in bing.translate_table.items():
            returned_table.append(f'{lang} : {code}\n')

        returned_table.sort()
        returned_message = reduce(add, returned_table)
        await ctx.author.send(returned_message)

    @commands.command()
    async def translate(self, ctx, lang, *message) -> None:
        """Send translation of specified message in selected language 🏴‍☠️

        Args:
            lang: language code, returned by the 'language' command
            message: the message to translate
        """
        # Stop if bad language code
        if lang not in bing.translate_table:
            await ctx.author.send(
                (f'`{lang}` n\'est pas un code de langue valide.\n'
                 f'Veuillez lancer la commande `{self.bot.command_prefix}'
                 'language` pour obtenir les codes de langage valides.')
            )
            return

        to_translate = ' '.join(message)
        translation, src_lang = bingtranslate.translate(to_translate, lang)
        await ctx.send(translation)


def setup(bot):
    """Function run by the bot.load_extension() call from main file
    """
    bot.add_cog(CommandsCog(bot))
