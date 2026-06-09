from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "badge-template.png"
SIZE = 1254
SCALE = 4
YELLOW = (253, 211, 5, 255)
BLACK = (1, 1, 1, 255)
WHITE = (245, 245, 235, 255)
CYAN = (0, 205, 225, 255)
ORANGE = (255, 105, 24, 255)
TEAL = (0, 184, 145, 255)
MAGENTA = (237, 61, 210, 255)
RED = (255, 72, 48, 255)
BLUE = (80, 165, 255, 255)
SILVER = (205, 214, 220, 255)
BRONZE = (198, 122, 48, 255)
GOLD = YELLOW
PLATINUM = (205, 236, 242, 255)

FONT_DIR = Path("C:/Windows/Fonts")
FONT_BLACK = FONT_DIR / "ariblk.ttf"
FONT_BOLD = FONT_DIR / "arialbd.ttf"
FONT_REGULAR = FONT_DIR / "arial.ttf"
FONT_MONO = FONT_DIR / "consolab.ttf"


@dataclass(frozen=True)
class Badge:
    filename: str
    title: str
    family: str
    level: int
    total: int
    threshold: str
    icon: str


BADGES: list[Badge] = [
    Badge("badge-hello-glados.png", "Hello, GLaDOS!", "glados", 1, 5, "1 MSG", "glados"),
    Badge("badge-still-alive.png", "Still Alive", "glados", 2, 5, "10 MSG", "cake"),
    Badge("badge-test-subject.png", "Test Subject", "glados", 3, 5, "50 MSG", "test"),
    Badge("badge-property-of-aperture.png", "Property of Aperture", "glados", 4, 5, "100 MSG", "aperture"),
    Badge("badge-cake-is-a-lie.png", "The Cake Is a Lie", "glados", 5, 5, "500 MSG", "cake_lie"),
    Badge("badge-first-draft.png", "First Draft", "docmost", 1, 5, "1 PAGE", "draft"),
    Badge("badge-wiki-contributor.png", "Wiki Contributor", "docmost", 2, 5, "10 PAGES", "wiki"),
    Badge("badge-archivist.png", "Archivist", "docmost", 3, 5, "25 PAGES", "archive"),
    Badge("badge-space-chronicler.png", "Space Chronicler", "docmost", 4, 5, "50 PAGES", "chronicle"),
    Badge("badge-first-queries.png", "First Queries", "ocabra", 1, 5, "10K TOKENS", "query"),
    Badge("badge-token-collector.png", "Token Collector", "ocabra", 2, 5, "100K TOKENS", "tokens"),
    Badge("badge-burning-tokens.png", "Burning Tokens", "ocabra", 3, 5, "1M TOKENS", "burn"),
    Badge("badge-gpu-melter.png", "GPU Melter", "ocabra", 4, 5, "5M TOKENS", "gpu"),
    Badge("badge-infinite-loop.png", "Infinite Loop", "ocabra", 5, 5, "10M TOKENS", "loop"),
    Badge("badge-first-hack.png", "First Hack", "hack", 1, 9, "1 SESSION", "hack1"),
    Badge("badge-hammer-time.png", "Hammer Time", "hack", 2, 9, "3 SESSIONS", "hack2"),
    Badge("badge-space-regular.png", "Space Regular", "hack", 3, 9, "5 SESSIONS", "hack3"),
    Badge("badge-hackspace-veteran.png", "Hackspace Veteran", "hack", 4, 9, "10 SESSIONS", "hack4"),
    Badge("badge-master-hacker.png", "Master Hacker", "hack", 5, 9, "15 SESSIONS", "hack5"),
    Badge("badge-hackspace-elder.png", "Hackspace Elder", "hack", 6, 9, "20 SESSIONS", "hack6"),
    Badge("badge-hackspace-legend.png", "Hackspace Legend", "hack", 7, 9, "25 SESSIONS", "hack7"),
    Badge("badge-hackspace-hero.png", "Hackspace Hero", "hack", 8, 9, "30 SESSIONS", "hack8"),
    Badge("badge-hackspace-immortal.png", "Hackspace Immortal", "hack", 9, 9, "35 SESSIONS", "hack9"),
    Badge("badge-first-assembly.png", "First Assembly", "assembly", 1, 9, "1 MEETING", "assembly1"),
    Badge("badge-assembly-regular.png", "Assembly Regular", "assembly", 2, 9, "3 MEETINGS", "assembly2"),
    Badge("badge-council-member.png", "Council Member", "assembly", 3, 9, "5 MEETINGS", "assembly3"),
    Badge("badge-community-veteran.png", "Community Veteran", "assembly", 4, 9, "10 MEETINGS", "assembly4"),
    Badge("badge-community-pillar.png", "Community Pillar", "assembly", 5, 9, "15 MEETINGS", "assembly5"),
    Badge("badge-assembly-elder.png", "Assembly Elder", "assembly", 6, 9, "20 MEETINGS", "assembly6"),
    Badge("badge-assembly-legend.png", "Assembly Legend", "assembly", 7, 9, "25 MEETINGS", "assembly7"),
    Badge("badge-marathon-member.png", "Marathon Member", "assembly", 8, 9, "30 MEETINGS", "assembly8"),
    Badge("badge-eternal-council.png", "Eternal Council", "assembly", 9, 9, "35 MEETINGS", "assembly9"),
    Badge("badge-first-year.png", "First Year", "membership", 1, 10, "1 YEAR", "year"),
    Badge("badge-second-year.png", "Second Year", "membership", 2, 10, "2 YEARS", "year"),
    Badge("badge-third-year.png", "Third Year", "membership", 3, 10, "3 YEARS", "year"),
    Badge("badge-fourth-year.png", "Fourth Year", "membership", 4, 10, "4 YEARS", "year"),
    Badge("badge-fifth-year.png", "Fifth Year", "membership", 5, 10, "5 YEARS", "year"),
    Badge("badge-sixth-year.png", "Sixth Year", "membership", 6, 10, "6 YEARS", "year"),
    Badge("badge-seventh-year.png", "Seventh Year", "membership", 7, 10, "7 YEARS", "year"),
    Badge("badge-eighth-year.png", "Eighth Year", "membership", 8, 10, "8 YEARS", "year"),
    Badge("badge-ninth-year.png", "Ninth Year", "membership", 9, 10, "9 YEARS", "year"),
    Badge("badge-10-years.png", "A Decade at Makespace", "membership", 10, 10, "10 YEARS", "decade"),
]


class Canvas:
    def __init__(self) -> None:
        self.image = Image.open(TEMPLATE).convert("RGBA").resize((SIZE * SCALE, SIZE * SCALE), Image.Resampling.LANCZOS)
        self.draw = ImageDraw.Draw(self.image)

    def xy(self, *values: float) -> tuple[int, ...]:
        return tuple(round(v * SCALE) for v in values)

    def font(self, path: Path, size: int) -> ImageFont.FreeTypeFont:
        return ImageFont.truetype(str(path), size * SCALE)

    def line(self, pts, fill=YELLOW, width=12, joint="curve") -> None:
        self.draw.line([self.xy(x, y) for x, y in pts], fill=fill, width=width * SCALE, joint=joint)

    def rectangle(self, box, outline=YELLOW, width=10, fill=None) -> None:
        self.draw.rectangle(self.xy(*box), outline=outline, width=width * SCALE, fill=fill)

    def rounded(self, box, radius=22, outline=YELLOW, width=10, fill=None) -> None:
        self.draw.rounded_rectangle(self.xy(*box), radius=radius * SCALE, outline=outline, width=width * SCALE, fill=fill)

    def ellipse(self, box, outline=YELLOW, width=10, fill=None) -> None:
        self.draw.ellipse(self.xy(*box), outline=outline, width=width * SCALE, fill=fill)

    def arc(self, box, start, end, fill=YELLOW, width=10) -> None:
        self.draw.arc(self.xy(*box), start=start, end=end, fill=fill, width=width * SCALE)

    def polygon(self, pts, outline=YELLOW, width=10, fill=None) -> None:
        scaled = [self.xy(x, y) for x, y in pts]
        self.draw.polygon(scaled, outline=outline, fill=fill)
        if width:
            self.draw.line(scaled + [scaled[0]], fill=outline, width=width * SCALE, joint="curve")

    def centered_text(self, text, y, size, fill=YELLOW, font_path=FONT_BLACK, max_width=720) -> None:
        font = fit_font(text, font_path, size, max_width)
        bbox = self.draw.textbbox((0, 0), text, font=font)
        x = (SIZE * SCALE - (bbox[2] - bbox[0])) // 2
        self.draw.text((x, y * SCALE), text, font=font, fill=fill)

    def save(self, path: Path) -> None:
        output = self.image.resize((SIZE, SIZE), Image.Resampling.LANCZOS)
        output.save(path, optimize=True)


def fit_font(text: str, path: Path, start_size: int, max_width: int) -> ImageFont.FreeTypeFont:
    probe = Image.new("RGBA", (10, 10))
    d = ImageDraw.Draw(probe)
    for size in range(start_size, 12, -2):
        font = ImageFont.truetype(str(path), size * SCALE)
        bbox = d.textbbox((0, 0), text, font=font)
        if bbox[2] - bbox[0] <= max_width * SCALE:
            return font
    return ImageFont.truetype(str(path), 12 * SCALE)


def draw_arc_text(c: Canvas, text: str) -> None:
    text = text.upper()
    max_width = 780 if len(text) < 18 else 860
    font = fit_font(text, FONT_BLACK, 76, max_width)
    probe = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    widths = [(probe.textbbox((0, 0), ch, font=font)[2] + 8 * SCALE) for ch in text]
    radius = 456 * SCALE
    total_angle = min(math.radians(118), sum(widths) / radius)
    angle = math.radians(90) + total_angle / 2
    cx = cy = 627 * SCALE
    for ch, width in zip(text, widths):
        char_angle = width / radius
        theta = angle - char_angle / 2
        if ch != " ":
            bbox = probe.textbbox((0, 0), ch, font=font)
            glyph = Image.new("RGBA", (bbox[2] - bbox[0] + 20 * SCALE, bbox[3] - bbox[1] + 20 * SCALE), (0, 0, 0, 0))
            gd = ImageDraw.Draw(glyph)
            gd.text((10 * SCALE - bbox[0], 10 * SCALE - bbox[1]), ch, font=font, fill=YELLOW)
            rotated = glyph.rotate(math.degrees(theta) - 90, expand=True, resample=Image.Resampling.BICUBIC)
            x = cx + radius * math.cos(theta) - rotated.width / 2
            y = cy - radius * math.sin(theta) - rotated.height / 2
            c.image.alpha_composite(rotated, (round(x), round(y)))
        angle -= char_angle


def draw_brand(c: Canvas) -> None:
    c.line([(330, 1002), (924, 1002)], width=12)
    c.ellipse((322, 994, 340, 1012), fill=BLACK, width=5)
    c.ellipse((914, 994, 932, 1012), fill=BLACK, width=5)
    c.centered_text("MAKESPACE", 1032, 66, max_width=640)
    c.line([(410, 1116), (844, 1116)], width=12)
    c.ellipse((400, 1107, 420, 1127), fill=BLACK, width=5)
    c.ellipse((834, 1107, 854, 1127), fill=BLACK, width=5)


def draw_progress(c: Canvas, badge: Badge, accent) -> None:
    label = f"LEVEL {badge.level}/{badge.total}"
    c.centered_text(label, 875, 35, fill=accent, font_path=FONT_BOLD, max_width=420)
    start_x, gap, y = 430, 44, 940
    if badge.total == 10:
        start_x, gap = 386, 35
    for i in range(1, badge.total + 1):
        x = start_x + (i - 1) * gap
        fill = accent if i <= badge.level else BLACK
        outline = accent if i <= badge.level else YELLOW
        c.ellipse((x - 13, y - 13, x + 13, y + 13), outline=outline, fill=fill, width=5)
    c.centered_text(badge.threshold, 958, 30, fill=WHITE, font_path=FONT_BOLD, max_width=500)


def family_accent(badge: Badge):
    if badge.family == "glados":
        return ORANGE if badge.level % 2 else CYAN
    if badge.family == "docmost":
        return TEAL
    if badge.family == "ocabra":
        return RED if badge.level >= 3 else MAGENTA
    if badge.family == "assembly":
        return BLUE if badge.level < 5 else SILVER
    if badge.family == "membership":
        scale = [BRONZE, BRONZE, SILVER, SILVER, GOLD, GOLD, PLATINUM, PLATINUM, (190, 150, 255, 255), (255, 255, 245, 255)]
        return scale[badge.level - 1]
    return YELLOW


def sparkle(c: Canvas, x, y, r=32, fill=YELLOW) -> None:
    c.polygon([(x, y - r), (x + r * 0.28, y - r * 0.28), (x + r, y), (x + r * 0.28, y + r * 0.28), (x, y + r), (x - r * 0.28, y + r * 0.28), (x - r, y), (x - r * 0.28, y - r * 0.28)], outline=fill, width=8)


def draw_chip(c: Canvas, x=420, y=410, w=400, h=280, accent=CYAN) -> None:
    c.rounded((x, y, x + w, y + h), radius=26, outline=YELLOW, width=14)
    c.rounded((x + 95, y + 70, x + w - 95, y + h - 70), radius=16, outline=accent, width=10)
    for i in range(6):
        px = x - 42
        py = y + 34 + i * 42
        c.line([(px, py), (x, py)], fill=YELLOW, width=8)
        c.line([(x + w, py), (x + w + 42, py)], fill=YELLOW, width=8)
    for i in range(5):
        px = x + 55 + i * 70
        c.line([(px, y - 42), (px, y)], fill=YELLOW, width=8)
        c.line([(px, y + h), (px, y + h + 42)], fill=YELLOW, width=8)


def draw_glados_icon(c: Canvas, badge: Badge, accent) -> None:
    if badge.icon == "glados":
        c.ellipse((420, 360, 834, 700), outline=YELLOW, width=18)
        c.ellipse((530, 430, 724, 624), outline=accent, width=18)
        c.ellipse((595, 495, 659, 559), fill=accent, outline=accent, width=8)
        c.line([(626, 700), (626, 780), (520, 820)], fill=YELLOW, width=16)
        c.line([(626, 780), (734, 820)], fill=YELLOW, width=16)
        c.rounded((410, 725, 844, 805), radius=30, outline=YELLOW, width=12)
        c.centered_text("HELLO?", 742, 38, fill=accent, font_path=FONT_MONO, max_width=280)
    elif badge.icon in {"cake", "cake_lie"}:
        c.line([(430, 660), (824, 660)], width=16)
        c.rounded((470, 510, 784, 660), radius=24, outline=YELLOW, width=14)
        c.line([(510, 510), (510, 445)], fill=accent, width=10)
        c.line([(626, 510), (626, 420)], fill=accent, width=10)
        c.line([(742, 510), (742, 445)], fill=accent, width=10)
        for x, y in [(510, 428), (626, 403), (742, 428)]:
            c.polygon([(x, y - 32), (x + 18, y + 6), (x, y + 26), (x - 18, y + 6)], outline=accent, width=8)
        if badge.icon == "cake_lie":
            c.line([(424, 396), (830, 732)], fill=RED, width=18)
            c.line([(830, 396), (424, 732)], fill=RED, width=18)
        else:
            c.centered_text("STILL", 706, 42, fill=accent, font_path=FONT_BOLD, max_width=300)
    elif badge.icon == "test":
        c.rounded((445, 360, 810, 735), radius=22, outline=YELLOW, width=14)
        c.line([(500, 470), (755, 470)], fill=accent, width=10)
        c.line([(500, 590), (755, 590)], fill=accent, width=10)
        c.ellipse((565, 510, 690, 635), outline=YELLOW, width=12)
        c.line([(628, 635), (628, 755)], fill=YELLOW, width=12)
        c.line([(570, 755), (686, 755)], fill=YELLOW, width=12)
    else:
        c.rounded((430, 390, 824, 710), radius=24, outline=YELLOW, width=14)
        c.centered_text("LAB", 455, 96, fill=accent, font_path=FONT_BLACK, max_width=300)
        c.centered_text("PROPERTY", 570, 45, fill=YELLOW, font_path=FONT_BOLD, max_width=350)
        c.line([(500, 650), (754, 650)], fill=accent, width=12)


def draw_doc_icon(c: Canvas, badge: Badge, accent) -> None:
    if badge.icon == "draft":
        c.rectangle((460, 350, 740, 725), width=14)
        c.line([(505, 435), (690, 435), (690, 445)], fill=accent, width=10)
        c.line([(505, 500), (700, 500)], width=10)
        c.line([(505, 565), (680, 565)], width=10)
        c.line([(720, 680), (835, 565)], fill=accent, width=22)
        c.polygon([(835, 565), (875, 525), (850, 610)], outline=accent, width=8, fill=accent)
    elif badge.icon == "wiki":
        for off in [0, 34, 68]:
            c.rectangle((430 + off, 380 - off, 742 + off, 705 - off), outline=YELLOW if off != 68 else accent, width=12)
        c.centered_text("WIKI", 602, 70, fill=accent, font_path=FONT_BLACK, max_width=300)
    elif badge.icon == "archive":
        c.rounded((405, 420, 850, 740), radius=25, outline=YELLOW, width=14)
        c.rectangle((445, 360, 810, 455), outline=accent, width=12)
        c.line([(520, 520), (735, 520)], width=12)
        c.line([(555, 590), (700, 590)], width=12)
        c.ellipse((595, 650, 660, 715), outline=accent, width=10)
    else:
        c.ellipse((420, 410, 625, 730), outline=YELLOW, width=14)
        c.ellipse((630, 410, 835, 730), outline=YELLOW, width=14)
        c.line([(628, 410), (628, 760)], fill=accent, width=12)
        c.line([(500, 520), (590, 520)], width=8)
        c.line([(500, 585), (590, 585)], width=8)
        c.line([(665, 520), (755, 520)], width=8)
        c.line([(665, 585), (755, 585)], width=8)
        sparkle(c, 825, 405, 35, fill=accent)


def draw_ocabra_icon(c: Canvas, badge: Badge, accent) -> None:
    if badge.icon == "query":
        c.rounded((390, 390, 864, 700), radius=24, outline=YELLOW, width=14)
        c.centered_text("> ?", 485, 120, fill=accent, font_path=FONT_MONO, max_width=330)
        c.line([(485, 660), (770, 660)], width=12)
    elif badge.icon == "tokens":
        for i in range(4):
            y = 655 - i * 70
            c.ellipse((450, y, 805, y + 95), outline=YELLOW if i < 3 else accent, width=12)
            c.arc((450, y - 65, 805, y + 95), 0, 180, fill=YELLOW, width=12)
        c.centered_text("TOK", 514, 70, fill=accent, font_path=FONT_BLACK, max_width=250)
    elif badge.icon == "burn":
        c.polygon([(625, 350), (745, 570), (690, 710), (625, 780), (548, 700), (515, 585)], outline=RED, width=16)
        c.polygon([(625, 480), (675, 610), (625, 705), (575, 610)], outline=ORANGE, width=12)
        c.ellipse((520, 700, 735, 800), outline=YELLOW, width=12)
        c.centered_text("TOK", 720, 40, fill=YELLOW, font_path=FONT_BLACK, max_width=180)
    elif badge.icon == "gpu":
        draw_chip(c, 390, 400, 470, 300, accent)
        for i, x in enumerate([505, 625, 745]):
            c.line([(x, 735), (x + 55, 810)], fill=RED if i != 1 else ORANGE, width=12)
    else:
        c.arc((395, 440, 635, 680), 300, 60, fill=accent, width=22)
        c.arc((620, 440, 860, 680), 120, 240, fill=accent, width=22)
        c.arc((395, 440, 635, 680), 120, 240, fill=YELLOW, width=22)
        c.arc((620, 440, 860, 680), 300, 60, fill=YELLOW, width=22)
        c.centered_text("LOOP", 705, 52, fill=YELLOW, font_path=FONT_BLACK, max_width=300)


def draw_hammer(c: Canvas, x, y, accent=YELLOW) -> None:
    c.rounded((x, y, x + 220, y + 70), radius=16, outline=accent, width=12)
    c.line([(x + 90, y + 70), (x + 235, y + 315)], fill=accent, width=24)


def draw_wrench(c: Canvas, x, y, accent=YELLOW) -> None:
    c.arc((x, y, x + 150, y + 150), 35, 315, fill=accent, width=20)
    c.line([(x + 112, y + 112), (x + 310, y + 310)], fill=accent, width=22)
    c.ellipse((x + 280, y + 280, x + 360, y + 360), outline=accent, width=18)


def draw_hack_icon(c: Canvas, badge: Badge, accent) -> None:
    draw_wrench(c, 415, 360, YELLOW)
    draw_hammer(c, 600, 390, accent)
    if badge.level >= 3:
        c.rounded((410, 665, 842, 780), radius=22, outline=YELLOW, width=12)
        c.line([(475, 665), (475, 625), (610, 625), (610, 665)], width=12)
    if badge.level >= 5:
        c.polygon([(627, 325), (690, 430), (805, 455), (728, 540), (738, 655), (627, 610), (516, 655), (526, 540), (449, 455), (564, 430)], outline=accent, width=10)
    if badge.level >= 7:
        sparkle(c, 855, 430, 34, fill=accent)
        sparkle(c, 380, 555, 26, fill=accent)
    if badge.level == 9:
        c.centered_text("IMMORTAL", 790, 37, fill=accent, font_path=FONT_BOLD, max_width=410)


def draw_assembly_icon(c: Canvas, badge: Badge, accent) -> None:
    c.ellipse((445, 385, 535, 475), outline=YELLOW, width=12)
    c.ellipse((585, 350, 685, 450), outline=accent, width=12)
    c.ellipse((725, 385, 815, 475), outline=YELLOW, width=12)
    c.arc((380, 480, 570, 735), 200, 340, fill=YELLOW, width=14)
    c.arc((535, 450, 720, 735), 200, 340, fill=accent, width=14)
    c.arc((685, 480, 875, 735), 200, 340, fill=YELLOW, width=14)
    c.ellipse((410, 670, 845, 790), outline=YELLOW, width=14)
    if badge.level >= 3:
        c.line([(535, 610), (720, 610)], fill=accent, width=12)
        c.line([(628, 610), (628, 760)], fill=accent, width=12)
    if badge.level >= 5:
        for x in [455, 555, 655, 755]:
            c.rectangle((x, 650, x + 35, 805), outline=accent, width=10)
    if badge.level >= 7:
        c.arc((380, 330, 875, 830), 145, 215, fill=accent, width=12)
        c.arc((380, 330, 875, 830), 325, 35, fill=accent, width=12)
    if badge.level == 9:
        sparkle(c, 627, 315, 42, fill=accent)


def draw_membership_icon(c: Canvas, badge: Badge, accent) -> None:
    number = "10" if badge.level == 10 else str(badge.level)
    c.ellipse((390, 335, 864, 810), outline=accent, width=18)
    c.centered_text(number, 395, 230 if badge.level == 10 else 260, fill=accent, font_path=FONT_BLACK, max_width=430)
    c.centered_text("YEARS" if badge.level != 1 else "YEAR", 690, 58, fill=YELLOW, font_path=FONT_BLACK, max_width=340)
    if badge.level >= 5:
        sparkle(c, 432, 410, 32, fill=accent)
        sparkle(c, 825, 410, 32, fill=accent)
    if badge.level == 10:
        c.line([(485, 770), (769, 770)], fill=accent, width=16)
        sparkle(c, 627, 335, 42, fill=WHITE)


def draw_icon(c: Canvas, badge: Badge, accent) -> None:
    if badge.family == "glados":
        draw_glados_icon(c, badge, accent)
    elif badge.family == "docmost":
        draw_doc_icon(c, badge, accent)
    elif badge.family == "ocabra":
        draw_ocabra_icon(c, badge, accent)
    elif badge.family == "hack":
        draw_hack_icon(c, badge, accent)
    elif badge.family == "assembly":
        draw_assembly_icon(c, badge, accent)
    elif badge.family == "membership":
        draw_membership_icon(c, badge, accent)


def render_badge(badge: Badge) -> Path:
    c = Canvas()
    accent = family_accent(badge)
    draw_arc_text(c, badge.title)
    draw_icon(c, badge, accent)
    draw_progress(c, badge, accent)
    draw_brand(c)
    out = ROOT / badge.filename
    c.save(out)
    return out


def main() -> None:
    outputs = [render_badge(badge) for badge in BADGES]
    print(f"Generated {len(outputs)} badges")
    for path in outputs:
        print(path.name)


if __name__ == "__main__":
    main()
