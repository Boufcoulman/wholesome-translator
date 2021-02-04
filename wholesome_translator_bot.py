from googletrans import LANGUAGES
from json import loads
import discord
import os
from dotenv import load_dotenv
from operator import add
from functools import reduce
import bing

# Les paramètres sont à placer dans un fichier .env dans le même repertoire que le script, avec le formalisme suivant :
# DISCORD_TOKEN='{bot_token}'
# DISCORD_GUILD='{nom_du_serveur}'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
# Permet de definir le nombre de messages à garder en scrutation pour des suppressions notamment
client.max_messages = 5000

bingtranslate = bing.BingTranslate()


@client.event
async def on_ready():
    '''
    Indique que le bot s'est correctement connecté
    '''

    print(
        f'{client.user} is connected\n'
    )


@client.event
async def on_reaction_add(reaction, user):
    '''
    Se déclenche dès qu'un utilisateur ajoute une réaction
    '''
    # Empêche le déclenchement du bot par lui même
    if user == client.user:
        return

    # Si la réaction est le drapeau rouge ":triangular_flag_on_post:"
    if "'\\U0001f6a9'" == ascii(reaction.emoji):

        # Message source
        src_msg = reaction.message.content

        # Récupération des informations de traduction
        translated_text = bingtranslate.translate(src_msg, "fr")
        src_lang = bingtranslate.language(src_msg)[0]

        # Envoie en mp de la traduction
        await user.create_dm()
        await user.dm_channel.send(
            f'"{src_msg}"\ntraduit du "{src_lang.upper()}" en\n"{translated_text}"'
        )


client.run(TOKEN)
