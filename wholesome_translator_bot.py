from googletrans import LANGUAGES
from json import loads
from requests import get
import discord
import os
from dotenv import load_dotenv

# Les paramètres sont à placer dans un fichier .env dans le même repertoire que le script, avec le formalisme suivant :
# DISCORD_TOKEN='{bot_token}'
# DISCORD_GUILD='{nom_du_serveur}'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

client = discord.Client()
# Permet de definir le nombre de messages à garder en scrutation pour des suppressions notamment
client.max_messages = 5000


@client.event
async def on_ready():
    '''
    Indique que le bot s'est correctement connecté
    '''
    guild = discord.utils.get(client.guilds, name=GUILD)

    print(
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})\n'
    )


@client.event
async def on_reaction_add(reaction, user):
    '''
    Se déclenche dès qu'un utilisateur ajoute une réaction
    '''
    # Ne se déclenche que pour les messages du serveur voulu
    if str(reaction.message.guild) != GUILD:
        return

    # Empêche le déclenchement du bot par lui même
    if user == client.user:
        return

    # Si la réaction est le drapeau rouge ":triangular_flag_on_post:"
    if "'\\U0001f6a9'" == ascii(reaction.emoji):

        # Epuration du message pour l'API google WIP
        epurated_message = reaction.message.content

        # Appel de l'API google
        google_api_base = "https://translate.googleapis.com/translate_a/single?client=gtx&dt=t&sl=auto&tl=fr&q="
        request_result = get(google_api_base + epurated_message)

        # Récupération des informations de traduction
        translated_text = loads(request_result.text)
        src_msg = reaction.message.content
        src_lang = LANGUAGES[translated_text[2]]
        fr_trad = translated_text[0][0][0]

        # Envoie en mp de la traduction
        await user.create_dm()
        await user.dm_channel.send(f'"{src_msg}"\ntraduit du "{src_lang.capitalize()}" en\n"{fr_trad.capitalize()}"')


client.run(TOKEN)
