import discord
from discord import app_commands
from discord.ext import commands

from assets.helparrays import enhelp, uahelp, ruhelp
from service import localeService, pagedMessagesService
from cogs import LogCog

UAhelpPages = {}
ENhelpPages = {}
RUhelpPages = {}

# This cog have a lot of hard coded rubbish which I want to keep here
helpLocales = {
    'docs':
        {
            'en': "All commands here are described like\n"
                  ">roll [?start] [?end] - send random number from start to end. By default, it's 0 and 100\n"
                  "[start] - variable\n"
                  "? - means it's optional\n"
                  "So you can write >roll 10, and it will return random number in range from 0 to 10\n"
                  "All commands start with >, It's command prefix\n"
                  "Change language if you need with >lang [lang]. All available languages: >langs\n"
                  "**Still have a questions? Join to our [Discord](https://discord.gg/2EGkGzDTK5)**\n",
            'ua': "Всі команди описані подібним чином:\n"
                  ">roll [?start] [?end] - відправляє випадкове число від start до end. За замовчанням це 0 і 100\n"
                  "[start] - змінна\n"
                  "? - означає що змінна не обов'язкова\n"
                  "Тому Ви можете написати >roll 10, і отримати випадкове число від 0 до 10\n"
                  "Всі команди починаються з >. Це префікс команд бота\n"
                  "Змінити мову можна завдяки >lang [lang]. Всі доступні мови: >langs\n"
                  "**Задати питання завжди можна в нашому [Discord](https://discord.gg/2EGkGzDTK5)**\n",
            'ru': "Все команды здесь описаны как:\n"
                  ">roll [?start] [?end] - отправление случайного числа от start до end. По умолчанию от 0 до 100\n"
                  "[start] - переменная\n"
                  "? - означает что это не обязательно\n"
                  "Вы можете написать >roll 10, и оно отправит случайное число от 0 до 10\n"
                  "Все команды начинаются с >. Это префикс команд\n"
                  "Если нужно сменить язык, используйте команду >lang [lang]. Поддерживаемые ботом языки: >langs\n"
                  "**Остались вопросы? Присоединяйся к нашему [Discord](https://discord.gg/2EGkGzDTK5)**\n"
        }
}


class DropdownEN(discord.ui.Select):
    def __init__(self, bot):
        options = []
        self.bot = bot
        for key in enhelp.helpEN.keys():
            options.append(discord.SelectOption(label=key))
        super().__init__(placeholder='Select one of them...', min_values=1, max_values=1,
                         options=options, custom_id='persistent_view:help_en')

    async def callback(self, interaction):
        user_selected = self.values[0]
        pagedMsg = pagedMessagesService.setPagedMessage(self.bot, user_selected, ENhelpPages[user_selected])
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await interaction.response.send_message(embed=embed, view=pagedMsg.view, ephemeral=True)


class DropdownUA(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = []
        for key in uahelp.helpUA.keys():
            options.append(discord.SelectOption(label=key))
        super().__init__(placeholder='Виберіть розділ...', min_values=1, max_values=1,
                         options=options, custom_id='persistent_view:help_ua')

    async def callback(self, interaction):
        user_selected = self.values[0]
        pagedMsg = pagedMessagesService.setPagedMessage(self.bot, user_selected, UAhelpPages[user_selected])
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await interaction.response.send_message(embed=embed, view=pagedMsg.view, ephemeral=True)


class DropdownRU(discord.ui.Select):
    def __init__(self, bot):
        self.bot = bot
        options = []
        for key in ruhelp.helpRU.keys():
            options.append(discord.SelectOption(label=key))
        super().__init__(placeholder='Выберите раздел...', min_values=1, max_values=1,
                         options=options, custom_id='persistent_view:help_ru')

    async def callback(self, interaction):
        user_selected = self.values[0]
        pagedMsg = pagedMessagesService.setPagedMessage(self.bot, user_selected, RUhelpPages[user_selected])
        embed = discord.Embed(title=pagedMsg.title, description=pagedMsg.pages[0])
        embed.set_footer(text=f'Page 1 of {len(pagedMsg.pages)}')
        await interaction.response.send_message(embed=embed, view=pagedMsg.view, ephemeral=True)


class HelpView(discord.ui.View):
    def __init__(self, lang, bot):
        self.bot = bot
        super().__init__(timeout=None)
        # Adds the dropdown to our view object.
        if lang == "en":
            self.add_item(DropdownEN(self.bot))
        elif lang == "ua":
            self.add_item(DropdownUA(self.bot))
        elif lang == "ru":
            self.add_item(DropdownRU(self.bot))


class HelpCog(commands.Cog):

    def __init__(self, bot):
        LogCog.logSystem('Help cog loaded')
        self.bot = bot
        # start to init pages
        for part in enhelp.helpEN.keys():
            pages = []
            currentString = ""
            for cmd in enhelp.helpEN[part]:
                if len(cmd['aliases']) > 0:
                    addString = f"Command: {cmd['name']}\nAlliases: {' '.join(cmd['aliases'])}\n-- {cmd['description']}"
                else:
                    addString = f"Command: {cmd['name']}\n{cmd['description']}"
                if len(addString) + len(currentString) > 3500:
                    pages.append(currentString)
                    currentString = addString
                else:
                    currentString += "\n\n" + addString
            pages.append(currentString)
            ENhelpPages[part] = pages

        for part in uahelp.helpUA.keys():
            pages = []
            currentString = ""
            for cmd in uahelp.helpUA[part]:
                if len(cmd['aliases']) > 0:
                    addString = f"Команда: {cmd['name']}\nСиноніми: {' '.join(cmd['aliases'])}\n--\n{cmd['description']}"
                else:
                    addString = f"Команда: {cmd['name']}\n{cmd['description']}"
                if len(addString) + len(currentString) > 3500:
                    pages.append(currentString)
                    currentString = addString
                else:
                    currentString += "\n\n" + addString
            pages.append(currentString)
            UAhelpPages[part] = pages

        for part in ruhelp.helpRU.keys():
            pages = []
            currentString = ""
            for cmd in ruhelp.helpRU[part]:
                if len(cmd['aliases']) > 0:
                    addString = f"Команда: {cmd['name']}\nСинонимы: {' '.join(cmd['aliases'])}\n-- {cmd['description']}"
                else:
                    addString = f"Команда: {cmd['name']}\n{cmd['description']}"
                if len(addString) + len(currentString) > 3500:
                    pages.append(currentString)
                    currentString = addString
                else:
                    currentString += "\n\n" + addString
            pages.append(currentString)
            RUhelpPages[part] = pages
        LogCog.logSystem('Help messages inited')

    @commands.command()
    async def help(self, ctx, *args):
        lang = await localeService.getUserLang(ctx.author.id)
        await ctx.send(helpLocales['docs'][lang], view=HelpView(lang, self.bot))

    @app_commands.command(name="help", description="Shows help message")
    async def helpSlash(self, interaction: discord.Interaction):
        lang = await localeService.getUserLang(interaction.user.id)
        await interaction.response.send_message(helpLocales['docs'][lang], view=HelpView(lang, self.bot))

    @commands.command()
    async def github(self, ctx):
        await ctx.send("https://github.com/Kostia1507/Bifur")
