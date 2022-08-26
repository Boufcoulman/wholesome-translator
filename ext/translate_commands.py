from discord.ext import commands
import lib.gtranslate as translate
from functools import reduce
from operator import add
from lib.load_var import get_var


# Emojis
emoji_IDs = get_var('emoji_IDs')


class TranslateCmdCog(commands.Cog, name="Translate bot commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def language(self, ctx) -> None:
        """Send list of language aliases for "translate" command 🏳️‍🌈
        """
        returned_table = []
        for code, lang in translate.translate_table.items():
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
        if lang not in translate.translate_table:
            await ctx.author.send(
                f"`{lang}` n'est pas un code valide.\n"
                f"Veuillez lancer la commande `{self.bot.command_prefix}"
                "language` pour obtenir les codes de langage."
            )
            return

        # Stop if message omitted
        if message == ():
            await ctx.author.send(
                'Veuillez indiquer un message à traduire !'
            )
            return

        to_translate = ' '.join(message)
        translation = translate.translate(to_translate, lang)

        # Send translation if it worked
        if translation is not None:
            await ctx.send(translation.msg)
        else:
            await ctx.send(translate.translate_error_msg)

    @translate.error
    async def translate_handler(self, ctx, error):
        """A local Error Handler for our command translate.
        This will only listen for errors in translate.
        The global on_command_error will still be invoked after.
        """

        # Check if an argument is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.author.send(
                "Il manque un bout de la commande !\n"
                "Exemple pour traduire Bisous en allemand :\n"
                "`%translate de Bisous`"
                f" <:love:{emoji_IDs['LOVE_ID']}>"
            )


async def setup(bot):
    """Function run by the bot.load_extension() call from main file
    """
    await bot.add_cog(TranslateCmdCog(bot))
