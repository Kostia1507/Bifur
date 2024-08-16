import discord

from discordModels.views.MusicView import MusicView
from service.localeService import getLocale
from service.musicService import getMusicPlayer


async def createPlayer(ctx):
    mp = getMusicPlayer(ctx.guild.id, ctx.channel.id)
    if mp.musicPlayerMessageId is None:
        mp.musicPlayerChannelId = ctx.channel.id
        if isinstance(ctx, discord.Interaction):
            userId = ctx.user.id
        else:
            userId = ctx.author.id
        mp.musicPlayerAuthorId = userId

        # format message
        t = mp.playing
        if t is not None:
            embed = discord.Embed(
                title=f'{getLocale("playing", userId)} {t.name}',
                description=f'{getLocale("ordered", userId)} {t.author}\n'
                            f'{getLocale("duration", userId)} {t.getDurationToStr()}\n'
                            f'{getLocale("volume", userId)} {mp.volume}%')
            embed.set_thumbnail(url=t.icon_link)
            embed.set_footer(text=t.original_url)
        else:
            embed = discord.Embed(
                title=f'{getLocale("playing", userId)} {getLocale("nothing", userId)}'
            )
        if isinstance(ctx, discord.Interaction):
            await ctx.response.send_message(embed=embed, view=MusicView(timeout=None))
            msg = await ctx.original_response()
            mp.musicPlayerMessageId = msg.id
        else:
            msg = await ctx.send(embed=embed, view=MusicView(timeout=None))
            mp.musicPlayerMessageId = msg.id


async def updatePlayer(mediaPlayer, bot):
    t = mediaPlayer.playing
    if t is not None:
        embed = discord.Embed(
            title=f'{getLocale("playing", mediaPlayer.musicPlayerAuthorId)} {t.name}',
            description=f'{getLocale("ordered", mediaPlayer.musicPlayerAuthorId)} {t.author}\n'
                        f'{getLocale("duration", mediaPlayer.musicPlayerAuthorId)} {t.getDurationToStr()}\n'
                        f'{getLocale("volume", mediaPlayer.musicPlayerAuthorId)} {mediaPlayer.volume}%')
        embed.set_thumbnail(url=t.icon_link)
        embed.set_footer(text=t.original_url)
    else:
        embed = discord.Embed(
            title=f'{getLocale("playing", mediaPlayer.musicPlayerAuthorId)} {getLocale("nothing", mediaPlayer.musicPlayerAuthorId)}'
        )

    message = await bot.get_channel(mediaPlayer.musicPlayerChannelId) \
        .fetch_message(mediaPlayer.musicPlayerMessageId)
    await message.edit(embed=embed, view=MusicView(timeout=None))