# bot.py

import discord
import os
from dotenv import load_dotenv

# Les paramètres sont à placer dans un fichier .env dans le même repertoire que le script, avec le formalisme suivant :
# DISCORD_TOKEN='{bot_token}'
# DISCORD_GUILD='{nom_du_serveur}'
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
CHANNEL = os.getenv('BACKUP_CHANNEL')
USER = os.getenv('TARGET_LOCKED')

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
async def on_message(message):
    '''
    Se déclenche dès qu'un message est posté
    '''
    # Ne se déclenche que pour les messages du serveur voulu
    if str(message.guild) != GUILD:
        return

    # Empêche le déclenchement du bot par lui même
    if message.author == client.user:
        return

    # Si le message vient d'un utilisateur USER donné, le message est répliqué dans le chan textuel CHANNEL donné
    if str(message.author) == USER:
        chan = discord.utils.get(message.guild.channels, name=CHANNEL)
        await chan.send(f'Post "{message.content}" par {message.author} depuis le channel {message.channel}')
        # Affiche le code string des emojis dans le message
        # if any(str(emoji) in message.content for emoji in message.guild.emojis):


@client.event
async def on_message_delete(message):
    '''
    Se déclenche dès qu'un message est supprimé
    '''
    # Ne se déclenche que pour les messages du serveur voulu
    if str(message.guild) != GUILD:
        return

    # Empêche le déclenchement du bot par lui même
    if message.author == client.user:
        return

    # Si le message vient d'un utilisateur USER donné, le message est répliqué dans le chan textuel CHANNEL donné
    if str(message.author) == USER:
        chan = discord.utils.get(message.guild.channels, name=CHANNEL)
        await chan.send(f'Suppression de "{message.content}" par {message.author} depuis le channel {message.channel}')
        # Le message lui est envoyé par mp
        await message.author.create_dm()
        await message.author.dm_channel.send(f'{message.author.name}, tu as supprimé le message "{message.content}". Il avait les réactions {[str(reaction.emoji) for reaction in message.reactions]}. Aussi sous le format {message.reactions} ou encore {[ascii(reaction.emoji) for reaction in message.reactions]} La bise.')

        # Récup le code ascii, il suffit de comparer telle quelle la chaine ensuite : "'\\U0001f6a9'" par exemple
        print([ascii(reaction.emoji) for reaction in message.reactions])

        # Test pour savoir si le drapeau :triangular_flag_on_post: est présent
        if "'\\U0001f6a9'" in [ascii(reaction.emoji) for reaction in message.reactions]:
            await message.author.dm_channel.send('Il\'y avait le drapal')


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

    # Renvoi l'emoji utilisé à l'utilisateur
    await user.create_dm()
    await user.dm_channel.send(f'{reaction.emoji}, lol')

    # Récup le code ascii, il suffit de comparer telle quelle la chaine ensuite : "'\\U0001f6a9'" par exemple
    print(ascii(reaction.emoji))

    if "'\\U0001f6a9'" == ascii(reaction.emoji):
        await user.dm_channel.send('C\'est le drapal')


client.run(TOKEN)
