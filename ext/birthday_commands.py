from discord.ext import commands
import re
import lib.birthday_lib as bd_lib
import discord


USER_TAG_RE = re.compile(r'.*#\d{4}')
USER_ID_RE = re.compile(r'\d{18}')


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
    async def update(self, ctx, user, *date_input) -> None:
        """Add or update the birthday of the specified user

        Args:
            user: the user tag of the birthday person
            date: the birthday date "dd-mm"

        Usage : %update Mudae#0807 27-05
        """

        await ctx.send(f"Oui voilà user:{user} et date:{date}.")

        if BIRTHDAY_RE.match(birthday):
            birthday = date
            await ctx.send("Format mmdd")
        elif ALT_BIRTHDAY_RE.match(date):
            # birthday =
            await ctx.send("Format mm-dd")
        else:
            await ctx.send("ça ne fonctionne pas :/")

    async def user_parser(self, ctx, user) -> discord.User.id:
        """Verify that user exists and returns it's discord id if so

        Args:
            user: the user to try to find (id or name#discriminator)

        Returns:
            user_id: discord id of the user if found, None otherwise
        """
        id_match = USER_ID_RE.search(user)
        tag_match = USER_TAG_RE.search(user)

        # Check if input user exists
        if id_match:
            # Try to found user with parsed id
            found_user = discord.utils.get(
                ctx.guild.members,
                id=int(id_match.group(0))
            )
        elif tag_match:
            name, discriminator = tag_match.group(0).split('#')
            # Try to found user with parsed name and discriminator
            found_user = discord.utils.get(
                ctx.guild.members,
                name=name,
                discriminator=discriminator
            )
        else:
            found_user = None

        return found_user.id if found_user else None

    @ commands.command(name="birthday.list", aliases=["bd.list"])
    async def list(self, ctx) -> None:
        """Certes
        """
        await ctx.send("Oui voilà la liste.")

    @ commands.command(name="birthday.delete", aliases=["bd.delete"])
    async def delete(self, ctx, user) -> None:
        """Certes
        """
        await ctx.send(f"Oui voilà à supprimer:{user}.")


def setup(bot):
    """Function run by the bot.load_extension() call from main file
    """
    bot.add_cog(BirthdayCmdCog(bot))
