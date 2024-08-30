import discord

from discordModels.views.musicViews import MusicViewBlue, MusicViewGreen, MusicViewGray, MusicViewRed
from service.localeService import getLocale, getUserLang, getLocaleByLang
from service.musicService import getMusicPlayer
from models.MusicPlayer import ColorTheme


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
            if mp.theme == ColorTheme.BLUE:
                await ctx.response.send_message(embed=embed, view=MusicViewBlue.MusicViewBlue(bot=bot))
            if mp.theme == ColorTheme.GRAY:
                await ctx.response.send_message(embed=embed, view=MusicViewGray.MusicViewGray(bot=bot))
            if mp.theme == ColorTheme.GREEN:
                await ctx.response.send_message(embed=embed, view=MusicViewGreen.MusicViewGreen(bot=bot))
            if mp.theme == ColorTheme.RED:
                await ctx.response.send_message(embed=embed, view=MusicViewRed.MusicViewRed(bot=bot))
            msg = await ctx.original_response()
            mp.musicPlayerMessageId = msg.id
        else:
            if mp.theme == ColorTheme.BLUE:
                msg = await ctx.send(embed=embed, view=MusicViewBlue.MusicViewBlue(bot=bot))
            if mp.theme == ColorTheme.GRAY:
                msg = await ctx.send(embed=embed, view=MusicViewGray.MusicViewGray(bot=bot))
            if mp.theme == ColorTheme.GREEN:
                msg = await ctx.send(embed=embed, view=MusicViewGreen.MusicViewGreen(bot=bot))
            if mp.theme == ColorTheme.RED:
                msg = await ctx.send(embed=embed, view=MusicViewRed.MusicViewRed(bot=bot))
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
    if mediaPlayer.theme == ColorTheme.BLUE:
        await message.edit(embed=embed, view=MusicViewBlue.MusicViewBlue(bot))
    if mediaPlayer.theme == ColorTheme.GREEN:
        await message.edit(embed=embed, view=MusicViewGreen.MusicViewGreen(bot))
    if mediaPlayer.theme == ColorTheme.GRAY:
        await message.edit(embed=embed, view=MusicViewGray.MusicViewGray(bot))
    if mediaPlayer.theme == ColorTheme.RED:
        await message.edit(embed=embed, view=MusicViewRed.MusicViewRed(bot))
