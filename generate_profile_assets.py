
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import random

# Colors

YELLOW = (255, 249, 204)
PURPLE = (225, 207, 255)
LAVENDER = (177, 145, 230)
DARK = (36, 30, 58)
WHITE = (255, 255, 255)
PINK = (255, 195, 222)

WIDTH = 1200
OUT = Path("assets")
OUT.mkdir(exist_ok=True)


def font(size, bold=False):
    names = (
        ["arialbd.ttf", "DejaVuSans-Bold.ttf"]
        if bold else
        ["consola.ttf", "arial.ttf", "DejaVuSans.ttf"]
    )
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


BIG = font(90, True)
MEDIUM = font(28, True)
SMALL = font(21)
MONO = font(20)


def background(height):
    img = Image.new("RGB", (WIDTH, height))
    d = ImageDraw.Draw(img)

    for y in range(height):
        t = y / max(height - 1, 1)
        color = tuple(
            int(YELLOW[i] * (1 - t) + PURPLE[i] * t)
            for i in range(3)
        )
        d.line((0, y, WIDTH, y), fill=color)

    return img, d


def center_text(d, y, text, f, color, outline=None):
    bbox = d.textbbox((0, 0), text, font=f)
    x = (WIDTH - (bbox[2] - bbox[0])) // 2

    if outline:
        d.text(
            (x, y), text, font=f, fill=color,
            stroke_width=3, stroke_fill=outline
        )
    else:
        d.text((x, y), text, font=f, fill=color)


def pixel_star(d, x, y, size=6):
    points = [
        (2, 0), (2, 1),
        (0, 2), (1, 2), (2, 2),
        (3, 2), (4, 2),
        (2, 3), (2, 4)
    ]

    for px, py in points:
        d.rectangle(
            (
                x + px * size,
                y + py * size,
                x + (px + 1) * size - 1,
                y + (py + 1) * size - 1
            ),
            fill=LAVENDER
        )

    d.rectangle(
        (x + 2*size, y + 2*size,
         x + 3*size-1, y + 3*size-1),
        fill=WHITE
    )


def stars(d, height, seed):
    rng = random.Random(seed)

    for _ in range(22):
        x = rng.randint(20, WIDTH - 60)
        y = rng.randint(15, height - 50)
        pixel_star(d, x, y, rng.choice([3, 4, 5]))


# 1. Banner

banner, d = background(350)
stars(d, 350, 10)

center_text(
    d, 75, "AMAL ALAMRI",
    BIG, WHITE, LAVENDER
)

d.rounded_rectangle(
    (315, 200, 885, 252),
    radius=24,
    fill=DARK
)

center_text(
    d, 211,
    "Information Technology Student",
    MEDIUM, WHITE
)

center_text(
    d, 278,
    "AMXstar  |  Saudi Arabia",
    SMALL, DARK
)

banner.save(OUT / "banner.png")


# 2. Terminal

terminal, d = background(540)
stars(d, 540, 22)

d.rounded_rectangle(
    (70, 65, 1130, 475),
    radius=18,
    fill=DARK,
    outline=LAVENDER,
    width=5
)

d.rounded_rectangle(
    (70, 65, 1130, 112),
    radius=14,
    fill=(25, 20, 43)
)

d.rectangle(
    (70, 94, 1130, 112),
    fill=(25, 20, 43)
)

for i, color in enumerate(
    [(255, 110, 130), (255, 210, 100), (140, 220, 170)]
):
    x = 100 + i * 28
    d.ellipse((x, 82, x+15, 97), fill=color)

d.text(
    (430, 78),
    "amal@github ~ fastfetch",
    font=SMALL,
    fill=PURPLE
)

left_lines = [
    "amal@github:~$ fastfetch",
    "",
    "       .--.",
    "      /    \\",
    "     |  o o |",
    "     |   ^  |",
    "      \\____/",
    "",
    "  hello, world!",
    "",
    "  git push   [OK]",
    "  code       [OK]",
    "  creativity [OK]"
]

for i, line in enumerate(left_lines):
    d.text(
        (105, 137 + i*24),
        line,
        font=MONO,
        fill=YELLOW if i == 0 else PURPLE
    )

right_lines = [
    "AMAL ALAMRI",
    "---------------------------",
    "Role:       IT Student",
    "Location:   Saudi Arabia",
    "Major:      Information Technology",
    "Languages:  Python, Java, C",
    "Web:        HTML, CSS, JavaScript",
    "Tools:      Git, GitHub, VS Code",
    "Interests:  Cybersecurity, Design",
    "Projects:   WIN, Mood Calendar",
    "Theme:      Pastel Stars",
]

for i, line in enumerate(right_lines):
    d.text(
        (485, 155 + i*29),
        line,
        font=MONO,
        fill=YELLOW if i == 0 else WHITE
    )

terminal.save(OUT / "terminal.png")


# 3. Pixel Penguin

penguin = [
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
    "..OOOO..OOOO.."
]

palette = {
    "K": DARK,
    "W": WHITE,
    "O": (255, 177, 75)
}


def draw_penguin(d, x, y, scale=11):
    for row, line in enumerate(penguin):
        for col, char in enumerate(line):
            if char in palette:
                d.rectangle(
                    (
                        x + col*scale,
                        y + row*scale,
                        x + (col+1)*scale-1,
                        y + (row+1)*scale-1
                    ),
                    fill=palette[char]
                )


# 4. Footer

footer, d = background(320)
stars(d, 320, 31)

draw_penguin(d, 80, 115, 11)

d.rounded_rectangle(
    (290, 115, 1120, 245),
    radius=18,
    fill=DARK,
    outline=LAVENDER,
    width=4
)

d.text(
    (325, 135),
    "amal says:",
    font=MEDIUM,
    fill=YELLOW
)

d.text(
    (325, 175),
    "Hello! Welcome to my little universe.",
    font=SMALL,
    fill=WHITE
)

d.text(
    (325, 205),
    "Coding, creating, and chasing stars.",
    font=SMALL,
    fill=PINK
)

footer.save(OUT / "footer.png")

print("SUCCESS!")
print("Created:")
print("assets/banner.png")
print("assets/terminal.png")
print("assets/footer.png")
