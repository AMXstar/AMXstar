from pathlib import Path
from PIL import Image, ImageDraw
import math

# Run from the folder containing the 'assets' directory.
ASSETS = Path(__file__).resolve().parent / "assets"
FRAMES = 16
DURATION = 110  # milliseconds per frame

YELLOW = (255, 249, 204)
PURPLE = (225, 207, 255)
DARK = (36, 30, 58)
WHITE = (255, 255, 255)
ORANGE = (255, 177, 75)

PENGUIN = [
    "....KKKKKK....",
    "...KKKKKKKK...",
    "..KKWWKKWWKK..",
    "..KKWWKKWWKK..",
    ".KKKWWOOWWKKK.",
    ".KKKWWWWWWKKK.",
    "KKKWWWWWWWWKKK",
    "KKKWWWWWWWWKKK",
    ".KKWWWWWWWWKK.",
    ".KKWWWWWWWWKK.",
    "..KKWWWWWWKK..",
    "...KKKKKKKK...",
    "...OO....OO...",
    "..OOOO..OOOO..",
]

STAR_SPOTS = {
    "banner": [(78, 62), (220, 42), (420, 40), (720, 60), (1060, 55), (1155, 155), (90, 295), (1100, 300)],
    "terminal": [(45, 72), (330, 35), (830, 45), (1110, 30), (1170, 150), (35, 405), (1145, 505), (450, 517)],
    "footer": [(55, 45), (320, 30), (710, 45), (1030, 55), (1150, 275), (400, 275)],
}


def add_twinkles(image, frame_number, name):
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(overlay)
    for index, (x, y) in enumerate(STAR_SPOTS[name]):
        x = round(x * image.width / 1200)
        height = {"banner": 350, "terminal": 540, "footer": 320}[name]
        y = round(y * image.height / height)
        glow = (1 + math.sin(2 * math.pi * frame_number / FRAMES + index * 1.45)) / 2
        alpha = round(30 + 225 * glow)
        r = 3 + round(6 * glow)
        d.line((x - r, y, x + r, y), fill=(255, 255, 255, alpha), width=2)
        d.line((x, y - r, x, y + r), fill=(188, 146, 245, alpha), width=2)
        d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(255, 255, 255, alpha))
    return Image.alpha_composite(image.convert("RGBA"), overlay)


def erase_old_penguin(base):
    # Restore the original pastel gradient only beneath the penguin pixels.
    mask = Image.new("L", base.size, 0)
    md = ImageDraw.Draw(mask)
    scale = 11
    for y, line in enumerate(PENGUIN):
        for x, symbol in enumerate(line):
            if symbol != ".":
                x0, y0 = 80 + x * scale, 115 + y * scale
                md.rectangle((x0, y0, x0 + scale - 1, y0 + scale - 1), fill=255)
    grad = Image.new("RGB", base.size)
    gd = ImageDraw.Draw(grad)
    for y in range(base.height):
        t = y / max(base.height - 1, 1)
        col = tuple(round(YELLOW[k] * (1-t) + PURPLE[k] * t) for k in range(3))
        gd.line((0, y, base.width, y), fill=col)
    cleaned = base.copy()
    cleaned.paste(grad, (0, 0), mask)
    return cleaned


def penguin_sprite():
    size = 11
    palette = {"K": DARK, "W": WHITE, "O": ORANGE}
    sprite = Image.new("RGBA", (len(PENGUIN[0]) * size, len(PENGUIN) * size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(sprite)
    for y, line in enumerate(PENGUIN):
        for x, symbol in enumerate(line):
            if symbol in palette:
                draw.rectangle((x*size, y*size, (x+1)*size-1, (y+1)*size-1), fill=palette[symbol] + (255,))
    return sprite


def write_gif(name):
    path = ASSETS / (name + ".png")
    if not path.exists():
        raise FileNotFoundError(f"Missing {path}. Check you ran generate_profile_assets.py first.")
    original = Image.open(path).convert("RGB")
    if name == "footer":
        original = erase_old_penguin(original)
        penguin = penguin_sprite()

    frames = []
    for i in range(FRAMES):
        frame = add_twinkles(original, i, name)
        d = ImageDraw.Draw(frame)
        if name == "terminal":
            if i < FRAMES // 2:  # cursor blinks
                x = round(427 * frame.width / 1200)
                y = round(441 * frame.height / 540)
                d.rectangle((x, y, x+11, y+25), fill=(255, 210, 110, 255))
        elif name == "footer":
            bob = round(4 * (1 + math.sin(2 * math.pi * i / FRAMES)))
            frame.alpha_composite(penguin, (80, 115 - bob))
        frames.append(frame.convert("RGB"))

    
    palette = frames[0].quantize(colors=192, method=Image.Quantize.MEDIANCUT)
    gif_frames = [f.quantize(palette=palette, dither=Image.Dither.NONE) for f in frames]
    target = ASSETS / (name + ".gif")
    gif_frames[0].save(target, save_all=True, append_images=gif_frames[1:],
                       duration=DURATION, loop=0, optimize=True, disposal=2)
    print(f"Created: {target}")


if __name__ == "__main__":
    for name in ("banner", "terminal", "footer"):
        write_gif(name)
    print("Done! Change .png to .gif in your README.md and upload the GIF files.")