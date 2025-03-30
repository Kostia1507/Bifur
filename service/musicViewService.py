import discord

from discordModels.views.musicViews import MusicViewBlue, MusicViewGreen, MusicViewGray, MusicViewRed
from service.localeService import getUserLang, getLocaleByLang
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

        userLang = await getUserLang(userId)
        # format message
        t = mp.playing
        if t is not None:
            embed = discord.Embed(
                title=f'{getLocaleByLang("playing", userLang)} {t.name}',
                description=f'{getLocaleByLang("ordered", userLang)} {t.author}\n'
                            f'{getLocaleByLang("duration", userLang)} {t.getDurationToStr()}\n'
                            f'{getLocaleByLang("volume", userLang)} {mp.volume}%\n'
                            f'[Link]({t.original_url})')
            embed.set_thumbnail(url=t.icon_link)

            if len(mp.songs) >= 1 and mp.songs[0] is not None:
                embed.set_footer(text=f"{getLocaleByLang('next', userLang)} {mp.songs[0].name}")
        else:
            embed = discord.Embed(
                title=f'{getLocaleByLang("playing", userLang)} {getLocaleByLang("nothing", userLang)}'
            )
        if isinstance(ctx, discord.Interaction):
            await ctx.followup.send(embed=embed, view=getViewByTheme(mp.theme)(bot=bot, guildId=ctx.guild.id))
            msg = await ctx.original_response()
            mp.musicPlayerMessageId = msg.id
        else:
            msg = await ctx.send(embed=embed, view=getViewByTheme(mp.theme)(bot=bot, guildId=ctx.guild.id))
            mp.musicPlayerMessageId = msg.id
        return True
    else:
        return False


async def updatePlayer(mediaPlayer, bot):
    t = mediaPlayer.playing
    userLang = await getUserLang(mediaPlayer.musicPlayerAuthorId)
    if t is not None:
        embed = discord.Embed(
            title=f'{getLocaleByLang("playing", userLang)} {t.name}',
            description=f'{getLocaleByLang("ordered", userLang)} {t.author}\n'
                        f'{getLocaleByLang("duration", userLang)} {t.getDurationToStr()}\n'
                        f'{getLocaleByLang("volume", userLang)} {mediaPlayer.volume}%\n'
                        f'[Link]({t.original_url})')
        embed.set_thumbnail(url=t.icon_link)

        if len(mediaPlayer.songs) >= 1 and mediaPlayer.songs[0] is not None:
            embed.set_footer(text=f"{getLocaleByLang('next', userLang)} {mediaPlayer.songs[0].name}")
    else:
        embed = discord.Embed(
            title=f'{getLocaleByLang("playing", userLang)} {getLocaleByLang("nothing", userLang)}'
        )

    message = await bot.get_channel(mediaPlayer.musicPlayerChannelId) \
        .fetch_message(mediaPlayer.musicPlayerMessageId)
    await message.edit(embed=embed, view=getViewByTheme(mediaPlayer.theme)(bot, mediaPlayer.guildId))


def getThemeFromStr(query: str):
    query = query.upper().strip()
    if query == "GREY":
        query = "GRAY"
    return getattr(ColorTheme, query, None)


def getViewByTheme(colorTheme):
    if colorTheme == ColorTheme.BLUE:
        return MusicViewBlue.MusicViewBlue
    if colorTheme == ColorTheme.GREEN:
        return MusicViewGreen.MusicViewGreen
    if colorTheme == ColorTheme.RED:
        return MusicViewRed.MusicViewRed
    return MusicViewGray.MusicViewGray
