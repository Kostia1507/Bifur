import random

import discord
from discord.ext import commands

from cogs import LogCog
from models.Song import Song
from service import musicService, musicViewService, radioService, pagedMessagesService
from service.localeService import getLocale
from utils import commandUtils


async def connect_to_user_voice(ctx):
    if not ctx.guild.voice_client:
        if ctx.message.author.voice is not None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            return 1
        else:
            await ctx.send(getLocale('not-connected-to-voice', ctx.author.id))
            return 0


async def connect_to_user_voiceInteraction(interaction):
    if not interaction.guild.voice_client:
        if interaction.user.voice is not None:
            channel = interaction.user.voice.channel
            await channel.connect()
            return 1
        else:
            await interaction.response.send_message(
                getLocale('not-connected-to-voice', interaction.user.id), ephemeral=True, delete_after=15)
            return 0


class RadioCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Radio cog loaded')
        self.bot = bot

    @commands.command()
    async def radio(self, ctx, radio_name):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        retStatus = musicService.startRadio(radio_name, ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
            await musicViewService.createPlayer(ctx)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def addradio(self, ctx, radio_name):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        retStatus = musicService.startRadio(radio_name, ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, False)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def radios(self, ctx, *args):
        if len(args) > 0:
            user_id = commandUtils.deleteNotNumbers(args[0])
            radios = radioService.getSharedPlayLists(user_id)
            user = await self.bot.fetch_user(user_id)
            if user is None:
                await ctx.send(getLocale('user-not-found', ctx.author.id))
                return
            else:
                title = getLocale('user-playlists', ctx.author.id).replace("%p", user.name)
        else:
            radios = radioService.getPlayLists(ctx.author.id)
            title = getLocale('playlists-list', ctx.author.id)
        if len(radios) == 0:
            await ctx.send(getLocale('no-playlists', ctx.author.id))
        else:
            res = ''
            radios.sort(key=lambda radioEntry: radioEntry.radio_id)
            for radio in radios:
                res += f'\nID: {radio.radio_id} -- {radio.name}'
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, title, res)
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command(aliases=["rlist", "rl"])
    async def radiolist(self, ctx, radio_name):
        if radio_name[0].isdigit():
            radio = radioService.getRadioById(radio_name)
        else:
            radio = radioService.getRadioByName(radio_name, ctx.author.id)
        ret = radio.getInfo(ctx.author.id)
        if isinstance(ret, tuple):
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
            embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
            await ctx.send(embed=embed, view=pagedMsg.view)
        else:
            await ctx.send(ret)

    @commands.command(aliases=['at'])
    async def addtrack(self, ctx, radio_id, url):
        song = Song(url, True)
        name, duration = song.name, song.duration
        retStatus = radioService.createTrack(name, radio_id, url, ctx.author.id, duration)
        if retStatus is None:
            await ctx.reply(getLocale('url-exist', ctx.author.id))
        elif retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.reply(getLocale('no-playlist', ctx.author.id))

    @commands.command(aliases=['fat'])
    async def forceaddtrack(self, ctx, radio_id, url):
        song = Song(url, True)
        name, duration = song.name, song.duration
        retStatus = radioService.forceCreateTrack(name, radio_id, url, ctx.author.id, duration)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.reply(getLocale('no-playlist', ctx.author.id))

    @commands.command()
    async def deltrack(self, ctx, n: int):
        retStatus = radioService.deleteTrack(n, ctx.author.id)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def createradio(self, ctx, name):
        if not name[0].isdigit():
            radio_id = radioService.createRadio(name, ctx.author.id)
            await ctx.send(f'{getLocale("new-playlist", ctx.author.id)} {radio_id}')
        else:
            await ctx.send(getLocale("first-not-number", ctx.author.id))

    @commands.command()
    async def share(self, ctx, name):
        shared_status = radioService.shareRadio(name, ctx.author.id)
        await ctx.send(f'{getLocale("shared", ctx.author.id)} {shared_status}')

    @commands.command()
    async def rename(self, ctx, radio_id, newname):
        if not newname[0].isdigit():
            radioService.getRadioById(radio_id).rename(newname, ctx.author.id)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send(getLocale("first-not-number", ctx.author.id))

    @commands.command()
    async def allradios(self, ctx):
        radios = radioService.getAllSharedRadios()
        ret = ''
        for radio in radios:
            ret += f'ID: {radio.radio_id} -- {radio.name}\n'
        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, getLocale("shared-list", ctx.author.id), ret)
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await ctx.send(embed=embed, view=pagedMsg.view)

    @commands.command()
    async def delradio(self, ctx, radio_id: int):
        retStatus = radioService.getRadioById(radio_id).delete(ctx.author.id)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def tinfo(self, ctx, track_id: int):
        track = radioService.getTrackById(track_id)
        radio = radioService.getRadioById(track.radioId)
        if radio.owner == ctx.author.id or radio.is_shared or ctx.author.id in radio.getEditors():
            track = Song(track.original_url, True)
            embed = discord.Embed(
                title=f'{track.name} {getLocale("from-list", ctx.author.id)} ID:{radio.radio_id}:{radio.name}',
                description=f'URL: {track.original_url}\n{getLocale("duration", ctx.author.id)} {track.getDurationToStr()}'
            )
            embed.set_thumbnail(url=track.icon_link)
            await ctx.send(embed=embed)

    @commands.command()
    async def rinfo(self, ctx, radio_name):
        if radio_name[0].isdigit():
            radio = radioService.getRadioById(radio_name)
        else:
            radio = radioService.getRadioByName(radio_name, ctx.author.id)
        if radio.owner == ctx.author.id or radio.is_shared or ctx.author.id in radio.getEditors():
            owner = await self.bot.fetch_user(radio.owner)
            editors = radio.getEditors()
            EditorsList = ""
            for entry in editors:
                user = await self.bot.fetch_user(entry)
                EditorsList += user.name + "\n"
            tracks = radio.getTracks(ctx.author.id)
            seconds = 0
            for t in tracks:
                if t.duration is not None:
                    seconds += int(t[4])
            durationStr = f'{seconds // 3600}:{seconds % 3600 // 60}:{seconds % 60 // 10}{seconds % 60 % 10}'
            while durationStr.startswith('0') or durationStr.startswith(':'):
                durationStr = durationStr[1:len(durationStr)]
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocale("owner", ctx.author.id)} {owner.name}\n'
                            f'{getLocale("count", ctx.author.id)} {len(tracks)}\n'
                            f'{getLocale("duration", ctx.author.id)} {durationStr}\n'
                            f'{getLocale("shared", ctx.author.id)} {radio.is_shared}\n'
                            f'{getLocale("editors", ctx.author.id)} {EditorsList}'
            )
            await ctx.send(embed=embed)

    @commands.command(aliases=['rradio', 'randomradio'])
    async def randradio(self, ctx):
        radios = radioService.getAllSharedRadios()
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        radio = random.choice(radios)
        retStatus = musicService.startRadio(str(radio.radio_id), ctx.guild.id,
                                            ctx.author.name, ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
            owner = await self.bot.fetch_user(radio.owner)
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocale("owner", ctx.author.id)} {owner.name}\n'
                            f'{getLocale("count", ctx.author.id)} {len(radio.getTracks(ctx.author.id))}\n'
                            f'{getLocale("shared", ctx.author.id)} {radio.is_shared}'
            )
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=['roradio', 'randomownradio'])
    async def randownradio(self, ctx):
        radios = radioService.getPlayLists(ctx.author.id)
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        radio = random.choice(radios)
        retStatus = musicService.startRadio(str(radio.radio_id), ctx.guild.id,
                                            ctx.author.name, ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
            owner = await self.bot.fetch_user(radio.owner)
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocale("owner", ctx.author.id)} {owner.name}\n'
                            f'{getLocale("count", ctx.author.id)} {len(radio.getTracks(ctx.author.id))}\n'
                            f'{getLocale("shared", ctx.author.id)} {radio.is_shared}'
            )
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=["edit"])
    async def allowedit(self, ctx, radio_id, *args):
        radio = radioService.getRadioById(radio_id)
        if radio.owner == ctx.author.id:
            count = 0
            for entry in ctx.message.mentions:
                count += radio.addEditor(entry.id)
            await ctx.send(f'Added {count} editors')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=["disedit"])
    async def disallowedit(self, ctx, radio_id, *args):
        radio = radioService.getRadioById(radio_id)
        if radio.owner == ctx.author.id:
            for entry in ctx.message.mentions:
                radio.removeEditor(entry.id)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

