import discord

from service.TransparertAnimatedGifConverter import TransparentAnimatedGifConverter
from io import BytesIO
from typing import Any, Union

from PIL import ImageDraw, Image
from PIL.Image import Image as IMG


async def animate_history(width, height, history):
    SIZE = 50
    PADDING = 4
    BLUE_COLOR = "#16b1ea"
    RED_COLOR = "#ef1346"

    width, height = width * SIZE, height * SIZE

    frames = [Image.new('RGBA', size=(width, height), color=(0, 0, 0, 0))]
    current_height = []
    for i in range(0, width):
        current_height.append(0)

    for move in range(0, len(history)):
        canvas = frames[-1].copy()
        draw = ImageDraw.Draw(canvas)
        current_color = BLUE_COLOR if move % 2 == 0 else RED_COLOR
        draw.ellipse(
            ((history[move] * SIZE + PADDING, height - (current_height[history[move]] + 1) * SIZE + PADDING),
             ((history[move] + 1) * SIZE - PADDING, height - current_height[history[move]] * SIZE - PADDING)),
            fill=current_color)
        frames.append(canvas)
        current_height[history[move]] = current_height[history[move]] + 1

    frames.append(frames[-1].copy())
    frames.append(frames[-1].copy())

    gif_image, save_kwargs = await __animate_gif(frames)

    buffer = BytesIO()
    gif_image.save(buffer, **save_kwargs)
    buffer.seek(0)

    return buffer


async def __animate_gif(images: list[IMG], durations: Union[int, list[int]] = 100) -> tuple[
    IMG, dict[str, Any]]:
    save_kwargs: dict[str, Any] = {}
    new_images: list[IMG] = []

    for frame in images:
        thumbnail = frame.copy()
        thumbnail_rgba = thumbnail.convert(mode='RGBA')
        thumbnail_rgba.thumbnail(size=frame.size, reducing_gap=3.0)
        converter = TransparentAnimatedGifConverter(img_rgba=thumbnail_rgba)
        thumbnail_p = converter.process()
        new_images.append(thumbnail_p)

    output_image = new_images[0]
    save_kwargs.update(
        format='GIF',
        save_all=True,
        optimize=False,
        append_images=new_images[1:],
        duration=durations,
        disposal=2,  # Other disposals don't work
        loop=0)

    return output_image, save_kwargs


class Connect4HistoryView(discord.ui.View):

    def __init__(self, width, height, history):
        super().__init__(timeout=None)
        self.history = history
        self.width = width
        self.height = height

    @discord.ui.button(label="History", style=discord.ButtonStyle.gray, emoji="📝", row=0)
    async def historyCallback(self, interaction, button):
        await interaction.response.defer(thinking=True)
        history_buffer = await animate_history(self.width, self.height, self.history)
        history_gif = discord.File(history_buffer, filename=f'{interaction.id}-history.gif')
        await interaction.followup.send(file=history_gif)
