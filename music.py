import asyncio
import discord
from discord.ext import commands
import datetime
#CRIADO POR ZERO
#CODE FULL COGS MÚSICA

color = 0x0cb4f1

if not discord.opus.is_loaded():


class VoiceEntry:
    def __init__(self, message, player):
        self.requester = message.author
        self.channel = message.channel
        self.player = player

    def __str__(self):
        fmt = '**<a:disco:495599105033109557> Música:**\n{0.title}\n**<:Online:484132926838276096> Música Solicitada Por:**\n{1.display_name}\n'
        duration = self.player.duration
        if duration:
            fmt = fmt + ' **<a:carregando:489775219339165703> Duração da música:**\n{0[0]} **Minutos** / {0[1]} **Segundos**'.format(divmod(duration, 60))
        return fmt.format(self.player, self.requester)

class VoiceState:
    def __init__(self, bot):
        self.current = None
        self.voice = None
        self.bot = bot
        self.play_next_song = asyncio.Event()
        self.songs = asyncio.Queue()
        self.skip_votes = set()
        self.audio_player = self.bot.loop.create_task(self.audio_player_task())

    def is_playing(self):
        if self.voice is None or self.current is None:
            return False

        player = self.current.player
        return not player.is_done()

    @property
    def player(self):
        return self.current.player

    def skip(self):
        self.skip_votes.clear()
        if self.is_playing():
            self.player.stop()

    def toggle_next(self):
        self.bot.loop.call_soon_threadsafe(self.play_next_song.set)

    async def audio_player_task(self):
        while True:
            self.play_next_song.clear()
            self.current = await self.songs.get()
            embed1 = discord.Embed(color=color, description="**• Tocando agora:**\n\n" + str(self.current))
            embed1.set_thumbnail(url="https://cdn.discordapp.com/attachments/510459921054040065/512242135760896012/tumblr_nkd4h5V0a91rzy0w8o1_500.gif")
            embed1.set_footer(text="• Sona 白 🎧  ajuda? digite s!ajuda")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.send_message(self.current.channel,embed=embed1)
            self.current.player.start()
            await self.play_next_song.wait()

class Music:
    def __init__(self, bot):
        self.bot = bot
        self.voice_states = {}

    def get_voice_state(self, server):
        state = self.voice_states.get(server.id)
        if state is None:
            state = VoiceState(self.bot)
            self.voice_states[server.id] = state

        return state

    async def create_voice_client(self, channel):
        voice = await self.bot.join_voice_channel(channel)
        state = self.get_voice_state(channel.server)
        state.voice = voice

    def __unload(self):
        for state in self.voice_states.values():
            try:
                state.audio_player.cancel()
                if state.voice:
                    self.bot.loop.create_task(state.voice.disconnect())
            except:
                pass

    @commands.command(pass_context=True, no_pm=True)
    async def join(self, ctx, *, channel : discord.Channel):
        try:
            await self.create_voice_client(channel)
        except discord.ClientException:
            embed1 = discord.Embed(color=color, description="**• Já estou em um canal de voz!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)
            await self.bot.say(embed=embed1)
        except discord.InvalidArgument:
            embed1 = discord.Embed(color=color, description="**• Este não é um canal de voz!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)
        else:
            await self.bot.say('Pronto para reproduzir audio em ' + channel.name)

    @commands.command(pass_context=True, no_pm=True)
    async def summon(self, ctx):
        summoned_channel = ctx.message.author.voice_channel
        if summoned_channel is None:
            embed1 = discord.Embed(color=color, description="**• Você não esta em um canal de voz!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)
            return False

        state = self.get_voice_state(ctx.message.server)
        if state.voice is None:
            state.voice = await self.bot.join_voice_channel(summoned_channel)
        else:
            await state.voice.move_to(summoned_channel)

        return True

    @commands.command(pass_context=True, no_pm=True)
    async def play(self, ctx, *, song : str):
        state = self.get_voice_state(ctx.message.server)
        opts = {
            'default_search': 'auto',
            'quiet': True,
        }

        if state.voice is None:
            success = await ctx.invoke(self.summon)
            if not success:
                return

        try:
            player = await state.voice.create_ytdl_player(song, ytdl_options=opts, after=state.toggle_next)
        except Exception as e:
            fmt = '• Ocorreu um erro ao processar esta solicitação:{}: {}'
        else:
            player.volume = 0.1
            entry = VoiceEntry(ctx.message, player)
            embed1 = discord.Embed(color=color, description="**• Na Playlist**\n\n" + str(entry))
            embed1.set_footer(text="• Sona 白 🎧 Música 24 horas / Bugs ? relate para o suporte")
            await self.bot.say(embed=embed1)
            await state.songs.put(entry)

    @commands.command(pass_context=True, no_pm=True)
    async def volume(self, ctx, value : int):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.volume = value / 100
            embed1 = discord.Embed(color=color, description="• Volume definido para\n\n **{:.0%}**".format(player.volume))
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)

    @commands.command(pass_context=True, no_pm=True)
    async def pause(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.pause()

    @commands.command(pass_context=True, no_pm=True)
    async def resume(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.is_playing():
            player = state.player
            player.resume()

    @commands.command(pass_context=True, no_pm=True)
    async def stop(self, ctx):
        server = ctx.message.server
        state = self.get_voice_state(server)

        if state.is_playing():
            player = state.player
            player.stop()

        try:
            state.audio_player.cancel()
            del self.voice_states[server.id]
            await state.voice.disconnect()
        except:
            pass

    @commands.command(pass_context=True, no_pm=True)
    async def skip(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if not state.is_playing():
            embed1 = discord.Embed(color=color, description="**• Não esta tocando música agora!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)
            return

        voter = ctx.message.author
        if voter == state.current.requester:
            embed1 = discord.Embed(color=color, description="**• Usuário solicitou pular á música!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)
            state.skip()
        elif voter.id not in state.skip_votes:
            state.skip_votes.add(voter.id)
            total_votes = len(state.skip_votes)
            if total_votes >= 2:
                embed1 = discord.Embed(color=color, description="**• Votação aprovada,pulando a música!**")
                embed1.timestamp = datetime.datetime.utcnow()
                await self.bot.say(embed=embed1)
                state.skip()
            else:
                embed1 = discord.Embed(color=color, description="**• Votação para pular a musica, atualmente em [{}/2]**".format(total_votes))
                embed1.timestamp = datetime.datetime.utcnow()
                await self.bot.say(embed=embed1)
        else:
            embed1 = discord.Embed(color=color,description="**• Você votou para pular esta música!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)

    @commands.command(pass_context=True, no_pm=True)
    async def playing(self, ctx):
        state = self.get_voice_state(ctx.message.server)
        if state.current is None:
            embed1 = discord.Embed(color=color,description="**• Nenhuma musica esta sendo tocada!**")
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)
        else:
            skip_count = len(state.skip_votes)
            embed1 = discord.Embed(color=color,description="**• Tocando agoran\n {} [skips: {}/3]**".format(state.current, skip_count))
            embed1.timestamp = datetime.datetime.utcnow()
            await self.bot.say(embed=embed1)

bot = commands.Bot(command_prefix=commands.when_mentioned_or('ls!'), description='Comandos Teste')
bot.add_cog(Music(bot))


@bot.event
async def on_ready():
    print('Música Online!')
    print('Online Zero ---->', bot.user)
    print('ID:', bot.user.id)


bot.run(str(os.environ.get('TOKEN')))
