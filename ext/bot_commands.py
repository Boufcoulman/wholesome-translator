import requests
import json
from discord.ext import commands
import lib.gtranslate as gtranslate
from functools import reduce
from operator import add
import discord
import traceback
import sys
from lib.load_var import get_var


# Emojis
emoji_IDs = get_var('emoji_IDs')


class CommandsCog(commands.Cog, name="Bot commands"):
    def __init__(self, bot):
        self.bot = bot

    # Source https://gist.github.com/EvieePy/7822af90858ef65012ea500bcecf1612
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        """The event triggered when an error is raised while invoking a command.
        Parameters
        ------------
        ctx: commands.Context
            The context used for command invocation.
        error: commands.CommandError
            The Exception raised.
        """

        # This prevents any commands with local handlers
        # being handled here in on_command_error.
        if hasattr(ctx.command, 'on_error'):
            return

        # This prevents any cogs with an overwritten
        # cog_command_error being handled here.
        cog = ctx.cog
        if cog:
            if cog._get_overridden_method(cog.cog_command_error) is not None:
                return

        ignored = ()

        # Allows us to check for original exceptions raised and
        # sent to CommandInvokeError.
        # If nothing is found. We keep the exception passed to
        # on_command_error.
        error = getattr(error, 'original', error)

        # Anything in ignored will return and prevent anything happening.
        if isinstance(error, ignored):
            return

        if isinstance(error, commands.CommandNotFound):
            await ctx.author.send(
                "This command doesn't exist.\n"
                "Type %help to get the list of existing commands."
            )

        if isinstance(error, commands.DisabledCommand):
            await ctx.send(f'{ctx.command} has been disabled.')

        elif isinstance(error, commands.NoPrivateMessage):
            try:
                await ctx.author.send(
                    f'{ctx.command} can not be used in Private Messages.'
                )
            except discord.HTTPException:
                pass

        # For this error example we check to see where it came from...
        elif isinstance(error, commands.BadArgument):
            if ctx.command.qualified_name == 'tag list':  # Check if
                # the command being invoked is 'tag list'
                await ctx.send(
                    'I could not find that member. Please try again.'
                )

        else:
            # All other Errors not returned come here.
            # And we can just print the default TraceBack.
            print(
                'Ignoring exception in command {}:'.format(ctx.command),
                file=sys.stderr
            )
            traceback.print_exception(
                type(error), error, error.__traceback__,
                file=sys.stderr
            )

    @commands.command(name='repeat', aliases=['mimic', 'copy'])
    async def do_repeat(self, ctx, *, inp: str):
        """A simple command which repeats your input!
        Parameters
        ------------
        inp: str
            The input you wish to repeat.
        """
        await ctx.send(inp)

    @do_repeat.error
    async def do_repeat_handler(self, ctx, error):
        """A local Error Handler for our command do_repeat.
        This will only listen for errors in do_repeat.
        The global on_command_error will still be invoked after.
        """

        # Check if our required argument inp is missing.
        if isinstance(error, commands.MissingRequiredArgument):
            if error.param.name == 'inp':
                await ctx.send("You forgot to give me input to repeat!")

    @commands.command()
    async def inspire(self, ctx) -> None:
        """Send inspiring quote ☄️
        """
        response = requests.get("https://zenquotes.io/api/random")
        json_data = json.loads(response.text)
        quote = json_data[0]['q'] + " -" + json_data[0]['a']
        await ctx.send(quote + "\n" + gtranslate.translate(quote, 'fr')[0])

    @commands.command()
    async def language(self, ctx) -> None:
        """Send list of language aliases for "translate" command 🏳️‍🌈
        """
        returned_table = []
        for code, lang in gtranslate.translate_table.items():
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
        if lang not in gtranslate.translate_table:
            await ctx.author.send(
                f'`{lang}` n\'est pas un code valide.\n'
                f'Veuillez lancer la commande `{self.bot.command_prefix}'
                'language` pour obtenir les codes de langage.'
            )
            return

        # Stop if message omitted
        if message == ():
            await ctx.author.send(
                'Veuillez indiquer un message à traduire !'
            )
            return

        to_translate = ' '.join(message)
        translation = gtranslate.translate(to_translate, lang)[0]
        await ctx.send(translation)

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


def setup(bot):
    """Function run by the bot.load_extension() call from main file
    """
    bot.add_cog(CommandsCog(bot))
