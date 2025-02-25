from datetime import datetime
from enum import Enum

import discord
from discord import app_commands
from discord.ext import commands, tasks

from discordModels.views.LobbyView import LobbyView
from discordModels.views.ReversiView import ReversiView
from discordModels.views.TicTacToeView import TicTacToeView
from discordModels.views.WordleView import WordleView
from discordModels.views.connect4HistoryView import Connect4HistoryView
from models.ReversiGame import ReversiGame
from models.TicTacToeGame import TicTacToeGame
from models.WordleGame import WordleGame


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

    @commands.command()
    async def tictactoe(self, ctx, user: discord.User, *args):
        if user.id != self.bot.user.id:
            game = TicTacToeGame(players=[ctx.author.id, user.id])
            game.startText = f'Blue: {user.name}\nRed: {ctx.author.name}\n'
        else:
            # User started game against Bifur
            # Let him make first move
            game = TicTacToeGame(players=[user.id, ctx.author.id])
            game.ai_game = True
            game.startText = f'Blue: {ctx.author.name}\nRed: {user.name}\n'
        msg = await ctx.send(content=game.startText, view=TicTacToeView(game))
        game.messageId = msg.id
        game.channelId = msg.channel.id
        LogCog.logSystem(f'start TicTacToe at {game.lastIterated} with messageId {game.messageId}')

    @commands.command(aliases=["othello"])
    async def reversi(self, ctx, user: discord.User, *args):
        if user.id != self.bot.user.id:
            game = ReversiGame(players=[user.id, ctx.author.id], players_nicknames=[user.name, ctx.author.name])
        else:
            # User started game against Bifur
            # Let him make first move
            game = ReversiGame(players=[ctx.author.id, user.id], players_nicknames=[ctx.author.name, user.name])
            game.ai_game = True
            game.bot_id = self.bot.user.id
        img = discord.File(game.generate_picture(), "reversi.jpg")
        embed = discord.Embed(title="Reversi", description=game.get_text())
        embed.set_image(url=f'attachment://reversi.jpg')
        msg = await ctx.send(embed=embed, view=ReversiView(self.bot, game), file=img)
        game.messageId = msg.id
        game.channelId = msg.channel.id
        LogCog.logSystem(f'start reversi at {datetime.now()} with messageId {game.messageId}')

    @commands.command(aliases=[])
    async def wordle(self, ctx, *args):
        if len(args) > 0:
            locale = "en" if args[0] not in ["en", "ru", "ua"] else args[0]
        else:
            locale = "en"
        game = WordleGame(ctx.author.id, locale)
        if locale == "ua":
            await ctx.send(content="Напишіть вашу першу здогадку\n"
                                   "Зверніть увагу, що апостроф не рахується за букву!\n"
                                   "Його не потрібно дописувати, а слова об'єм чи сім'я мають всього 4 букви.",
                           view=WordleView(self.bot, game))
        elif locale == "ru":
            await ctx.send(content="Напишите ваше первое слово\n", view=WordleView(self.bot, game))
        else:
            await ctx.send(content="Write your first guess", view=WordleView(self.bot, game))
        LogCog.logSystem(f'start Wordle at {datetime.now()} with messageId {ctx.message.id} for {ctx.author.id}')

    @commands.command(aliases=["bj"])
    async def blackjack(self, ctx, *args):
        await ctx.send(content=f"{ctx.author.display_name} started the game of Blackjack",
                       view=LobbyView(self.bot, "Blackjack", 4, ctx.author.id))
        LogCog.logSystem(f'start Lobby BJ at {datetime.now()} with messageId {ctx.message.id} for {ctx.author.id}')

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
                        if ret != 0:
                            await msg.edit(content=text,
                                           view=Connect4HistoryView(game.width, game.height, game.history))
                        else:
                            await msg.edit(content=text)
                        await msg.remove_reaction(numbers[i], await self.bot.fetch_user(event.user_id))

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
