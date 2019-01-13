import discord
import youtube_dl
import datetime
import os

client = discord.Client()

players = {}
color = 0xe081e4

@client.event
async def on_ready():
    print(client.user.name)
    print("===================")

@client.event
async def on_message(message):
    if message.content.startswith('ls!entrar'):
        try:
            channel = message.author.voice.voice_channel
            await client.join_voice_channel(channel)
        except discord.errors.InvalidArgument:
            embed1 = discord.Embed(color=color,description="Desculpe senhor(a) já estou em um canal de voz")
            embed1.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            embed1.timestamp = datetime.datetime.utcnow()
            await client.send_message(message.channel,embed=embed1)
        except Exception as error:
            embed2 = discord.Embed(color=color,description="``{error}``".format(error=error))
            embed2.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            embed2.timestamp = datetime.datetime.utcnow()
            await client.send_message(message.channel,embed=embed2)

    if message.content.startswith('ls!sair'):
        try:
            mscleave = discord.Embed(title="\n",color=color,description="Hey senhor (a) sai do canal de voz e a música parou!")
            mscleave.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            mscleave.timestamp = datetime.datetime.utcnow()
            voice_client = client.voice_client_in(message.server)
            await client.send_message(message.channel, embed=mscleave)
            await voice_client.disconnect()
        except AttributeError:
            mscleave1 = discord.Embed(title="\n",color=color,description="Hey senhor (a) não estou em nenhum canal de voz.")
            mscleave1.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            mscleave1.timestamp = datetime.datetime.utcnow()
            await client.send_message(message.channel,embed=mscleavel1)
        except Exception as Hugo:
            embed3 = discord.Embed(color=color,description="Ein Error: ``{haus}``".format(haus=Hugo))
            embed3.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            embed3.timestamp = datetime.datetime.utcnow()
            await client.send_message(message.channel,embed=embed3)

    if message.content.startswith('ls!tocar'):
        try:
            yt_url = message.content[6:]
            if client.is_voice_connected(message.server):
                try:
                    voice = client.voice_client_in(message.server)
                    players[message.server.id].stop()
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb = discord.Embed(title="\n",color=color)
                    mscemb.add_field(name="Música",inline=True ,value="{}".format(player.title))
                    mscemb.add_field(name="Views",inline=False, value="[]".format(player.views))
                    mscemb.add_field(name="Postado Em",inline=True , value="{}".format(player.uploaded_date))
                    mscemb.add_field(name="Canal",inline=True , value="{}".format(player.uploadeder))
                    mscemb.add_field(name="Duração",inline=True , value="{}".format(player.uploadeder))
                    mscemb.add_field(name="Likes",inline=True , value="{}".format(player.likes))
                    mscemb.add_field(name="Deslikes",inline=True , value="{}".format(player.dislikes))
                    mscemb.set_footer(text=message.server.name, icon_url=message.server.icon_url)
                    mscemb.timestamp = datetime.datetime.utcnow()
                    await client.send_message(message.channel, embed=mscemb)
                except Exception:
                    await client.send_message(message.server, "Error: [{error}]".format(error=e))

            if not client.is_voice_connected(message.server):
                try:
                    channel = message.author.voice.voice_channel
                    voice = await client.join_voice_channel(channel)
                    player = await voice.create_ytdl_player('ytsearch: {}'.format(yt_url))
                    players[message.server.id] = player
                    player.start()
                    mscemb2 = discord.Embed(title="\n",color=color)
                    mscemb2.add_field(name="Música",inline=True ,value="``{}``".format(player.title))
                    mscemb2.add_field(name="Views",inline=False, value="``[]``".format(player.views))
                    mscemb2.add_field(name="Postado",inline=True , value="``{}``".format(player.upload_date))
                    mscemb2.add_field(name="Canal",inline=True ,value="``{}``".format(player.uploader))
                    mscemb2.add_field(name="Duração",inline=True , value="``{}``".format(player.duration))
                    mscemb2.add_field(name="Likes",inline=True , value="``{}``".format(player.likes))
                    mscemb2.add_field(name="Deslikes",inline=True , value="``{}``".format(player.dislikes))
                    mscemb2.set_footer(text=message.server.name, icon_url=message.server.icon_url)
                    mscemb2.timestamp = datetime.datetime.utcnow()
                    await client.send_message(message.channel, embed=mscemb2)
                except SyntaxError:
                    await client.send_message(message.channel, "Error: [{error}]".format(error=error))
        except Exception as e:
            await client.send_message(message.channel, "Error: [{error}]".format(error=e))




    if message.content.startswith('ls!pausa'):
        try:
            mscpause = discord.Embed(title="\n",color=color,description="Música pausada com sucesso!")
            mscpause.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            mscpause.timestamp = datetime.datetime.utcnow()
            await client.send_message(message.channel, embed=mscpause)
            players[message.server.id].pause()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))
    if message.content.startswith('ls!resume'):
        try:
            mscresume = discord.Embed(title="\n",color=color,description="Música retornou a tocar com sucesso senhor (a)!" )
            mscresume.set_footer(text=message.server.name, icon_url=message.server.icon_url)
            mscresume.timestamp = datetime.datetime.utcnow()
            await client.send_message(message.channel, embed=mscresume)
            players[message.server.id].resume()
        except Exception as error:
            await client.send_message(message.channel, "Error: [{error}]".format(error=error))




client.run(str(os.environ.get('TOKEN')))
