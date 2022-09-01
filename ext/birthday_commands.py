"""Define commands for the birthday management functionalities."""

import re

import discord
from discord.ext import commands

from lib import birthday_lib as bd_lib
from lib.load_var import get_var

USER_TAG_RE = re.compile(r'.*#\d{4}')
USER_ID_RE = re.compile(r'\d{18}')

ZAMI_ROLE = get_var('ZAMI_ROLE')


class BirthdayCmdCog(commands.Cog, name='Birthday commands'):  # type:ignore
    """Commands for managing birthdays."""

    def __init__(self, bot):
        """Injects the bot dependency.

        Args:
            bot: the Discord bot that will run the commands
        """
        self.bot = bot

    @commands.command(name='birthday', aliases=['bd'])
    async def menu(self, ctx) -> None:
        """Get the list of birthday commands.

        Args:
            ctx: message context
        """
        await ctx.send("Afin d'utiliser le bot d'anniversaire vous pouvez"
                       "utiliser les commandes suivantes :\n"
                       "-Ajouter un anniversaire : `bd.add Mudae#0807 11-08`\n"
                       "-Supprimer un anniversaire : `bd.delete Mudae#0807`\n"
                       "-Afficher les anniversaire : `bd.list`")

    @commands.command(name='birthday.update', aliases=['bd.update', 'bd.add'])
    async def update(self, ctx, user_info, *date_input) -> None:
        """Add or update the birthday of the specified user.

        Args:
            ctx: message context
            user_info: the user tag of the birthday person
            date_input: the birthday date "dd-mm"

        Usage : %bd.update Mudae#0807 27-05
        """
        # Exit if it's not from the adequate server
        if ctx.guild.id != get_var('SERVER_ID'):
            await ctx.send(
                "You are not supposed to use this command on "
                f"this server : {str(ctx.guild)}"
            )
            return

        # Exit if the user has not the adequate role
        if ctx.author not in ctx.guild.get_role(ZAMI_ROLE).members:
            await ctx.send(
                "You don't have the adequate role to execute this command."
            )
            return

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
        date = bd_lib.date_parser('-'.join(date_input))
        if not date:
            await ctx.send("Le format de date n'est pas reconnu !\n"
                           "Pour ajouter un anniversaire le 20 mars, "
                           "il faut écrire `20-03` ou `20 mars`.")
            return

        # Update database
        bd_lib.update_birthday(user.id, date)
        await ctx.send(
            f"La date d'anniversaire {bd_lib.display_db_date(date)}"
            f" a été enregistrée pour l'utilisateur {user} !"
        )

    def user_parser(self, ctx, user) -> discord.User:
        """Verify that user exists and returns its discord id.

        Args:
            ctx: message context
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

    @commands.command(name='birthday.list', aliases=['bd.list'])
    async def list(self, ctx) -> None:
        """Display the list of every birthdays registered in the database.

        Args:
            ctx: message context
        """
        # Exit if it's not from the adequate server
        if ctx.guild.id != get_var('SERVER_ID'):
            await ctx.send("You are not supposed to use this command on "
                           f"this server : {str(ctx.guild)}")
            return

        bds = bd_lib.get_all_birthdays()
        bds_list = [
            str(
                ctx.guild.get_member(bd.user_id)
            ) + ' : ' + bd_lib.display_db_date(bd.birthday) for bd in bds
        ]
        bds_display = '\n'.join(bds_list)
        await ctx.send("Liste des anniversaires enregistrés :\n"
                       f"{bds_display}")

    @commands.command(
        name="birthday.delete",
        aliases=["bd.delete", "bd.remove"]
    )
    async def delete(self, ctx, user_info) -> None:
        """Delete targeted user from the birthday database.

        Args:
            ctx: message context
            user_info: the user tag of the birthday person

        Usage:
            %bd.delete Mudae#0807
        """
        # Exit if it's not from the adequate server
        if ctx.guild.id != get_var('SERVER_ID'):
            await ctx.send("You are not supposed to use this command on "
                           f"this server : {str(ctx.guild)}")
            return

        # Exit if the user has not the adequate role
        if ctx.author not in ctx.guild.get_role(ZAMI_ROLE).members:
            await ctx.send("You don't have the adequate role to "
                           "execute this command.")
            return

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


async def setup(bot):
    """Enable the commands in the bot.

    Args:
        bot: the bot that will run the commands
    """
    await bot.add_cog(BirthdayCmdCog(bot))
