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
    async def update(self, ctx, user_info, *date_input) -> None:
        """Add or update the birthday of the specified user

        Args:
            user: the user tag of the birthday person
            date: the birthday date "dd-mm"

        Usage : %bd.update Mudae#0807 27-05
        """
        # Check if the user is valid
        user = self.user_parser(ctx, user_info)
        if not user:
            await ctx.send("Mauvaise utilisation de la commande, "
                           f"l'utilisateur {user_info} n'existe pas.\n"
                           f"Exemple : `{self.bot.command_prefix}bd.update "
                           "Mudae#0807 27-05`\n"
                           "Vérifiez la syntaxe Nom#1234, ou le discord id, "
                           "ou taggez directement la personne @personne !")
            return

        # Check if the date is valid
        date = bd_lib.date_parser(date_input)
        if not date:
            await ctx.send("Le format de date n'est pas reconnu !\n"
                           "Pour ajouter un anniversaire le 20 mars, "
                           "il faut écrire 20-03.")
            return

        # Update database
        bd_lib.update_birthday(user.id, date)
        await ctx.send(f"La date d'anniversaire {date} a été enregistrée pour "
                       f"l'utilisateur {user} !")

    def user_parser(self, ctx, user) -> discord.User:
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

        return found_user

    @ commands.command(name="birthday.list", aliases=["bd.list"])
    async def list(self, ctx) -> None:
        """Display the list of every birthdays registered in the database
        """
        bds = bd_lib.get_all_birthdays()
        list = '\n'.join([
            str(
                ctx.guild.get_member(bd.user_id)
            ) + ' : ' + bd_lib.display_db_date(bd.birthday) for bd in bds
        ])
        await ctx.send("Liste des anniversaires enregistrés :\n"
                       f"{list}")

    @ commands.command(
        name="birthday.delete",
        aliases=["bd.delete", "bd.remove"]
    )
    async def delete(self, ctx, user_info) -> None:
        """Delete targeted user from the birthday database

        Args:
            user: the user tag of the birthday person

        Usage:
            %bd.delete Mudae#0807
        """
        # Check if the user is valid
        user = self.user_parser(ctx, user_info)
        if user:
            # Update database
            bd_lib.remove_birthday(user.id)
            await ctx.send(
                f"L'anniversaire de l'utilisateur {user} a été retiré !"
            )
        else:
            # Yell at discord user
            await ctx.send("Mauvaise utilisation de la commande, "
                           f"l'utilisateur {user_info} n'existe pas.\n"
                           f"Exemple : `{self.bot.command_prefix}bd.delete "
                           "Mudae#0807`\n"
                           "Vérifiez la syntaxe Nom#1234, ou le discord id, "
                           "ou taggez directement la personne @personne !")


def setup(bot):
    """Function run by the bot.load_extension() call from main file
    """
    bot.add_cog(BirthdayCmdCog(bot))
