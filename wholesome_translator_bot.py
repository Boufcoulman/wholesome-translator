from googletrans import LANGUAGES
from json import loads
import discord
import os
from dotenv import load_dotenv
from operator import add
from functools import reduce
import bing
import re

# Les paramètres sont à placer dans un fichier .env dans le même repertoire que le script, avec le formalisme suivant :
# DISCORD_TOKEN='{bot_token}'
# DISCORD_GUILD='{nom_du_serveur}'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
MUDAE = os.getenv('MUDAE')
POKEMON_CHANNEL = os.getenv('POKEMON_CHANNEL')
PSYDUCK_ID = os.getenv('PSYDUCK_ID')
KOIKINGU_ID = os.getenv('KOIKINGU_ID')
GRRPIN_ID = os.getenv('GRRPIN_ID')
FLOUCOP_ID = os.getenv('FLOUCOP_ID')
VIP = os.getenv('VIP')
MAJ_CHAN = os.getenv('MAJ_CHAN')


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
async def on_message(message):
    '''
    Se déclenche dès qu'un message est posté
    '''
    # Empêche le déclenchement du bot par lui même
    if message.author == client.user:
        return

    # Embête Muade si c'est elle qui a parlé dans le channel pokemon
    if str(message.author) == MUDAE and str(message.channel) == POKEMON_CHANNEL:
        if "psyduck" in message.content.lower():
            koin_emoji = discord.utils.get(client.emojis, id=int(PSYDUCK_ID))
            await message.add_reaction(koin_emoji)

        if "magikarp" in message.content.lower():
            koikingu_emoji = discord.utils.get(client.emojis, id=int(KOIKINGU_ID))
            await message.add_reaction(koikingu_emoji)

        if "uncommon nothing" in message.content:
            grrpin_emoji = discord.utils.get(client.emojis, id=int(GRRPIN_ID))
            await message.add_reaction(grrpin_emoji)

    # Ajoute le drapal sur les messages des channels langue
    language_channels = [
        'chit-chat-in-love-and-joy',
        'charla-en-amor-y-alegria',
        'diskussion-in-liebe-und-freude',
        'worldwide-shitpostingue'
    ]
    if str(message.channel) in language_channels:
        await message.add_reaction('\U0001f6a9')

    # Ajout la police flou si quelqu'un oublie de mettre en majuscule dans le channel majuscule sauf si c'est VIP
    if str(message.channel) == MAJ_CHAN and str(message.author) != VIP:
        words = message.content.strip().split(' ')
        min_count = sum(any(c.islower() for c in s) for s in words)

        if min_count/len(words) > 0.25:
            floucop_emoji = discord.utils.get(client.emojis, id=int(FLOUCOP_ID))
            await message.add_reaction(floucop_emoji)


@ client.event
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


if __name__ == "__main__":
    client.run(TOKEN)
