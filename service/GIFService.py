import aiohttp

from PIL import Image, ImageOps, ImageFont, ImageDraw
from PIL.Image import Image as IMG
from typing import Any, Union
from io import BytesIO

from service.TransparertAnimatedGifConverter import TransparentAnimatedGifConverter


class GifCreator:
    def __init__(self, image_url: str) -> None:
        self.image_url = image_url
        self.max_framesForPat = 10
        self.max_framesForVibe = 151
        self.max_framesForSlap = 151
        self.resolutionPat = (200, 200)
        self.resolutionVibe = (280, 190)
        self.resolutionSlap = (270, 211)
        self.resolutionVibeResult = (320, 190)
        self.frames: list[IMG] = []

    async def create_pat_gif(self):
        img_bytes = await self.__get_image_bytes()

        base = Image.open(img_bytes).convert('RGBA').resize(self.resolutionPat)

        for i in range(self.max_framesForPat):
            squeeze = i if i < self.max_framesForPat / 2 else self.max_framesForPat - i
            width = 0.8 + squeeze * 0.02
            height = 0.8 - squeeze * 0.05
            offsetX = (1 - width) * 0.5 + 0.1
            offsetY = (1 - height) - 0.08

            canvas = Image.new('RGBA', size=self.resolutionPat, color=(0, 0, 0, 0))
            canvas.paste(base.resize((round(width * self.resolutionPat[0]), round(height * self.resolutionPat[1]))),
                         (round(offsetX * self.resolutionPat[0]), round(offsetY * self.resolutionPat[1])))

            pat_hand = Image.open(f'./assets/gifs/pat/pet{i}.gif').convert('RGBA').resize(self.resolutionPat)

            canvas.paste(pat_hand, mask=pat_hand)
            self.frames.append(canvas)

        gif_image, save_kwargs = await self.__animate_gif(self.frames)

        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)

        return buffer

    async def sign_gif(self, messageId, text):
        gif_data = None
        async with aiohttp.ClientSession() as session:
            async with session.get(self.image_url) as response:
                if response.status == 200:
                    gif_data = await response.read()
        with open(f'temp/{messageId}.gif', 'wb') as handler:
            handler.write(gif_data)
        gif = Image.open(f'temp/{messageId}.gif')
        duration = gif.info["duration"]
        current_frame = None
        size = int(gif.size[0] / (len(text) + 2)) * 2
        size = min(size, int(gif.size[0] / 4))
        font = ImageFont.truetype("assets/arial.ttf", size)
        x = (gif.size[0] - font.getsize(text)[0] + 10) / 2
        y = (gif.size[1] - font.getsize(text)[1] - 10)
        while True:
            try:
                current_frame = gif.tell()
                # Create a new image for the current frame
                frame = Image.new("RGBA", gif.size)
                frame.paste(gif.convert("RGBA"))
                draw = ImageDraw.Draw(frame)
                draw.text((x - 2, y - 2), text, fill='black', font=font, align="left")
                draw.text((x - 2, y + 2), text, fill='black', font=font, align="left")
                draw.text((x + 2, y - 2), text, fill='black', font=font, align="left")
                draw.text((x + 2, y + 2), text, fill='black', font=font, align="left")
                draw.text((x, y), text, fill='white', font=font, align="left")
                self.frames.append(frame)
                # Move to the next frame
                gif.seek(current_frame + 1)
            except EOFError:
                break
        if current_frame is not None:
            gif_image, save_kwargs = await self.__animate_gif(self.frames, durations=duration)
            buffer = BytesIO()
            gif_image.save(buffer, **save_kwargs)
            buffer.seek(0)

            return buffer

    async def create_vibe_gif(self, side):
        img_bytes = await self.__get_image_bytes()

        base = Image.open(img_bytes).convert('RGBA').resize(self.resolutionVibe)

        for i in range(self.max_framesForVibe):
            canvas = Image.new('RGBA', size=self.resolutionVibeResult, color=(0, 0, 0, 0))
            if side == 'l':
                canvas.paste(base, (40, 0))
                vibeCat = Image.open(f'./assets/gifs/vibe/vibe{i}.gif').convert('RGBA')
                canvas.paste(vibeCat, mask=vibeCat)
            elif side == 'r':
                canvas.paste(base)
                vibeCat = Image.open(f'./assets/gifs/vibe/vibe{i}.gif').convert('RGBA')
                vibeCat = ImageOps.mirror(vibeCat)
                canvas.paste(vibeCat, mask=vibeCat, box=(40, 0))
            self.frames.append(canvas)

        gif_image, save_kwargs = await self.__animate_gif(self.frames, 40)
        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)
        return buffer

    async def create_slap_gif(self):
        img_bytes = await self.__get_image_bytes()

        user_image = Image.open(img_bytes).convert('RGBA').resize((75, 75))

        for i in range(self.max_framesForSlap):
            canvas = Image.new('RGBA', size=self.resolutionSlap, color=(0, 0, 0, 0))
            slapCat = Image.open(f'./assets/gifs/slap/{i}.gif').convert('RGBA')
            canvas.paste(slapCat, mask=slapCat)
            canvas.paste(user_image, (18, 130))
            self.frames.append(canvas)

        gif_image, save_kwargs = await self.__animate_gif(self.frames, 40)
        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)
        return buffer

    async def create_work_gif(self):
        img_bytes = await self.__get_image_bytes()

        user_image = Image.open(img_bytes).convert('RGBA').resize((140, 140))

        for i in range(13):
            canvas = Image.new('RGBA', size=(640, 640), color=(0, 0, 0, 0))
            workGif = Image.open(f'./assets/gifs/work/{i}.gif').convert('RGBA')
            canvas.paste(workGif, mask=workGif)
            canvas.paste(user_image, (190, 135))
            self.frames.append(canvas)

        gif_image, save_kwargs = await self.__animate_gif(self.frames, 40)
        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)
        return buffer

    async def create_hammer_gif(self):
        img_bytes = await self.__get_image_bytes()
        user_image = Image.open(img_bytes).convert('RGBA').resize((64, 64))

        for i in range(5):
            user_image = user_image.resize((64, 64-i*2))
            canvas = Image.new('RGBA', size=(128, 128), color=(0, 0, 0, 0))
            hammerBack = Image.open(f'./assets/gifs/hammer/hammer{i}.gif').convert('RGBA')
            canvas.paste(user_image, (64, 64+i*2))
            canvas.paste(hammerBack, mask=hammerBack)
            self.frames.append(canvas)

        gif_image, save_kwargs = await self.__animate_gif(self.frames, 40)
        buffer = BytesIO()
        gif_image.save(buffer, **save_kwargs)
        buffer.seek(0)
        return buffer

    async def __animate_gif(self, images: list[IMG], durations: Union[int, list[int]] = 20) -> tuple[
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

    async def __get_image_bytes(self):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(url=self.image_url) as res:
                if res.status != 200:
                    raise FileNotFoundError(res.status, res.url)

                return BytesIO(await res.read())