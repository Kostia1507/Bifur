from datetime import datetime

from discordModels.views.PagedMessageView import PagedMessageView


def initPagedMessage(bot, title, description):
    pagedMessage = PagedMessage(bot)
    pagedMessage.title = title
    pagedMessage.initPages(description)
    return pagedMessage


def setPagedMessage(bot, title, pages):
    pagedMessage = PagedMessage(bot)
    pagedMessage.title = title
    pagedMessage.pages = pages
    return pagedMessage


class PagedMessage:

    def __init__(self, bot):
        self.pages = []
        self.title = ""
        self.messageId = None
        self.channelId = None
        self.imageUrl = None
        self.bot = bot
        self.currentPage = 0
        self.lastIterated = datetime.utcnow().hour
        self.view = PagedMessageView(self)

    def getPage(self, n):
        self.lastIterated = datetime.utcnow().hour
        if n < 0:
            n = 0
        if n >= len(self.pages):
            n = len(self.pages) - 1
        self.currentPage = n
        return self.pages[n]

    def initPages(self, text):
        if text is None or len(text) == 0:
            self.pages.append("")
        else:
            paragraphs = text.split('\n')
            current_paragraph = ""

            n = 0
            for paragraph in paragraphs:
                if len(current_paragraph) + len(paragraph) <= 1800 and n < 18:
                    n += 1
                    if current_paragraph:
                        current_paragraph += "\n" + paragraph
                    else:
                        current_paragraph = paragraph
                else:
                    n = 0
                    self.pages.append(current_paragraph)
                    current_paragraph = paragraph

            if current_paragraph:
                self.pages.append(current_paragraph)
