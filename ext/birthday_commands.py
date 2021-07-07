from discord.ext import commands
import re
import lib.birthday_lib as bd_lib


BIRTHDAY_RE = re.compile(r'\d{4}')


class BirthdayCmdCog(commands.Cog, name="Translate bot commands"):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="birthday", aliases=["bd"])
    async def menu(self, ctx) -> None:
        """Get the list of birthday commands
        """
        await ctx.send("Afin d'utiliser le bot d'anniversaire "
                       "ou"
                       )

    @commands.command(name="birthday.update", aliases=["bd.update"])
    async def update(self, ctx, user, date) -> None:
        """Add or update the birthday of the specified user

        Args:
            user: the user tag of the birthday person
            date: the birthday date "mmdd" or "mm-dd"
        """

        await ctx.send(f"Oui voilà user:{user} et date:{date}.")

        # Unified birth date formalism
        birthday = str.replace('-', '')

        # Checker https://dateutil.readthedocs.io/en/stable/parser.html
        # pipenv install python-dateutil
        # from dateutil.parser import parse
        # parse("11 05",dayfirst=True, yearfirst=False)
        # >>> datetime.datetime(2021, 5, 11, 0, 0)

        # Checker ??? https://returns.readthedocs.io/en/latest/#id1

        if BIRTHDAY_RE.match(birthday):
            birthday = date
            await ctx.send("Format mmdd")
        elif ALT_BIRTHDAY_RE.match(date):
            birthday =
            await ctx.send("Format mm-dd")
        else:
            await ctx.send("ça ne fonctionne pas :/")

    @commands.command(name="birthday.list", aliases=["bd.list"])
    async def list(self, ctx) -> None:
        """Certes
        """
        await ctx.send("Oui voilà la liste.")

    @commands.command(name="birthday.delete", aliases=["bd.delete"])
    async def delete(self, ctx, user) -> None:
        """Certes
        """
        await ctx.send(f"Oui voilà à supprimer:{user}.")


def setup(bot):
    """Function run by the bot.load_extension() call from main file
    """
    bot.add_cog(BirthdayCmdCog(bot))
