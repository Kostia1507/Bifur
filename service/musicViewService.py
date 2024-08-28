import discord

from discordModels.views.MusicView import MusicView
from service.localeService import getLocale, getUserLang, getLocaleByLang
from service.musicService import getMusicPlayer


async def createPlayer(ctx, bot):
    mp = getMusicPlayer(ctx.guild.id, ctx.channel.id)
    if mp.musicPlayerMessageId is None:
        mp.musicPlayerChannelId = ctx.channel.id
        if isinstance(ctx, discord.Interaction):
            userId = ctx.user.id
        else:
            userId = ctx.author.id
        mp.musicPlayerAuthorId = userId

        userLang = getUserLang(userId)
        # format message
        t = mp.playing
        if t is not None:
            embed = discord.Embed(
                title=f'{getLocaleByLang("playing", userLang)} {t.name}',
                description=f'{getLocaleByLang("ordered", userLang)} {t.author}\n'
                            f'{getLocaleByLang("duration", userLang)} {t.getDurationToStr()}\n'
                            f'{getLocaleByLang("volume", userLang)} {mp.volume}%')
            embed.set_thumbnail(url=t.icon_link)
            embed.set_footer(text=t.original_url)

            if len(mp.songs) >= 1 and mp.songs[0] is not None:
                embed.description = embed.description + f"\n\n{getLocaleByLang('next', userLang)} {mp.songs[0].name}"
        else:
            embed = discord.Embed(
                title=f'{getLocaleByLang("playing", userLang)} {getLocaleByLang("nothing", userLang)}'
            )
        if isinstance(ctx, discord.Interaction):
            await ctx.response.send_message(embed=embed, view=MusicView(bot=bot))
            msg = await ctx.original_response()
            mp.musicPlayerMessageId = msg.id
        else:
            msg = await ctx.send(embed=embed, view=MusicView(bot=bot))
            mp.musicPlayerMessageId = msg.id


async def updatePlayer(mediaPlayer, bot):
    t = mediaPlayer.playing
    userLang = getUserLang(mediaPlayer.musicPlayerAuthorId)
    if t is not None:
        embed = discord.Embed(
            title=f'{getLocaleByLang("playing", userLang)} {t.name}',
            description=f'{getLocaleByLang("ordered", userLang)} {t.author}\n'
                        f'{getLocaleByLang("duration", userLang)} {t.getDurationToStr()}\n'
                        f'{getLocaleByLang("volume", userLang)} {mediaPlayer.volume}%')
        embed.set_thumbnail(url=t.icon_link)
        embed.set_footer(text=t.original_url)

        if len(mediaPlayer.songs) >= 1 and mediaPlayer.songs[0] is not None:
            embed.description = embed.description + f"\n\n{getLocaleByLang('next', userLang)} {mediaPlayer.songs[0].name}"
    else:
        embed = discord.Embed(
            title=f'{getLocaleByLang("playing", userLang)} {getLocaleByLang("nothing", userLang)}'
        )

    message = await bot.get_channel(mediaPlayer.musicPlayerChannelId) \
        .fetch_message(mediaPlayer.musicPlayerMessageId)
    await message.edit(embed=embed, view=MusicView(bot))
