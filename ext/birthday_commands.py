"""Define commands for the birthday management functionalities."""

import re

import discord
from discord.ext import commands

from lib import birthday_lib as bd_lib
from lib.load_var import get_var

BIRTHDAY_DB = get_var('BIRTHDAY_DB')

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
        self.database = bd_lib.DateDb(BIRTHDAY_DB)

    @commands.command(name='birthday', aliases=['bd'])
    async def menu(self, ctx) -> None:
        """Get the list of birthday commands.

        Args:
            ctx: message context
        """
        message = """Afin d'utiliser le bot d'anniversaire vous pouvez\
        utiliser les commandes suivantes :
        - Ajouter un anniversaire : `bd.add Mudae#0807 11-08
        - Supprimer un anniversaire : `bd.delete Mudae#0807
        - Afficher les anniversaire : `bd.list `
        """
        await ctx.send(message)

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
            message = f"""You are not supposed to use this command on \
            this server : {ctx.guild}"""
            await ctx.send(message)
            return

        # Exit if the user has not the adequate role
        if ctx.author not in ctx.guild.get_role(ZAMI_ROLE).members:
            await ctx.send(
                "You don't have the adequate role to execute this command.",
            )
            return

        # Check if the user is valid
        user = self.user_parser(ctx, user_info)
        if not user:
            cmd_prefix = self.bot.command_prefix
            message = f"""Mauvaise utilisation de la commande, \
            l'utilisateur {user_info} n'existe pas.
            Exemple : `{cmd_prefix}bd.update Mudae#0807 27-05`
            Vérifiez la syntaxe Nom#1234, ou le discord id, \
            ou taggez directement la personne @personne !"""
            await ctx.send(message)
            return

        # Check if the date is valid
        date = bd_lib.date_parser('-'.join(date_input))
        if not date:
            message = """Le format de date n'est pas reconnu !
            Pour ajouter un anniversaire le 20 mars, \
            il faut écrire `20-03` ou `20 mars`."""
            await ctx.send(message)
            return

        # Update database
        with self.database as database:
            database.update_birthday(user.id, date)

        message = """La date d'anniversaire {0} a été enregistrée \
        pour l'utilisateur {1} !"""

        await ctx.send(message.format(bd_lib.display_db_date(date), user))

    def user_parser(self, ctx, user) -> discord.User | None:
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
        found_user: discord.User | None = None
        if id_match:
            # Try to found user with parsed id
            found_user = discord.utils.get(
                ctx.guild.members,
                id=int(id_match.group(0)),
            )
        elif tag_match:
            name, discriminator = tag_match.group(0).split('#')
            # Try to found user with parsed name and discriminator
            found_user = discord.utils.get(
                ctx.guild.members,
                name=name,
                discriminator=discriminator,
            )

        return found_user

    @commands.command(name='birthday.list', aliases=['bd.list'])
    async def list(self, ctx) -> None:
        """Display the list of every birthdays registered in the database.

        Args:
            ctx: message context
        """
        # Exit if it's not from the adequate server
        if ctx.guild.id != get_var('SERVER_ID'):
            message = f"""You are not supposed to use this command on \
            this server : {ctx.guild}"""
            await ctx.send(message)
            return

        with self.database as database:
            bds = database.get_all_birthdays()

        bds_list = (bd.format(ctx.guild.get_member) for bd in bds)
        bds_display = '\n'.join(bds_list)
        message = f"""Liste des anniversaires enregistrés :
        {bds_display}"""
        await ctx.send(message)

    @commands.command(
        name='birthday.delete',
        aliases=['bd.delete', 'bd.remove'],
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
            message = f"""You are not supposed to use this command on \
            this server : {ctx.guild}"""
            await ctx.send(message)
            return

        # Exit if the user has not the adequate role
        if ctx.author not in ctx.guild.get_role(ZAMI_ROLE).members:
            message = "You don't have the role to execute this command."
            await ctx.send(message)
            return

        # Check if the user is valid
        user = self.user_parser(ctx, user_info)
        if user:
            # Update database
            with self.database as database:
                database.remove_birthday(user.id)

            await ctx.send(
                f"L'anniversaire de l'utilisateur {user} a été retiré !",
            )
        else:
            # Yell at discord user
            cmd_prefix = self.bot.command_prefix
            message = f"""Mauvaise utilisation de la commande, \
            l'utilisateur {user_info} n'existe pas.
            Exemple : `{cmd_prefix}bd.delete Mudae#0807`
            Vérifiez la syntaxe Nom#1234, ou le discord id, \
            "ou taggez directement la personne @personne !"""
            await ctx.send(message)


async def setup(bot):
    """Enable the commands in the bot.

    Args:
        bot: the bot that will run the commands
    """
    await bot.add_cog(BirthdayCmdCog(bot))
