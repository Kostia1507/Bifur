import io
from datetime import datetime, timedelta
from enum import Enum

import discord
from discord import app_commands
from discord.ext import commands, tasks


class Connect4Difficult(Enum):
    EASY = 2
    NORMAL = 4
    HARD = 6


from utils import commandUtils
from cogs import LogCog
from models.FourInRowGame import FourInRowGame

numbers = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
arrows = ["⬅", "⬆", "⬇", "➡"]
numbersContent = [":one:", ":two:", ":three:", ":four:", ":five:", ":six:", ":seven:", ":eight:", ":nine:"]


class GamesCog(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.rowGames = []
        self.checkNotFinishedGames.start()
        LogCog.logSystem("Games Cog loaded")

    @commands.command()
    @commands.check(commandUtils.is_owner)
    async def checkgames(self, ctx):
        await ctx.send(f"Всього об'єктів Connect4: {len(self.rowGames)}\n")

    @commands.command(aliases=['4inrow', 'connect4'])
    async def fourinrow(self, ctx, user: discord.User, *args):
        height = 6
        width = 7
        if len(args) >= 2:
            height = max(min(int(args[0]), 9), 4)
            width = max(min(int(args[1]), 9), 4)
        elif len(args) == 1:
            height = max(min(int(args[0]), 9), 4)
        if user.id != self.bot.user.id:
            game = FourInRowGame(width, height, players=[ctx.author.id, user.id])
            game.startText = f'Blue: {user.name}\nRed: {ctx.author.name}\n'
        else:
            # User started game against Bifur
            # Let him make first move
            game = FourInRowGame(width, height, players=[user.id, ctx.author.id])
            game.startText = f'Blue: {ctx.author.name}\nRed: {user.name}\n'
        msg = await ctx.send(content=game.printBoard())
        for i in range(0, game.width):
            await msg.add_reaction(numbers[i])
        game.messageId = msg.id
        game.channelId = msg.channel.id
        LogCog.logSystem(f'start conneсt4 at {game.lastIterated} with messageId {game.messageId}')
        self.rowGames.append(game)

    @app_commands.command(name="connect4", description="Challenge your friends in Connect 4")
    @app_commands.describe(opponent="Friend to play with. Choose Bifur to play against him")
    @app_commands.describe(difficult="Choose difficult if you playing against Bifur")
    async def connectSlash(self, interaction: discord.Interaction, opponent: discord.User,
                           difficult: Connect4Difficult = Connect4Difficult.NORMAL):
        await interaction.response.defer(thinking=True)
        if opponent.id != self.bot.user.id:
            game = FourInRowGame(7, 6, players=[interaction.user.id, opponent.id])
            game.startText = f'Blue: {opponent.name}\nRed: {interaction.user.name}\n'
        else:
            game = FourInRowGame(7, 6, players=[opponent.id, interaction.user.id])
            game.startText = f'Blue: {interaction.user.name}\nRed: {opponent.name}: {difficult.name}\n'
            game.difficult = difficult.value
        msg = await interaction.followup.send(content=game.printBoard())
        for i in range(0, game.width):
            await msg.add_reaction(numbers[i])
        game.messageId = msg.id
        game.channelId = msg.channel.id
        LogCog.logSystem(f'start conneсt4 at {game.lastIterated} with messageId {game.messageId} from slash command')
        self.rowGames.append(game)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, event):
        # connect 4 check
        for i in range(0, len(numbers)):
            if numbers[i] == event.emoji.name:
                for game in self.rowGames:
                    if game.messageId == event.message_id:
                        msg = await self.bot.get_channel(event.channel_id).fetch_message(game.messageId)
                        game.makeMove(event.user_id, i)
                        ret = game.isEnd()
                        if ret == 0 and self.bot.user.id in game.players:
                            game.makeBotMove(self.bot.user.id)
                            ret = game.isEnd()
                        text = game.printBoard()
                        if ret == 1:
                            text += '\nRed won'
                            self.rowGames.remove(game)
                        if ret == 2:
                            text += '\nBlue won'
                            self.rowGames.remove(game)
                        if ret == 3:
                            text += '\nDraw'
                            self.rowGames.remove(game)
                        await msg.edit(content=text)
                        await msg.remove_reaction(numbers[i], await self.bot.fetch_user(event.user_id))
                        if ret != 0:
                            history_buffer = await game.animate_history()
                            history_gif = discord.File(history_buffer, filename=f'{game.messageId}history.gif')
                            await msg.reply(file=history_gif)
                        break

    @tasks.loop(minutes=11)
    async def checkNotFinishedGames(self):
        hour = datetime.utcnow().hour
        for game in self.rowGames:
            spHour = hour
            if hour < game.lastIterated:
                spHour += 24
            if spHour - game.lastIterated >= 2:
                # гру потрібно видалити
                msg = await self.bot.get_channel(game.channelId).fetch_message(game.messageId)
                text = game.printBoard()
                if game.move % 2 == 0:
                    text += '\nBlue won. Game finished!'
                else:
                    text += '\nRed won. Game finished!'
                await msg.edit(content=text)
                history_buffer = await game.animate_history()
                history_gif = discord.File(history_buffer, filename=f'{game.messageId}history.gif')
                await msg.reply(file=history_gif)
                self.rowGames.remove(game)
