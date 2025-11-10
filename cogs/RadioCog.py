import asyncio
import random

import discord
from discord import Colour, app_commands
from discord.ext import commands

from cogs import LogCog
from discordModels.views import RadioInfoView
from models.Song import Song
from service import musicService, musicViewService, radioService, pagedMessagesService, cooldownService
from service.localeService import getLocale, getUserLang, getLocaleByLang
from service.musicViewService import createPlayer
from utils import commandUtils


async def connect_to_user_voice(ctx):
    if not ctx.guild.voice_client:
        if ctx.message.author.voice is not None:
            channel = ctx.message.author.voice.channel
            await channel.connect()
            return 1
        else:
            await ctx.send(await getLocale('not-connected-to-voice', ctx.author.id))
            return 0


async def connect_to_user_voiceInteraction(interaction):
    if not interaction.guild.voice_client:
        if interaction.user.voice is not None:
            channel = interaction.user.voice.channel
            await channel.connect()
            return 1
        else:
            await interaction.response.send_message(
                await getLocale('not-connected-to-voice', interaction.user.id), ephemeral=True, delete_after=15)
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
        await musicViewService.createPlayer(ctx, self.bot)
        retStatus = await musicService.startRadio(radio_name, ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def addradio(self, ctx, radio_name):
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        retStatus = await musicService.startRadio(radio_name, ctx.guild.id, ctx.author.name,
                                            ctx.channel.id, ctx.author.id, False)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def radios(self, ctx, *args):
        if len(args) > 0:
            user_id = commandUtils.deleteNotNumbers(args[0])
            radios = await radioService.getSharedPlayLists(user_id)
            user = await self.bot.fetch_user(user_id)
            if user is None:
                await ctx.send(await getLocale('user-not-found', ctx.author.id))
                return
            else:
                title = await getLocale('user-playlists', ctx.author.id).replace("%p", user.name)
        else:
            radios = await radioService.getPlayLists(ctx.author.id)
            title = await getLocale('playlists-list', ctx.author.id)
        if len(radios) == 0:
            await ctx.send(await getLocale('no-playlists', ctx.author.id))
        else:
            res = ''
            radios.sort(key=lambda radioEntry: radioEntry.radio_id)
            for radio in radios:
                res += f'\nID: {radio.radio_id} -- {radio.name}'
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, title, res)
            await ctx.send(view=pagedMsg.view)

    @commands.command(aliases=["rlist", "rl"])
    async def radiolist(self, ctx, radio_name):
        if radio_name[0].isdigit():
            radio = await radioService.getRadioById(radio_name)
        else:
            radio = await radioService.getRadioByName(radio_name, ctx.author.id)
        if radio is None:
            await ctx.send(await getLocale("nothing-found", ctx.author.id))
            return
        ret = await radio.getInfo(ctx.author.id)
        if isinstance(ret, tuple):
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            await ctx.send(view=pagedMsg.view)
        else:
            await ctx.send(ret)

    @commands.command(aliases=['at'])
    async def addtrack(self, ctx, radio_id, url):
        song = Song(url, False)
        await song.updateFromWeb()
        name, duration = song.name, song.duration
        if name is None or duration is None:
            await ctx.message.add_reaction('❌')
            return
        retStatus = await radioService.createTrack(name, radio_id, url, ctx.author.id, duration)
        if retStatus is None:
            await ctx.reply(await getLocale('url-exist', ctx.author.id))
        elif retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.reply(await getLocale('no-playlist', ctx.author.id))

    @commands.command(aliases=['fat'])
    async def forceaddtrack(self, ctx, radio_id, url):
        song = Song(url, False)
        await song.updateFromWeb()
        name, duration = song.name, song.duration
        retStatus = await radioService.forceCreateTrack(name, radio_id, url, ctx.author.id, duration)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.reply(await getLocale('no-playlist', ctx.author.id))

    @commands.command()
    async def deltrack(self, ctx, n: int):
        retStatus = await radioService.deleteTrack(n, ctx.author.id)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def createradio(self, ctx, name):
        if not name[0].isdigit():
            radio_id = await radioService.createRadio(name, ctx.author.id)
            await ctx.send(f'{await getLocale("new-playlist", ctx.author.id)} {radio_id}')
        else:
            await ctx.send(await getLocale("first-not-number", ctx.author.id))

    @commands.command()
    async def share(self, ctx, name):
        shared_status = await radioService.shareRadio(name, ctx.author.id)
        await ctx.send(f'{await getLocale("shared", ctx.author.id)} {shared_status}')

    @commands.command()
    async def rename(self, ctx, radio_id, newname):
        if not newname[0].isdigit():
            radio = await radioService.getRadioById(radio_id)
            await radio.rename(newname, ctx.author.id)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.send(await getLocale("first-not-number", ctx.author.id))

    @commands.command()
    async def allradios(self, ctx):
        radios = await radioService.getAllSharedRadios()
        ret = ''
        for radio in radios:
            ret += f'ID: {radio.radio_id} -- {radio.name}\n'
        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, await getLocale("shared-list", ctx.author.id), ret)
        await ctx.send(view=pagedMsg.view)

    @commands.command()
    async def delradio(self, ctx, radio_id: int):
        radio = await radioService.getRadioById(radio_id)
        retStatus = await radio.delete(ctx.author.id)
        if retStatus:
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command()
    async def tinfo(self, ctx, track_id: int):
        track = await radioService.getTrackById(track_id)
        radio = await radioService.getRadioById(track.radioId)
        userLang = await getUserLang(ctx.author.id)
        if radio.owner == ctx.author.id or radio.is_shared or ctx.author.id in await radio.getEditors():
            track = Song(track.original_url, False)
            await track.updateFromWeb()
            embed = discord.Embed(
                title=f'{track.name} {getLocaleByLang("from-list", userLang)} ID:{radio.radio_id}:{radio.name}',
                description=f'URL: {track.original_url}\n{getLocaleByLang("duration", userLang)} {track.getDurationToStr()}'
            )
            embed.set_thumbnail(url=track.icon_link)
            await ctx.send(embed=embed)
        else:
            await ctx.send(await getLocale("nothing-found", ctx.author.id))

    @commands.command()
    async def rinfo(self, ctx, radio_name):
        if radio_name[0].isdigit():
            radio = await radioService.getRadioById(radio_name)
        else:
            radio = await radioService.getRadioByName(radio_name, ctx.author.id)
        if radio is None:
            await ctx.send(await getLocale("nothing-found", ctx.author.id))
            return
        if radio.owner == ctx.author.id or radio.is_shared or ctx.author.id in await radio.getEditors():
            owner = await self.bot.fetch_user(radio.owner)
            editors = await radio.getEditors()
            EditorsList = ""
            for entry in editors:
                user = await self.bot.fetch_user(entry)
                EditorsList += user.name + "\n"
            tracks = await radio.getTracks(ctx.author.id)
            seconds = 0
            for t in tracks:
                if t.duration is not None:
                    seconds += int(t.duration)
            durationStr = f'{seconds // 3600}:{seconds % 3600 // 60}:{seconds % 60 // 10}{seconds % 60 % 10}'
            while durationStr.startswith('0') or durationStr.startswith(':'):
                durationStr = durationStr[1:len(durationStr)]
            userLang = await getUserLang(ctx.author.id)
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocaleByLang("owner", userLang)} {owner.name}\n'
                            f'{getLocaleByLang("count", userLang)} {len(tracks)}\n'
                            f'{getLocaleByLang("duration", userLang)} {durationStr}\n'
                            f'{getLocaleByLang("shared", userLang)} {radio.is_shared}\n'
                            f'{getLocaleByLang("editors", userLang)} {EditorsList}'
            )
            await ctx.send(embed=embed, view=RadioInfoView.RadioInfoView(self.bot, radio.radio_id))

    @commands.command(aliases=['rradio', 'randomradio'])
    async def randradio(self, ctx):
        radios = await radioService.getAllSharedRadios()
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        radio = random.choice(radios)
        retStatus = await musicService.startRadio(str(radio.radio_id), ctx.guild.id,
                                            ctx.author.name, ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
            owner = await self.bot.fetch_user(radio.owner)
            userLang = await getUserLang(ctx.author.id)
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocaleByLang("owner", userLang)} {owner.name}\n'
                            f'{getLocaleByLang("count", userLang)} {len(await radio.getTracks(ctx.author.id))}\n'
                            f'{getLocaleByLang("shared", userLang)} {radio.is_shared}'
            )
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=['roradio', 'randomownradio'])
    async def randownradio(self, ctx):
        radios = await radioService.getPlayLists(ctx.author.id)
        res = await connect_to_user_voice(ctx)
        if res == 0:
            return 0
        radio = random.choice(radios)
        retStatus = await musicService.startRadio(str(radio.radio_id), ctx.guild.id,
                                            ctx.author.name, ctx.channel.id, ctx.author.id, True)
        if retStatus:
            await ctx.message.add_reaction('✅')
            owner = await self.bot.fetch_user(radio.owner)
            userLang = await getUserLang(ctx.author.id)
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocaleByLang("owner", userLang)} {owner.name}\n'
                            f'{getLocaleByLang("count", userLang)} {len(await radio.getTracks(ctx.author.id))}\n'
                            f'{getLocaleByLang("shared", userLang)} {radio.is_shared}'
            )
            await ctx.send(embed=embed)
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=["edit"])
    async def allowedit(self, ctx, radio_id, *args):
        radio = await radioService.getRadioById(radio_id)
        if radio.owner == ctx.author.id:
            count = 0
            for entry in ctx.message.mentions:
                count += await radio.addEditor(entry.id)
            await ctx.send(f'Added {count} editors')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=["disedit"])
    async def disallowedit(self, ctx, radio_id, *args):
        radio = await radioService.getRadioById(radio_id)
        if radio.owner == ctx.author.id:
            for entry in ctx.message.mentions:
                await radio.removeEditor(entry.id)
            await ctx.message.add_reaction('✅')
        else:
            await ctx.message.add_reaction('❌')

    @commands.command(aliases=['importlist', 'implist'])
    async def importplaylist(self, ctx, link):
        await ctx.message.add_reaction('👋')
        cooldownService.setSpecialCooldown(ctx.author.id)
        radio_id = await radioService.importYouTubePlayList(ctx.author.id, link, 0)
        if radio_id is None:
            await ctx.send("It's not a list. Pass the list with &list parameter in URL")
            cooldownService.removeCooldown(ctx.author.id)
        elif isinstance(radio_id, Exception):
            embed = discord.Embed(title="Exception!", description=str(radio_id), colour=Colour.red())
            await ctx.reply(embed=embed)
            cooldownService.removeCooldown(ctx.author.id)
        else:
            radio = await radioService.getRadioById(radio_id)
            owner = await self.bot.fetch_user(radio.owner)
            userLang = await getUserLang(ctx.author.id)
            embed = discord.Embed(
                title=f'ID:{radio.radio_id}:{radio.name}',
                description=f'{getLocaleByLang("owner", userLang)} {owner.name}\n'
                            f'{getLocaleByLang("count", userLang)} {len(await radio.getTracks(ctx.author.id))}\n'
                            f'{getLocaleByLang("shared", userLang)} {radio.is_shared}'
            )
            await ctx.reply(embed=embed)
            cooldownService.removeCooldown(ctx.author.id)

    @commands.command(aliases=['addlist'])
    async def addplaylist(self, ctx, radio_id, link):
        radio = await radioService.getRadioById(radio_id)
        if radio.owner == ctx.author.id or ctx.author.id in await radio.getEditors():
            await ctx.message.add_reaction('👋')
            cooldownService.setSpecialCooldown(ctx.author.id)
            radio_id = await radioService.importYouTubePlayList(ctx.author.id, link, radio_id)
            if radio_id is None:
                await ctx.send("It's not a list. Pass the list with &list parameter in URL")
                cooldownService.removeCooldown(ctx.author.id)
            elif isinstance(radio_id, Exception):
                embed = discord.Embed(title="Exception!", description=str(radio_id), colour=Colour.red())
                await ctx.reply(embed=embed)
                cooldownService.removeCooldown(ctx.author.id)
            else:
                radio = await radioService.getRadioById(radio_id)
                owner = await self.bot.fetch_user(radio.owner)
                userLang = await getUserLang(ctx.author.id)
                embed = discord.Embed(
                    title=f'ID:{radio.radio_id}:{radio.name}',
                    description=f'{getLocaleByLang("owner", userLang)} {owner.name}\n'
                                f'{getLocaleByLang("count", userLang)} {len(await radio.getTracks(ctx.author.id))}\n'
                                f'{getLocaleByLang("shared", userLang)} {radio.is_shared}'
                )
                await ctx.reply(embed=embed)
                cooldownService.removeCooldown(ctx.author.id)
        else:
            await ctx.message.add_reaction('❌')

    @app_commands.command(name="radio", description="Start playing playlist")
    @app_commands.describe(radio_name="playlist name or ID")
    async def radioSlash(self, interaction: discord.Interaction, radio_name: str):
        await interaction.response.defer()
        res = await connect_to_user_voiceInteraction(interaction)
        if res == 0:
            return 0
        retStatus = await musicService.startRadio(radio_name, interaction.guild_id, interaction.user.name,
                                            interaction.channel_id, interaction.user.id, True)
        if retStatus:
            await createPlayer(interaction, self.bot)
        if not interaction.is_done():
            await interaction.followup.send(await getLocale('ready', interaction.user.id),
                                            ephemeral=True)

    @app_commands.command(name="addradio", description="Add playlist to queue without clearing it")
    @app_commands.describe(radio_name="playlist name or ID")
    async def addradioSlash(self, interaction: discord.Interaction, radio_name: str):
        res = await connect_to_user_voiceInteraction(interaction)
        if res == 0:
            return 0
        retStatus = await musicService.startRadio(radio_name, interaction.guild_id, interaction.user.name,
                                            interaction.channel_id, interaction.user.id, False)
        if retStatus:
            await interaction.response.send_message(await getLocale('ready', interaction.user.id),
                                                    ephemeral=True, delete_after=15)
            await createPlayer(interaction, self.bot)

    @app_commands.command(name="radios", description="Show playlists")
    @app_commands.describe(user="Shows user's playlists if user defined")
    async def radiosSlash(self, interaction: discord.Interaction, user: discord.Member = None):
        if user is not None:
            radios = await radioService.getSharedPlayLists(user.id)
            title = await getLocale('user-playlists', interaction.user.id).replace("%p", user.name)
        else:
            radios = await radioService.getPlayLists(interaction.user.id)
            title = await getLocale('playlists-list', interaction.user.id)
        if len(radios) == 0:
            await interaction.response.send_message(await getLocale('no-playlists', interaction.user.id))
        else:
            res = ''
            radios.sort(key=lambda radioEntry: radioEntry.radio_id)
            for radio in radios:
                res += f'\nID: {radio.radio_id} -- {radio.name}'
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, title, res)
            await interaction.response.send_message(view=pagedMsg.view)

    @app_commands.command(name="allradios", description="Show all shared playlists")
    async def allradiosSlash(self, interaction: discord.Interaction):
        radios = await radioService.getAllSharedRadios()
        ret = ''
        for radio in radios:
            ret += f'ID: {radio[0]} -- {radio[1]}\n'
        pagedMsg = pagedMessagesService.initPagedMessage(self.bot, await getLocale("shared-list", interaction.user.id), ret)
        await interaction.response.send_message(view=pagedMsg.view)

    @app_commands.command(name="radiolist", description="Show tracks in playlist")
    @app_commands.describe(radio_name="playlist name or ID")
    async def radiolistSlash(self, interaction: discord.Interaction, radio_name: str):
        if radio_name[0].isdigit():
            radio = await radioService.getRadioById(radio_name)
        else:
            radio = await radioService.getRadioByName(radio_name, interaction.user.id)
        if radio is None:
            await interaction.response.send_message(await getLocale("nothing-found", interaction.user.id))
            return
        ret = await radio.getInfo(interaction.user.id)
        if isinstance(ret, tuple):
            pagedMsg = pagedMessagesService.initPagedMessage(self.bot, ret[0], ret[1])
            await interaction.response.send_message(view=pagedMsg.view)
        else:
            await interaction.response.send_message(ret)
