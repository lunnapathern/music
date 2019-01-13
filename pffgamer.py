import random
import discord
import asyncio
import requests
import json
import time
import datetime
import safygiphy
import os

g = safygiphy.Giphy()
start_time = {"start_time1": time.time()}
color = 0xc017b6


client = discord.Client()


cor = {'000000000000000000': {'color': '0x00000'}}



@client.event
async def on_ready():
    print(client.user.name)
    print('Logged in as ---->', client.user)
    print('ID:', client.user.id)
    print("Servidores: {} Serves".format(str(len(client.servers))))
    while True:
        await client.change_presence(game=discord.Game(name="{} Usuários 💜".format(str(len(set(client.get_all_members())))), type=1, url='https://www.twitch.tv/robertinhapfaff'), status='streaming')
        await asyncio.sleep(20)

        await client.change_presence(game=discord.Game(name="Vamos conversar? Live no streamcraft 💌", type=1,url='https://www.twitch.tv/robertinhapfaff'), status='streaming')
        await asyncio.sleep(40)

        await client.change_presence(game=discord.Game(name="Oi Gente , Oi Gente ,Oiiii Genteeeee 💋", type=1,url='https://www.twitch.tv/robertinhapfaff'), status='streaming')
        await asyncio.sleep(50)


@client.event
async def on_message(message):
    if message.content.lower().startswith('pf!msg'):
     if message.author.server_permissions.administrator:
        msg = message.content.strip('pf!msg')
        embed2 = discord.Embed(title='📌 Mensagem sendo enviada...', description='`Mensagem escolhida`\n' + (msg),color=color)
        await client.delete_message(message)
        await client.send_message(message.channel, embed=embed2)
        x = list(message.server.members)
        s = 0
        for member in x:
            user = message.author.name
            horario = datetime.datetime.now().strftime("%H:%M:%S")
            embed1 = discord.Embed(title="💜 PFAFFGAMER 💜", url="", color=color,description='**Mensagem nova para você 💌**\n<@{}> \n\n**Aviso:🍧**\n\n**{}**\n'.format(member.id, msg))
            embed1.set_image(url="https://cdn.discordapp.com/attachments/505165436464267295/530184598580363266/Roberta_2.png")
            embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/505165436464267295/530184598580363266/Roberta_2.png")
            embed1.set_footer(text="Enviado por --> {} • Hoje às {}".format(user, horario))
            try:
                await client.send_message(member, embed=embed1)
                print(member.name)
                s += 1
            except:
                pass
        print('\nAviso enviado para {} membros de {}'.format(s, len(x)))
        embed2 = discord.Embed(title='Concluido', color=color,description='\nAviso enviado para **{}** de **{}**'.format(s, len(x)))
        embed2.set_footer(text=message.server.name, icon_url=message.server.icon_url)
        await client.send_message(message.channel, embed=embed2)

@client.event
async def on_member_join(member):
    role1 = "Inscrito(a)"
    role = discord.utils.find(lambda r: r.name == "{}".format(role1), member.server.roles )
    await client.add_roles(member, role)
    embedvindo = discord.Embed(color=color, title='\n',description='\n' + member.mention + '\n• **Seja Bem vindo ao servidor da PFAFFGAMER** <a:partner_2:493067276233342978>\n\n**• Link do canal da Streamcraft**<:Transmitindo:484133030961872898>\n\n**https://streamcraft.com/user/2015336440**\n\n**• Link do canal do Youtube** <:youtube:487449115811381250>\n\n**https://www.youtube.com/user/Pfaffgamer**')
    embedvindo.set_thumbnail(url=member.avatar_url)
    embedvindo.set_image(url="https://cdn.discordapp.com/attachments/499686934700883981/513021860259299329/bem_vindo_robertaaaa.png")
    embedvindo.set_author(name=member.name, icon_url=member.avatar_url)
    embedvindo.set_footer(text=member.name, icon_url=member.avatar_url)
    embedvindo.timestamp = datetime.datetime.utcnow()
    mensagemvindo2 = "🚪bem-vindos🚪"
    bemvindo = discord.utils.find(lambda c: c.name == "{}".format(mensagemvindo2), member.server.channels )
    await client.send_message(bemvindo, embed=embedvindo)



client.run(str(os.environ.get('TOKEN')))
