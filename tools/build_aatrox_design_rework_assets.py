from __future__ import annotations

import csv
import json
import math
import random
import wave
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw, ImageEnhance


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "source" / "aatrox_design_rework"

ACTOR_SOURCE = SOURCE / "imagegen_actor_design_source.png"
ICON_SOURCE = SOURCE / "imagegen_icons_design_source.png"
VFX_SOURCE = SOURCE / "imagegen_vfx_design_source.png"

ACTOR_SHEET = ROOT / "aseprite_resources" / "champions" / "aatrox#sheet.png"
ACTOR_ANIM = ROOT / "aseprite_resources" / "champions" / "aatrox#anim.fanim"
Q_IMPACT_SHEET = ROOT / "aseprite_resources" / "effects" / "aatrox_q_impact#sheet.png"
Q_IMPACT_ANIM = ROOT / "aseprite_resources" / "effects" / "aatrox_q_impact#anim.fanim"
ATTACK_SLASH_SHEET = ROOT / "aseprite_resources" / "effects" / "aatrox_attack_slash#sheet.png"
ATTACK_SLASH_ANIM = ROOT / "aseprite_resources" / "effects" / "aatrox_attack_slash#anim.fanim"
ULT_AURA_SHEET = ROOT / "aseprite_resources" / "effects" / "aatrox_ult_aura#sheet.png"
ULT_AURA_ANIM = ROOT / "aseprite_resources" / "effects" / "aatrox_ult_aura#anim.fanim"

CONTACT_SHEET = SOURCE / "aatrox_design_actor_contact.png"
ICON_CONTACT = SOURCE / "aatrox_design_icon_contact.png"
VFX_CONTACT = SOURCE / "aatrox_design_vfx_contact.png"
QA_MATRIX = ROOT / "qa" / "aatrox_design_rework_asset_matrix.csv"
SFX_DIR = ROOT / "sound" / "sfx"


@dataclass(frozen=True)
class PoseCell:
    col: int
    row: int
    crop_left: float = 0.0
    crop_top: float = 0.0
    crop_right: float = 1.0
    crop_bottom: float = 1.0


ACTOR_POSES = {
    "idle_a": PoseCell(0, 0, 0.00, 0.02, 1.00, 0.98),
    "idle_b": PoseCell(1, 0, 0.00, 0.02, 1.00, 0.98),
    "run_a": PoseCell(2, 0, 0.00, 0.03, 1.00, 0.98),
    "run_b": PoseCell(3, 0, 0.00, 0.03, 1.00, 0.98),
    "attack": PoseCell(4, 0, 0.00, 0.02, 1.00, 0.98),
    "cleave": PoseCell(0, 1, 0.00, 0.02, 1.00, 0.98),
    "dash": PoseCell(1, 1, 0.00, 0.08, 1.00, 0.92),
    "ult": PoseCell(2, 1, 0.02, 0.00, 0.98, 0.98),
    "hit": PoseCell(3, 1, 0.03, 0.04, 0.96, 0.96),
    "dead": PoseCell(4, 1, 0.00, 0.10, 1.00, 0.92),
}

NORMAL_RUNTIME_POSES = {"idle_a", "idle_b"}
ACTION_BOUNDARY_POSE = "idle_a"

ACTION_DURATIONS = {
    "idle": [0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12],
    "attack": [0.055, 0.055, 0.055, 0.055, 0.06, 0.065, 0.055, 0.05, 0.05],
    "run": [0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075, 0.075],
    "skill": [0.14, 0.14, 0.26, 0.11, 0.09, 0.17, 0.14, 0.18],
    "skill2": [0.055, 0.045, 0.04, 0.035, 0.05, 0.07, 0.1],
    "hit": [0.13],
    "dead": [0.2],
    "ult": [0.12],
}

ACTION_FRAME_DIMS = {
    "idle": [(54, 50)] * 9,
    "attack": [(96, 72)] * 9,
    "run": [(96, 72)] * 8,
    "skill": [(96, 72)] * 8,
    "skill2": [(96, 72)] * 7,
    "hit": [(54, 50)],
    "dead": [(54, 50)],
    "ult": [(54, 50)],
}

SILVERBEAR_SHEET_SIZE = (6720, 72)
SILVERBEAR_FRAME_X = {
    "skill": [2784, 2880, 2976, 3072, 3168, 3264, 3360, 3456],
    "skill2": [3552, 3648, 3744, 3840, 3936, 4032, 4128],
    "run": [4224, 4320, 4416, 4512, 4608, 4704, 4800, 4896],
    "attack": [4992, 5088, 5184, 5280, 5376, 5472, 5568, 5664, 5760],
    "idle": [5868, 5964, 6060, 6156, 6252, 6348, 6444, 6540, 6636],
    "hit": [5868],
    "dead": [5868],
    "ult": [5868],
}


def load_rgba(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGBA")


def remove_green(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            saturated = max(r, g, b) - min(r, g, b) > 20
            green_dominant = g > 110 and g - r > 35 and g - b > 35
            chroma_green = g > 170 and r < 150 and b < 150
            dark_green_fringe = saturated and g > 35 and r < 120 and g >= r - 5 and g > b + 10
            near_key = g > 130 and r < 120 and b < 120
            if green_dominant or chroma_green or dark_green_fringe or near_key:
                px[x, y] = (0, 0, 0, 0)
    return image


def trim_alpha(image: Image.Image) -> Image.Image:
    bbox = image.getchannel("A").getbbox()
    if bbox is None:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    return image.crop(bbox)


def hard_alpha(image: Image.Image, threshold: int = 32) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A")
    image.putalpha(alpha.point(lambda value: 255 if value > threshold else 0))
    return image


def quantize_rgba(image: Image.Image, colors: int = 96) -> Image.Image:
    alpha = image.getchannel("A")
    rgb = Image.new("RGB", image.size, (0, 0, 0))
    rgb.paste(image.convert("RGB"), mask=alpha)
    quantized = rgb.quantize(colors=colors, method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert("RGBA")
    quantized.putalpha(alpha.point(lambda value: 255 if value > 32 else 0))
    return quantized


def multiply_alpha(image: Image.Image, factor: float) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: max(0, min(255, round(value * factor))))
    image.putalpha(alpha)
    return image


def tint_nontransparent(image: Image.Image, color: tuple[int, int, int], alpha_factor: float) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A").point(lambda value: max(0, min(255, round(value * alpha_factor))))
    tinted = Image.new("RGBA", image.size, (*color, 0))
    tinted.putalpha(alpha)
    return tinted


def grade_demon_palette(image: Image.Image) -> Image.Image:
    image = image.convert("RGBA")
    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = px[x, y]
            if a == 0:
                continue
            if r > 65 and g > 42:
                g = round(g * 0.42)
                b = round(b * 0.66)
                r = min(255, round(r * 1.08))
            if g > r * 0.55 and r > 35:
                g = round(r * 0.38)
            if r > 120 and b < 60:
                b = min(80, b + 12)
            px[x, y] = (r, g, b, a)
    return image


def remove_tiny_components(image: Image.Image, *, min_pixels: int = 10) -> Image.Image:
    image = image.convert("RGBA")
    alpha = image.getchannel("A")
    seen: set[tuple[int, int]] = set()
    keep: set[tuple[int, int]] = set()
    for y in range(image.height):
        for x in range(image.width):
            if (x, y) in seen or alpha.getpixel((x, y)) <= 32:
                continue
            stack = [(x, y)]
            seen.add((x, y))
            component: list[tuple[int, int]] = []
            while stack:
                cx, cy = stack.pop()
                component.append((cx, cy))
                for nx, ny in ((cx - 1, cy), (cx + 1, cy), (cx, cy - 1), (cx, cy + 1)):
                    if nx < 0 or ny < 0 or nx >= image.width or ny >= image.height:
                        continue
                    if (nx, ny) in seen or alpha.getpixel((nx, ny)) <= 32:
                        continue
                    seen.add((nx, ny))
                    stack.append((nx, ny))
            if len(component) >= min_pixels:
                keep.update(component)

    px = image.load()
    for y in range(image.height):
        for x in range(image.width):
            if (x, y) not in keep:
                px[x, y] = (0, 0, 0, 0)
    return image


def grid_crop(image: Image.Image, cols: int, rows: int, cell: PoseCell) -> Image.Image:
    cell_w = image.width / cols
    cell_h = image.height / rows
    left = round((cell.col + cell.crop_left) * cell_w)
    top = round((cell.row + cell.crop_top) * cell_h)
    right = round((cell.col + cell.crop_right) * cell_w)
    bottom = round((cell.row + cell.crop_bottom) * cell_h)
    return image.crop((left, top, right, bottom))


def normalized_crop(image: Image.Image, left: float, top: float, right: float, bottom: float) -> Image.Image:
    return image.crop((
        round(left * image.width),
        round(top * image.height),
        round(right * image.width),
        round(bottom * image.height),
    ))


def vfx_row_crop(image: Image.Image, row: str, cols: int, index: int, *, pad: float = 0.01) -> Image.Image:
    bands = {
        "q": (0.00, 0.34),
        "dash": (0.30, 0.59),
        "aura": (0.55, 0.99),
    }
    top, bottom = bands[row]
    left = max(0.0, index / cols - pad)
    right = min(1.0, (index + 1) / cols + pad)
    return normalized_crop(image, left, top, right, bottom)


def fit_sprite(
    image: Image.Image,
    *,
    frame_w: int,
    frame_h: int,
    target_h: int,
    max_w: int,
    baseline: int,
    center_x: int,
    x_offset: int = 0,
    y_offset: int = 0,
) -> Image.Image:
    sprite = trim_alpha(remove_green(image.copy()))
    if sprite.getchannel("A").getbbox() is None:
        return Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))

    scale = min(target_h / sprite.height, max_w / sprite.width)
    new_w = max(1, round(sprite.width * scale))
    new_h = max(1, round(sprite.height * scale))
    sprite = sprite.resize((new_w, new_h), Image.Resampling.LANCZOS)
    sprite = grade_demon_palette(sprite)
    sprite = hard_alpha(remove_tiny_components(sprite, min_pixels=10))

    canvas = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    x = center_x - new_w // 2 + x_offset
    y = baseline - new_h + y_offset
    canvas.alpha_composite(sprite, (x, y))
    return quantize_rgba(remove_tiny_components(canvas, min_pixels=10), 96)


def frame_box(frame: dict) -> tuple[int, int, int, int]:
    data = frame["data"]
    return (
        int(round(data["x"])),
        int(round(data["y"])),
        int(round(data["w"])),
        int(round(data["h"])),
    )


def pose_sequence(action: str, count: int) -> list[str]:
    sequences = {
        "idle": ["idle_a", "idle_a", "idle_b", "idle_b", "idle_b", "idle_a", "idle_a", "idle_b", "idle_a"],
        "run": ["run_a", "run_b", "run_a", "run_b", "run_a", "run_b", "run_a", "run_b"],
        "attack": ["idle_b", "attack", "attack", "attack", "attack", "attack", "attack", "idle_b", "idle_b"],
        "skill": ["idle_b", "cleave", "cleave", "cleave", "cleave", "cleave", "cleave", "idle_b"],
        "skill2": ["idle_b", "dash", "dash", "dash", "dash", "dash", "idle_b"],
        "ult": ["ult"],
        "hit": ["hit"],
        "dead": ["dead"],
    }
    sequence = sequences[action]
    if len(sequence) < count:
        sequence = [*sequence, *([sequence[-1]] * (count - len(sequence)))]
    return sequence[:count]


def frame_offsets(action: str, count: int) -> list[tuple[int, int]]:
    if action == "idle":
        pattern = [(0, 0), (1, -1), (1, -1), (0, 0), (0, 1), (-1, 0), (0, 0), (1, 0), (0, 0)]
        return pattern[:count]
    if action == "run":
        pattern = [(-2, 1), (2, -2), (-1, 1), (3, -2)]
        return [pattern[index % len(pattern)] for index in range(count)]
    if action in {"attack", "skill", "skill2"}:
        pattern = [(-1, 0), (0, 0), (1, 0), (0, 0)]
        return [
            (0, 0) if index in {0, count - 1} else pattern[(index - 1) % len(pattern)]
            for index in range(count)
        ]
    return [(0, 0)] * count


def actor_frame(
    source: Image.Image,
    action: str,
    pose: str,
    *,
    frame_w: int,
    frame_h: int,
    x_offset: int,
    y_offset: int = 0,
) -> Image.Image:
    crop = grid_crop(source, 5, 2, ACTOR_POSES[pose])
    if frame_w <= 60:
        return fit_sprite(
            crop,
            frame_w=frame_w,
            frame_h=frame_h,
            target_h=45,
            max_w=frame_w,
            baseline=frame_h - 5,
            center_x=frame_w // 2,
            x_offset=x_offset,
            y_offset=y_offset,
        )

    if pose in {"run_a", "run_b"}:
        target_h, max_w = 49, 88
    elif pose == "cleave":
        target_h, max_w = 62, 94
    elif pose == "dash":
        target_h, max_w = 53, 91
    elif pose == "attack":
        target_h, max_w = 49, 92
    else:
        target_h, max_w = 46, 80
    return fit_sprite(
        crop,
        frame_w=frame_w,
        frame_h=frame_h,
        target_h=target_h,
        max_w=max_w,
        baseline=frame_h - 8,
        center_x=43,
        x_offset=x_offset,
        y_offset=y_offset,
    )


def build_actor_sheet() -> None:
    source = load_rgba(ACTOR_SOURCE)
    vfx_source = load_rgba(VFX_SOURCE)
    rendered: list[tuple[str, int, float, Image.Image]] = []
    for action in ("skill", "skill2", "run", "attack", "idle", "hit", "dead", "ult"):
        durations = ACTION_DURATIONS[action]
        poses = pose_sequence(action, len(durations))
        offsets = frame_offsets(action, len(durations))
        dims = ACTION_FRAME_DIMS[action]
        for index, (duration, pose, (x_offset, y_offset), (frame_w, frame_h)) in enumerate(zip(durations, poses, offsets, dims)):
            frame = actor_frame(source, action, pose, frame_w=frame_w, frame_h=frame_h, x_offset=x_offset, y_offset=y_offset)
            if action == "skill2" and pose == "dash":
                frame = compose_dash_body_frame(vfx_source, frame, index)
            rendered.append((action, index, duration, frame))

    sheet = Image.new("RGBA", SILVERBEAR_SHEET_SIZE, (0, 0, 0, 0))
    anim: dict[str, dict[str, list[dict[str, object]]]] = {"anims": {action: {"frames": []} for action in ACTION_DURATIONS}}

    for action, index, duration, frame in rendered:
        frame_x = SILVERBEAR_FRAME_X[action][index]
        sheet.alpha_composite(frame, (frame_x, 0))
        anim["anims"][action]["frames"].append(
            {
                "duration": duration,
                "data": {
                    "x": float(frame_x),
                    "y": 0.0,
                    "w": float(frame.width),
                    "h": float(frame.height),
                },
            }
        )

    ACTOR_SHEET.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(ACTOR_SHEET)
    ACTOR_ANIM.write_text(json.dumps(anim, separators=(",", ":")), encoding="utf-8")


def build_actor_contact() -> None:
    source = load_rgba(ACTOR_SOURCE)
    samples = [
        ("idle", "idle", "idle_a", 54, 50),
        ("idle_b", "idle", "idle_b", 54, 50),
        ("run step A", "run", "run_a", 96, 72),
        ("run step B", "run", "run_b", 96, 72),
        ("attack body", "attack", "attack", 96, 72),
        ("skill body", "skill", "cleave", 96, 72),
        ("dash body", "skill2", "dash", 96, 72),
        ("ult cast body", "ult", "ult", 54, 50),
        ("hit body", "hit", "hit", 54, 50),
        ("dead body", "dead", "dead", 54, 50),
    ]
    cell_w, cell_h = 112, 104
    contact = Image.new("RGBA", (cell_w * 5, cell_h * 2), (22, 24, 32, 255))
    draw = ImageDraw.Draw(contact)
    for index, (label, action, pose, frame_w, frame_h) in enumerate(samples):
        col = index % 5
        row = index // 5
        ox = col * cell_w
        oy = row * cell_h
        draw.rectangle([ox, oy, ox + cell_w - 1, oy + cell_h - 1], outline=(72, 80, 94, 255))
        packed = actor_frame(source, action, pose, frame_w=frame_w, frame_h=frame_h, x_offset=0)
        if action == "skill2" and pose == "dash":
            packed = compose_dash_body_frame(load_rgba(VFX_SOURCE), packed, 2)
        contact.alpha_composite(packed, (ox + (cell_w - packed.width) // 2, oy + 10))
        draw.text((ox + 8, oy + 78), label, fill=(220, 230, 235, 255))
        draw.text((ox + 8, oy + 91), f"{packed.width}x{packed.height}", fill=(150, 165, 178, 255))
    CONTACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    contact.save(CONTACT_SHEET)


def crop_icon(source: Image.Image, index: int) -> Image.Image:
    cell = source.width // 3
    return source.crop((index * cell, 0, (index + 1) * cell, cell))


def polish_icon(icon: Image.Image) -> Image.Image:
    subject = trim_alpha(remove_green(icon))
    subject = ImageEnhance.Contrast(subject).enhance(1.12)
    subject = ImageEnhance.Color(subject).enhance(1.10)
    if subject.getchannel("A").getbbox() is None:
        subject = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
    subject.thumbnail((58, 58), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (64, 64), (18, 8, 13, 255))
    draw = ImageDraw.Draw(canvas)
    draw.rectangle([0, 0, 63, 63], outline=(155, 25, 35, 255), width=3)
    draw.rectangle([3, 3, 60, 60], outline=(42, 8, 12, 255), width=2)
    canvas.alpha_composite(subject, ((64 - subject.width) // 2, (64 - subject.height) // 2))
    return quantize_rgba(canvas, 96)


def build_icons() -> None:
    source = load_rgba(ICON_SOURCE)
    names = ["aatrox_skill.png", "aatrox_skill2.png", "aatrox_ult.png"]
    contact = Image.new("RGBA", (64 * 3, 64), (0, 0, 0, 0))
    for index, name in enumerate(names):
        polished = polish_icon(crop_icon(source, index))
        icon = polished.resize((24, 24), Image.Resampling.LANCZOS).convert("RGBA")
        (ROOT / "icons").mkdir(parents=True, exist_ok=True)
        icon.save(ROOT / "icons" / name)
        contact.alpha_composite(polished, (index * 64, 0))
    ICON_CONTACT.parent.mkdir(parents=True, exist_ok=True)
    contact.save(ICON_CONTACT)


def fit_effect(
    image: Image.Image,
    frame_w: int,
    frame_h: int,
    *,
    max_scale: float = 0.94,
    alpha_mult: float = 1.0,
    y_offset: int = 0,
) -> Image.Image:
    sprite = trim_alpha(remove_green(image.copy()))
    if sprite.getchannel("A").getbbox() is None:
        return Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    scale = min((frame_w * max_scale) / sprite.width, (frame_h * max_scale) / sprite.height)
    new_w = max(1, round(sprite.width * scale))
    new_h = max(1, round(sprite.height * scale))
    sprite = sprite.resize((new_w, new_h), Image.Resampling.LANCZOS)
    sprite = hard_alpha(sprite, threshold=24)
    canvas = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    canvas.alpha_composite(sprite, ((frame_w - new_w) // 2, (frame_h - new_h) // 2 + y_offset))
    result = quantize_rgba(remove_tiny_components(canvas, min_pixels=6), 96)
    if alpha_mult < 1.0:
        alpha = result.getchannel("A").point(lambda value: round(value * alpha_mult) if value else 0)
        result.putalpha(alpha)
    return result


def compose_dash_body_frame(vfx_source: Image.Image, body: Image.Image, index: int) -> Image.Image:
    trail_index = max(0, min(3, index - 1))
    trail_crop = vfx_row_crop(vfx_source, "dash", 4, trail_index, pad=0.02)
    trail = fit_effect(trail_crop, body.width, body.height, max_scale=0.92, alpha_mult=0.50, y_offset=3)
    canvas = Image.new("RGBA", body.size, (0, 0, 0, 0))
    canvas.alpha_composite(trail, (0, 0))
    canvas.alpha_composite(body, (0, 0))
    return quantize_rgba(canvas, 96)


def draw_attack_slash_frame(frame_w: int, frame_h: int, index: int, total: int) -> Image.Image:
    canvas = Image.new("RGBA", (frame_w, frame_h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    t = index / max(1, total - 1)
    alpha = round(230 * (1.0 - t * 0.45))
    bbox = [8 + round(t * 7), 4 + round(t * 5), frame_w - 6, frame_h - 5]
    for width, color in (
        (9, (28, 0, 8, round(alpha * 0.75))),
        (6, (150, 12, 24, alpha)),
        (3, (255, 72, 48, alpha)),
        (1, (255, 200, 118, round(alpha * 0.88))),
    ):
        draw.arc(bbox, start=292, end=52, fill=color, width=width)
    hit_x = frame_w - 25 + round(t * 6)
    hit_y = 32 + round(math.sin(t * math.pi) * 4)
    draw.polygon([(hit_x, hit_y - 8), (hit_x + 4, hit_y), (hit_x, hit_y + 8), (hit_x - 4, hit_y)], fill=(255, 84, 48, round(alpha * 0.86)))
    rng = random.Random(900 + index)
    for _ in range(9 - index):
        x = rng.randint(20, frame_w - 16)
        y = rng.randint(22, frame_h - 10)
        r = rng.choice([1, 1, 2])
        draw.ellipse([x - r, y - r, x + r, y + r], fill=(100, 6, 18, round(alpha * 0.55)))
    return quantize_rgba(canvas, 80)


def build_vfx() -> None:
    source = load_rgba(VFX_SOURCE)
    q_anim = json.loads(Q_IMPACT_ANIM.read_text(encoding="utf-8"))
    attack_anim = json.loads(ATTACK_SLASH_ANIM.read_text(encoding="utf-8"))
    aura_anim = json.loads(ULT_AURA_ANIM.read_text(encoding="utf-8"))

    attack_frames = attack_anim["anims"]["slash"]["frames"]
    attack_sheet = Image.new("RGBA", (96 * len(attack_frames), 72), (0, 0, 0, 0))
    for out_index, frame in enumerate(attack_frames):
        _, _, w, h = frame_box(frame)
        attack_sheet.alpha_composite(draw_attack_slash_frame(w, h, out_index, len(attack_frames)), (out_index * w, 0))
    ATTACK_SLASH_SHEET.parent.mkdir(parents=True, exist_ok=True)
    attack_sheet.save(ATTACK_SLASH_SHEET)

    q_frames = q_anim["anims"]["impact"]["frames"]
    q_sheet = Image.new("RGBA", (192 * len(q_frames), 96), (0, 0, 0, 0))
    for out_index, frame in enumerate(q_frames):
        _, _, w, h = frame_box(frame)
        crop = vfx_row_crop(source, "q", 6, out_index, pad=0.01)
        q_sheet.alpha_composite(fit_effect(crop, w, h, max_scale=0.94, alpha_mult=0.94, y_offset=2), (out_index * w, 0))
    Q_IMPACT_SHEET.parent.mkdir(parents=True, exist_ok=True)
    q_sheet.save(Q_IMPACT_SHEET)

    aura_frames = aura_anim["anims"]["loop"]["frames"]
    aura_sheet = Image.new("RGBA", (96 * len(aura_frames), 96), (0, 0, 0, 0))
    for out_index, frame in enumerate(aura_frames):
        _, _, w, h = frame_box(frame)
        crop = vfx_row_crop(source, "aura", 4, out_index, pad=0.015)
        aura_sheet.alpha_composite(fit_effect(crop, w, h, max_scale=0.86, alpha_mult=0.58, y_offset=6), (out_index * w, 0))
    ULT_AURA_SHEET.parent.mkdir(parents=True, exist_ok=True)
    aura_sheet.save(ULT_AURA_SHEET)

    contact_w = max(attack_sheet.width, q_sheet.width, aura_sheet.width)
    contact_h = attack_sheet.height + q_sheet.height + aura_sheet.height
    contact = Image.new("RGBA", (contact_w, contact_h), (22, 24, 32, 255))
    contact.alpha_composite(attack_sheet, (0, 0))
    contact.alpha_composite(q_sheet, (0, attack_sheet.height))
    contact.alpha_composite(aura_sheet, (0, attack_sheet.height + q_sheet.height))
    VFX_CONTACT.parent.mkdir(parents=True, exist_ok=True)
    contact.save(VFX_CONTACT)


def envelope(t: float, duration: float, attack: float = 0.02, release: float = 0.12) -> float:
    if t < attack:
        return t / attack
    if t > duration - release:
        return max(0.0, (duration - t) / release)
    return 1.0


def write_wav(path: Path, samples: list[float], sample_rate: int = 44100) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as out:
        out.setnchannels(1)
        out.setsampwidth(2)
        out.setframerate(sample_rate)
        frames = bytearray()
        for sample in samples:
            value = max(-1.0, min(1.0, sample))
            frames += int(value * 32767).to_bytes(2, "little", signed=True)
        out.writeframes(bytes(frames))


def synth_sweep(duration: float, start_hz: float, end_hz: float, *, noise: float, seed: int, gain: float) -> list[float]:
    rng = random.Random(seed)
    sample_rate = 44100
    total = int(duration * sample_rate)
    phase = 0.0
    samples: list[float] = []
    for i in range(total):
        t = i / sample_rate
        mix = t / duration
        hz = start_hz + (end_hz - start_hz) * mix
        phase += 2 * math.pi * hz / sample_rate
        tone = math.sin(phase) * 0.55 + math.sin(phase * 0.5) * 0.25
        hiss = (rng.random() * 2 - 1) * noise
        samples.append((tone + hiss) * envelope(t, duration) * gain)
    return samples


def synth_impact(duration: float, base_hz: float, *, seed: int, gain: float) -> list[float]:
    rng = random.Random(seed)
    sample_rate = 44100
    total = int(duration * sample_rate)
    samples: list[float] = []
    for i in range(total):
        t = i / sample_rate
        decay = math.exp(-8.0 * t)
        body = math.sin(2 * math.pi * base_hz * t) * decay
        crack = (rng.random() * 2 - 1) * math.exp(-22.0 * t)
        ring = math.sin(2 * math.pi * (base_hz * 2.8) * t) * math.exp(-5.0 * t)
        samples.append((body * 0.65 + crack * 0.45 + ring * 0.18) * envelope(t, duration, 0.004, 0.16) * gain)
    return samples


def mix(*tracks: list[float]) -> list[float]:
    total = max(len(track) for track in tracks)
    out = [0.0] * total
    for track in tracks:
        for index, sample in enumerate(track):
            out[index] += sample
    peak = max(max(abs(sample) for sample in out), 1.0)
    return [sample / peak * 0.92 for sample in out]


def delayed(track: list[float], seconds: float, sample_rate: int = 44100) -> list[float]:
    return [0.0] * int(seconds * sample_rate) + track


def build_sfx() -> None:
    write_wav(SFX_DIR / "test_mod_aatrox_attack_cast_clip.wav", synth_sweep(0.55, 760, 180, noise=0.20, seed=101, gain=0.60))
    write_wav(SFX_DIR / "test_mod_aatrox_attack_hit_clip.wav", synth_impact(0.62, 96, seed=102, gain=0.92))
    write_wav(SFX_DIR / "test_mod_aatrox_cleave_cast_clip.wav", mix(
        synth_sweep(0.86, 520, 90, noise=0.24, seed=103, gain=0.75),
        delayed(synth_sweep(0.42, 900, 260, noise=0.18, seed=104, gain=0.40), 0.18),
    ))
    write_wav(SFX_DIR / "test_mod_aatrox_cleave_hit_clip.wav", mix(
        synth_impact(0.78, 72, seed=105, gain=0.90),
        delayed(synth_impact(0.44, 140, seed=106, gain=0.55), 0.08),
    ))
    write_wav(SFX_DIR / "test_mod_aatrox_dash_effect_clip.wav", synth_sweep(0.72, 260, 980, noise=0.30, seed=107, gain=0.62))
    write_wav(SFX_DIR / "test_mod_aatrox_dash_voice_clip.wav", mix(
        synth_sweep(0.64, 150, 70, noise=0.08, seed=108, gain=0.58),
        delayed(synth_impact(0.36, 65, seed=109, gain=0.35), 0.10),
    ))
    write_wav(SFX_DIR / "test_mod_aatrox_ult_cast_clip.wav", mix(
        synth_sweep(1.35, 92, 48, noise=0.12, seed=110, gain=0.72),
        delayed(synth_sweep(0.95, 320, 900, noise=0.22, seed=111, gain=0.55), 0.18),
        delayed(synth_impact(0.90, 58, seed=112, gain=0.82), 0.35),
    ))


def write_qa_matrix() -> None:
    rows = [
        ("actor", str(ACTOR_SHEET.relative_to(ROOT)), str(ACTOR_SOURCE.relative_to(ROOT)), "design-book rebuild: larger compact demon silhouette, stronger run poses, stable existing frame contract"),
        ("icons", "icons/aatrox_skill.png;icons/aatrox_skill2.png;icons/aatrox_ult.png", str(ICON_SOURCE.relative_to(ROOT)), "green removed, dark framed, 24x24 outputs with Q slash / E dash / R transform reads"),
        ("vfx", str(ATTACK_SLASH_SHEET.relative_to(ROOT)), "procedural compact red-black slash", "4 frame caster-follow basic attack slash, 96x72 per frame"),
        ("vfx", str(Q_IMPACT_SHEET.relative_to(ROOT)), str(VFX_SOURCE.relative_to(ROOT)), "6 frame long ground-crack cleave, 192x96 per frame, not a circular explosion"),
        ("vfx", "skill2 body frames", str(VFX_SOURCE.relative_to(ROOT)), "dash trail composited into existing skill2 actor frames without changing champion data"),
        ("vfx", str(ULT_AURA_SHEET.relative_to(ROOT)), str(VFX_SOURCE.relative_to(ROOT)), "4 frame low-opacity world-ender aura loop, 96x96 per frame, reduced face/body obstruction"),
        ("sfx", "sound/sfx/test_mod_aatrox_*_clip.wav", "existing workshop package", "event names and audio files preserved"),
        ("view", "style/champion_view.champion_view", "existing tuned offsets", "face x=0 y=-20 and center x=0 y=-15 preserved"),
    ]
    QA_MATRIX.parent.mkdir(parents=True, exist_ok=True)
    with QA_MATRIX.open("w", newline="", encoding="utf-8") as out:
        writer = csv.writer(out)
        writer.writerow(["asset_type", "output", "source", "contract"])
        writer.writerows(rows)


def main() -> int:
    build_actor_sheet()
    build_actor_contact()
    build_icons()
    build_vfx()
    write_qa_matrix()
    print("aatrox_design_rework_assets=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
