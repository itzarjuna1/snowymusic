import os
import math
import aiohttp
import aiofiles

from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance
from py_yt import VideosSearch


CACHE_DIR = "cache"
BRAND = "Oneforall Music"
SPOTIFY_GREEN = (29, 185, 84)


def resize(img, size):
    return img.resize(size, Image.LANCZOS)


def truncate(text, length=40):
    return text if len(text) <= length else text[: max(0, length - 3)] + "..."


def fit_text(draw, text, font_path, max_size, min_size, max_width, max_lines=2):
    words = text.split()
    if not words:
        font = ImageFont.truetype(font_path, min_size)
        return font, text

    for size in range(max_size, min_size - 1, -1):
        font = ImageFont.truetype(font_path, size)
        lines = []
        current = ""

        for word in words:
            test = word if not current else current + " " + word
            if draw.textlength(test, font=font) <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word

        if current:
            lines.append(current)

        if len(lines) <= max_lines:
            return font, "".join(lines)

    font = ImageFont.truetype(font_path, min_size)
    return font, text


def make_radial_glow(size, center, inner_color, outer_color, radius):
    w, h = size
    img = Image.new("RGBA", size, outer_color + (0,))
    px = img.load()

    cx, cy = center
    for y in range(h):
        for x in range(w):
            d = math.dist((x, y), (cx, cy))
            t = max(0.0, min(1.0, d / radius))
            a = int((1.0 - t) ** 2 * 180)
            px[x, y] = (*inner_color, a)

    return img.filter(ImageFilter.GaussianBlur(30))


async def get_thumb(videoid: str):
    os.makedirs(CACHE_DIR, exist_ok=True)

    final = os.path.join(CACHE_DIR, f"{videoid}.png")
    temp = os.path.join(CACHE_DIR, f"{videoid}.jpg")

    if os.path.exists(final):
        return final

    try:
        search = VideosSearch(videoid, limit=1)
        result = await search.next()
        data = result["result"][0]

        title_raw = data.get("title", "Unknown Title")
        channel_raw = data.get("channel", {}).get("name", "Unknown Artist")
        duration = data.get("duration", "0:00")

        title = truncate(title_raw, 48)
        channel = truncate(channel_raw, 28)

        thumbs = data.get("thumbnails", [])
        if not thumbs:
            return None

        thumb = thumbs[-1]["url"].split("?")[0]

        async with aiohttp.ClientSession() as session:
            async with session.get(thumb) as resp:
                resp.raise_for_status()
                async with aiofiles.open(temp, "wb") as f:
                    await f.write(await resp.read())

        base = Image.open(temp).convert("RGB")

        bg = resize(base, (1280, 720)).filter(ImageFilter.GaussianBlur(40))
        bg = ImageEnhance.Brightness(bg).enhance(0.18).convert("RGBA")

        dark = Image.new("RGBA", (1280, 720), (0, 0, 0, 170))
        bg = Image.alpha_composite(bg, dark)

        glow1 = make_radial_glow(
            (1280, 720),
            (220, 140),
            SPOTIFY_GREEN,
            (0, 0, 0),
            520,
        )
        glow2 = make_radial_glow(
            (1280, 720),
            (1040, 620),
            (15, 130, 60),
            (0, 0, 0),
            480,
        )

        bg = Image.alpha_composite(bg, glow1)
        bg = Image.alpha_composite(bg, glow2)

        card_w, card_h = 1180, 430
        card_x = (1280 - card_w) // 2
        card_y = 145

        shadow = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 120))
        shadow_mask = Image.new("L", (card_w, card_h), 0)
        ImageDraw.Draw(shadow_mask).rounded_rectangle(
            (0, 0, card_w, card_h), radius=42, fill=255
        )
        shadow = shadow.filter(ImageFilter.GaussianBlur(35))
        bg.paste(shadow, (card_x, card_y + 12), shadow_mask)

        card = Image.new("RGBA", (card_w, card_h), (10, 10, 10, 230))
        card_mask = Image.new("L", (card_w, card_h), 0)
        ImageDraw.Draw(card_mask).rounded_rectangle(
            (0, 0, card_w, card_h), radius=42, fill=255
        )
        bg.paste(card, (card_x, card_y), card_mask)

        overlay = Image.new("RGBA", (card_w, card_h), (0, 0, 0, 0))
        od = ImageDraw.Draw(overlay)
        od.rounded_rectangle((0, 0, card_w - 1, card_h - 1), radius=42, outline=(40, 255, 120, 50), width=2)
        bg.alpha_composite(overlay, (card_x, card_y))

        draw = ImageDraw.Draw(bg)

        thumb_size = 170
        thumb_img = resize(base, (thumb_size, thumb_size))
        thumb_mask = Image.new("L", (thumb_size, thumb_size), 0)
        ImageDraw.Draw(thumb_mask).rounded_rectangle(
            (0, 0, thumb_size, thumb_size), radius=28, fill=255
        )

        thumb_x = card_x + 42
        thumb_y = card_y + 70
        bg.paste(thumb_img, (thumb_x, thumb_y), thumb_mask)

        try:
            title_font_path = "Oneforall/assets/font.ttf"
            artist_font_path = "Oneforall/assets/font2.ttf"
            title_font, title_text = fit_text(draw, title, title_font_path, 60, 34, 690, 2)
            artist_font = ImageFont.truetype(artist_font_path, 30)
            small_font = ImageFont.truetype(artist_font_path, 22)
        except Exception:
            title_font = ImageFont.load_default()
            artist_font = ImageFont.load_default()
            small_font = ImageFont.load_default()
            title_text = title

        draw.text((thumb_x + 240, card_y + 42), "This phone", fill=(165, 165, 165), font=artist_font)

        brand_w = draw.textlength(BRAND, font=small_font)
        draw.text((1220 - brand_w, 42), BRAND, fill=(200, 200, 200), font=small_font)

        btn_x = card_x + 910
        btn_y = card_y + 35
        draw.rounded_rectangle((btn_x, btn_y, btn_x + 230, btn_y + 72), radius=35, fill=(28, 28, 28))
        draw.rounded_rectangle((btn_x, btn_y, btn_x + 230, btn_y + 72), radius=35, outline=(29, 185, 84, 120), width=2)
        draw.text((btn_x + 32, btn_y + 18), "Media output", fill="white", font=small_font)

        title_x = thumb_x + 240
        title_y = card_y + 102
        draw.multiline_text((title_x, title_y), title_text, fill="white", font=title_font, spacing=6)

        draw.text((title_x, card_y + 205), channel, fill=(175, 175, 175), font=artist_font)

        controls_y = card_y + 265
        ctrl_font = title_font
        draw.text((thumb_x + 330, controls_y), "⏮", fill=(230, 230, 230), font=ctrl_font)
        draw.text((thumb_x + 495, controls_y), "⏸", fill=(230, 230, 230), font=ctrl_font)
        draw.text((thumb_x + 665, controls_y), "⏭", fill=(230, 230, 230), font=ctrl_font)

        bar_x1 = thumb_x + 20
        bar_x2 = card_x + card_w - 60
        bar_y = card_y + 385

        draw.line((bar_x1, bar_y, bar_x2, bar_y), fill=(55, 55, 55), width=8)

        progress = min(bar_x1 + 250, bar_x2)
        draw.line((bar_x1, bar_y, progress, bar_y), fill=(255, 255, 255), width=8)

        draw.ellipse((progress - 13, bar_y - 13, progress + 13, bar_y + 13), fill="white")
        draw.ellipse((progress - 18, bar_y - 18, progress + 18, bar_y + 18), outline=(29, 185, 84), width=2)

        draw.text((bar_x1, bar_y + 18), "0:00", fill=(210, 210, 210), font=small_font)
        draw.text((bar_x2 - 45, bar_y + 18), duration, fill=(210, 210, 210), font=small_font)

        bg.convert("RGB").save(final, "PNG")

        return final

    except Exception as e:
        print(f"THUMB ERROR: {e}")
        return None

    finally:
        if os.path.exists(temp):
            try:
                os.remove(temp)
            except:
                pass
