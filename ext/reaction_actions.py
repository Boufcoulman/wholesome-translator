import lib.bing as bing
from discord.ext import commands


bingtranslate = bing.BingTranslate()


class ReactionsCog(commands.Cog, name="Bot reactions actions"):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """Triggered every time a reaction is added.

        Args:
            payload : RawReactionActionEvent containing reaction infos
        """
        # Keep the bot from triggering himself
        if payload.user_id == self.bot.user.id:
            return

        # If reaction is the red flag ':triangular_flag_on_post:'
        if ascii(payload.emoji.name) == r"'\U0001f6a9'":

            # Message source
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            src_msg = message.content

            # Getting translation infos
            translation, src_lang = bingtranslate.translate(src_msg, 'fr')

            # Send traduction to private message of the user reacting
            user = await self.bot.fetch_user(payload.user_id)
            await user.create_dm()
            await user.dm_channel.send(
                f"'{src_msg}'\ntraduit du {src_lang} en\n'{translation}'",
            )


def setup(bot):
    bot.add_cog(ReactionsCog(bot))
