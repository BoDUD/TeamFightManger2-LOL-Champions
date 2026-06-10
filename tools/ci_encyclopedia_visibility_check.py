from __future__ import annotations

import json
import hashlib
import sys
import zlib
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
MOD_ID = "bo_league_champions"
EXPECTED_CHAMPIONS = {
    "aatrox",
    "azir",
    "ezreal",
    "fiddlesticks",
    "fizz",
    "jhin",
    "jinx",
    "kayn",
    "vayne",
    "veigar",
    "viktor",
    "yasuo",
}
REQUIRED_DESCRIPTION_KEYS = ("name", "attack", "skill", "skill2", "ult")
PROCESS_IMAGE_ROOTS = ("source", "qa")
PROCESS_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
ROSTER_VISIBILITY_COVERAGE_PATH = ROOT / "qa" / "roster_visibility_coverage.json"
AATROX_IDS = ("bo_league_champions_aatrox", "test_mod_aatrox")
AATROX_EFFECT_REFS = {
    "test_mod_aatrox_q1": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_q1_cleave",
        "q1",
    ),
    "test_mod_aatrox_q2": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_q2_cleave",
        "q2",
    ),
    "test_mod_aatrox_q3": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_q3_cleave",
        "q3",
    ),
    "test_mod_aatrox_infernal_chains": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_w_chain",
        "chain",
    ),
    "test_mod_aatrox_infernal_chains_snap": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_w_chain_snap",
        "snap",
    ),
}
AATROX_BUFF_REFS = {
    "test_mod_aatrox_world_ender": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_world_ender_aura",
        "loop",
    ),
}
AATROX_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
AATROX_VIKTOR_FRAME_SIZE = (57.0, 54.0)
AATROX_MIN_DISPLAY_BOTTOM_SAFE_PIXELS = 14
AATROX_MIN_ACTION_BOTTOM_SAFE_PIXELS = 7
AATROX_MAX_DISPLAY_BODY_HEIGHT = 36
AATROX_MAX_ACTION_BODY_HEIGHT = 45
AATROX_MIN_RUN_FOOT_CENTER_RANGE = 0.9
AATROX_MIN_RUN_FOOT_SHAPES = 5
AATROX_MIN_RUN_FOOT_PIXELS = 24
AATROX_MIN_RUN_LOWER_PIXELS = 40
AATROX_IDLE_FRAME_XS = (0, 96, 192, 288, 384, 480, 576, 672, 768)
AATROX_ULT_FRAME_X = 864
AATROX_HIT_FRAME_X = 960
AATROX_DEAD_FRAME_X = 1056
AATROX_RETIRED_MODEL_FRAME_XS = (5868, 5964, 6060, 6156, 6252, 6348, 6444, 6540, 6636)
AATROX_RUN_FRAME_XS = (4224, 4320, 4416, 4512, 4608, 4704, 4800, 4896)
AATROX_ATTACK_FRAME_XS = (4992, 5088, 5184, 5280, 5376, 5472, 5568, 5664, 5760)
AATROX_SKILL_FRAME_XS = (2784, 2880, 2976, 3072, 3168, 3264, 3360, 3456)
AATROX_SKILL2_FRAME_XS = (3552, 3648, 3744, 3840, 3936, 4032, 4128)
AATROX_ALLOWED_FRAME_XS = tuple(
    sorted(
        set(
            AATROX_IDLE_FRAME_XS
            + (AATROX_ULT_FRAME_X, AATROX_HIT_FRAME_X, AATROX_DEAD_FRAME_X)
            + AATROX_RUN_FRAME_XS
            + AATROX_ATTACK_FRAME_XS
            + AATROX_SKILL_FRAME_XS
            + AATROX_SKILL2_FRAME_XS
        )
    )
)
AATROX_ATTACK_CAST_EFFECT_REFS = {
    "test_mod_aatrox_attack_slash_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_attack_slash",
        "slash",
    ),
}
AATROX_Q_CAST_EFFECT_REFS = {
    "test_mod_aatrox_q1_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_q1_cleave",
        "q1",
    ),
    "test_mod_aatrox_q2_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_q2_cleave",
        "q2",
    ),
    "test_mod_aatrox_q3_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/aatrox_q3_cleave",
        "q3",
    ),
}
KAYN_IDS = ("bo_league_champions_kayn", "test_mod_kayn")
KAYN_EFFECT_REFS = {
    "test_mod_kayn_q_slash": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_q_slash",
        "slash",
    ),
    "test_mod_kayn_w_blade_reach": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_w_blade_reach",
        "blade",
    ),
}
KAYN_VIEW_EFFECT_REFS = {
    "test_mod_kayn_r_entry": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_r_entry",
        "entry",
    ),
    "test_mod_kayn_r_exit": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_r_exit",
        "exit",
    ),
}
KAYN_BUFF_REFS = {
    "test_mod_kayn_darkin_ascension": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_darkin_aura",
        "loop",
    ),
}
KAYN_SOUND_MEDIA_IDS = {
    "test_mod_kayn_attack_cast": "1231310",
    "test_mod_kayn_attack_hit": "673548444",
    "test_mod_kayn_q_cast": "16234722",
    "test_mod_kayn_q_hit": "249093668",
    "test_mod_kayn_w_cast": "533812089",
    "test_mod_kayn_w_hit": "800215479",
    "test_mod_kayn_r_cast": "49181076",
    "test_mod_kayn_r_hit": "710731227",
    "test_mod_kayn_ult_voice": "136354677",
}
KAYN_SKILL_SOUND_EVENTS = {
    "test_mod_kayn_q_cast",
    "test_mod_kayn_q_hit",
    "test_mod_kayn_w_cast",
    "test_mod_kayn_w_hit",
    "test_mod_kayn_r_cast",
    "test_mod_kayn_r_hit",
    "test_mod_kayn_ult_voice",
}
KAYN_SKILL_SOUND_VOLUME_FLOOR = 0.78
KAYN_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
KAYN_FRAME_SIZE = (57.0, 54.0)
YASUO_IDS = ("bo_league_champions_yasuo", "test_mod_yasuo")
YASUO_FRAME_SIZE = (57.0, 54.0)
YASUO_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
YASUO_EFFECT_REFS = {
    "test_mod_yasuo_q_stab": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_q_stab",
        "stab",
    ),
    "test_mod_yasuo_q_tornado": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_q_tornado",
        "tornado",
    ),
    "test_mod_yasuo_sweeping_blade": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_sweeping_blade",
        "dash",
    ),
    "test_mod_yasuo_wind_wall_barrier": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_wind_wall",
        "wall",
    ),
}
YASUO_VIEW_EFFECT_REFS = {
    "test_mod_yasuo_attack_slash_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_attack_slash",
        "slash",
    ),
    "test_mod_yasuo_q_stab_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_q_stab",
        "stab",
    ),
    "test_mod_yasuo_q_tornado_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_q_tornado",
        "tornado",
    ),
    "test_mod_yasuo_sweeping_blade_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_sweeping_blade",
        "dash",
    ),
    "test_mod_yasuo_wind_wall_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_wind_wall",
        "wall",
    ),
    "test_mod_yasuo_last_breath_burst": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_last_breath",
        "burst",
    ),
}
YASUO_BUFF_REFS = {
    "test_mod_yasuo_flow_shield_visual": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_flow_shield",
        "loop",
    ),
    "test_mod_yasuo_after_breath": (
        "asset/bo_league_champions/aseprite_resources/effects/yasuo_after_breath_aura",
        "loop",
    ),
}
YASUO_SOUND_MEDIA_IDS = {
    "test_mod_yasuo_attack_cast": "846111995",
    "test_mod_yasuo_attack_hit": "316775153",
    "test_mod_yasuo_q_cast": "406877763",
    "test_mod_yasuo_q_hit": "274810394",
    "test_mod_yasuo_q_tornado_cast": "153026395",
    "test_mod_yasuo_q_tornado_hit": "270102972",
    "test_mod_yasuo_dash_cast": "136033610",
    "test_mod_yasuo_dash_hit": "620318014",
    "test_mod_yasuo_wind_wall_cast": "663920909",
    "test_mod_yasuo_r_cast": "122167141",
    "test_mod_yasuo_r_hit": "706858599",
    "test_mod_yasuo_ult_voice": "959232333",
}
YASUO_SKILL_SOUND_EVENTS = {
    "test_mod_yasuo_q_cast",
    "test_mod_yasuo_q_hit",
    "test_mod_yasuo_q_tornado_cast",
    "test_mod_yasuo_q_tornado_hit",
    "test_mod_yasuo_dash_cast",
    "test_mod_yasuo_dash_hit",
    "test_mod_yasuo_wind_wall_cast",
    "test_mod_yasuo_r_cast",
    "test_mod_yasuo_r_hit",
    "test_mod_yasuo_ult_voice",
}
YASUO_SKILL_SOUND_VOLUME_FLOOR = 0.80
JINX_IDS = ("bo_league_champions_jinx", "test_mod_jinx")
JINX_FRAME_SIZE = (57.0, 54.0)
JINX_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
JINX_EFFECT_REFS = {
    "test_mod_jinx_minigun_bullet": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_minigun_bullet",
        "projectile",
    ),
    "test_mod_jinx_rocket_attack": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_rocket_attack",
        "projectile",
    ),
    "test_mod_jinx_zap": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_zap",
        "beam",
    ),
    "test_mod_jinx_flame_chompers": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_flame_chompers",
        "trap",
    ),
    "test_mod_jinx_super_mega_death_rocket": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_super_mega_death_rocket",
        "rocket",
    ),
}
JINX_VIEW_EFFECT_REFS = {
    "test_mod_jinx_switcheroo_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_switcheroo",
        "switch",
    ),
    "test_mod_jinx_rocket_explosion_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_rocket_explosion",
        "burst",
    ),
}
JINX_BUFF_REFS = {
    "test_mod_jinx_get_excited": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_get_excited_aura",
        "loop",
    ),
    "test_mod_jinx_fishbones_visual": (
        "asset/bo_league_champions/aseprite_resources/effects/jinx_fishbones_mode_aura",
        "loop",
    ),
}
JINX_SOUND_MEDIA_IDS = {
    "test_mod_jinx_minigun_cast": "871511008",
    "test_mod_jinx_minigun_hit": "230875545",
    "test_mod_jinx_rocket_cast": "1043413444",
    "test_mod_jinx_rocket_hit": "411020415",
    "test_mod_jinx_switch_to_minigun": "130431412",
    "test_mod_jinx_switch_to_rocket": "148352341",
    "test_mod_jinx_zap_cast": "995389952",
    "test_mod_jinx_zap_hit": "670846690",
    "test_mod_jinx_chompers_cast": "838897672",
    "test_mod_jinx_chompers_trigger": "1062072193",
    "test_mod_jinx_r_cast": "568985478",
    "test_mod_jinx_r_hit": "203216632",
    "test_mod_jinx_get_excited": "581983763",
    "test_mod_jinx_ult_voice": "870699277",
}
JINX_SKILL_SOUND_EVENTS = {
    "test_mod_jinx_switch_to_minigun",
    "test_mod_jinx_switch_to_rocket",
    "test_mod_jinx_zap_cast",
    "test_mod_jinx_zap_hit",
    "test_mod_jinx_chompers_cast",
    "test_mod_jinx_chompers_trigger",
    "test_mod_jinx_r_cast",
    "test_mod_jinx_r_hit",
    "test_mod_jinx_get_excited",
    "test_mod_jinx_ult_voice",
}
JINX_SKILL_SOUND_VOLUME_FLOOR = 0.84
REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS: dict[str, dict[str, tuple[str, ...]]] = {}
for _champion_id in AATROX_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Aatrox",),
        "zh-hans": ("\u4e9a\u6258\u514b\u65af", "\u5251\u9b54"),
        "zh-hant": ("\u4e9e\u6258\u514b\u65af", "\u528d\u9b54"),
    }
for _champion_id in KAYN_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Kayn", "Shadow Reaper"),
        "zh-hans": ("\u5f71\u6d41\u4e4b\u9570", "\u51ef\u9690"),
        "zh-hant": ("\u5f71\u6d41\u4e4b\u942e", "\u6168\u5f71"),
    }
for _champion_id in YASUO_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Yasuo", "Unforgiven"),
        "zh-hans": ("\u75be\u98ce\u5251\u8c6a", "\u4e9a\u7d22"),
        "zh-hant": ("\u75be\u98a8\u528d\u8c6a", "\u72bd\u5bbf"),
    }
for _champion_id in JINX_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Jinx", "Loose Cannon"),
        "zh-hans": ("\u66b4\u8d70\u841d\u8389", "\u91d1\u514b\u4e1d"),
        "zh-hant": ("\u66b4\u8d70\u863f\u8389", "\u91d1\u514b\u7d72"),
    }
AATROX_SOUND_MEDIA_IDS = {
    "test_mod_aatrox_attack_cast": ("29529616",),
    "test_mod_aatrox_attack_hit": ("780778749",),
    "test_mod_aatrox_cleave_cast": ("500087760",),
    "test_mod_aatrox_cleave_hit": ("711456995",),
    "test_mod_aatrox_dash_cast": ("243486348", "19360160"),
    "test_mod_aatrox_ult_cast": ("544373583",),
    "test_mod_aatrox_ult_voice": ("216379411",),
}
AATROX_SKILL_SOUND_VOLUME_FLOOR = 0.80


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # pragma: no cover - failure path prints file context
        raise AssertionError(f"{path.relative_to(ROOT)} is not valid JSON: {exc}") from exc


def load_rgba(path: Path) -> tuple[int, int, bytes]:
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        fail(f"{path.relative_to(ROOT)} is not a PNG file")

    offset = 8
    width = height = bit_depth = color_type = interlace = None
    idat = bytearray()
    while offset < len(raw):
        length = int.from_bytes(raw[offset : offset + 4], "big")
        chunk_type = raw[offset + 4 : offset + 8]
        chunk_data = raw[offset + 8 : offset + 8 + length]
        offset += 12 + length
        if chunk_type == b"IHDR":
            width = int.from_bytes(chunk_data[0:4], "big")
            height = int.from_bytes(chunk_data[4:8], "big")
            bit_depth = chunk_data[8]
            color_type = chunk_data[9]
            interlace = chunk_data[12]
        elif chunk_type == b"IDAT":
            idat.extend(chunk_data)
        elif chunk_type == b"IEND":
            break

    if width is None or height is None:
        fail(f"{path.relative_to(ROOT)} missing PNG IHDR")
    if bit_depth != 8 or color_type != 6 or interlace != 0:
        fail(f"{path.relative_to(ROOT)} must be non-interlaced 8-bit RGBA PNG for alpha QA")

    data = zlib.decompress(bytes(idat))
    bpp = 4
    stride = width * bpp
    rows: list[bytearray] = []
    pos = 0
    for row_index in range(height):
        filter_type = data[pos]
        pos += 1
        row = bytearray(data[pos : pos + stride])
        pos += stride
        prev = rows[row_index - 1] if row_index else bytearray(stride)
        for i in range(stride):
            left = row[i - bpp] if i >= bpp else 0
            up = prev[i]
            up_left = prev[i - bpp] if i >= bpp else 0
            if filter_type == 0:
                recon = row[i]
            elif filter_type == 1:
                recon = row[i] + left
            elif filter_type == 2:
                recon = row[i] + up
            elif filter_type == 3:
                recon = row[i] + ((left + up) // 2)
            elif filter_type == 4:
                p = left + up - up_left
                pa = abs(p - left)
                pb = abs(p - up)
                pc = abs(p - up_left)
                predictor = left if pa <= pb and pa <= pc else up if pb <= pc else up_left
                recon = row[i] + predictor
            else:
                fail(f"{path.relative_to(ROOT)} has unsupported PNG row filter {filter_type}")
            row[i] = recon & 0xFF
        rows.append(row)

    rgba = bytearray(width * height * bpp)
    for y, row in enumerate(rows):
        start = y * stride
        rgba[start : start + stride] = row
    return width, height, bytes(rgba)


def load_rgba_alpha(path: Path) -> tuple[int, int, bytes]:
    width, height, rgba = load_rgba(path)
    alpha = bytearray(width * height)
    for i in range(width * height):
        alpha[i] = rgba[i * 4 + 3]
    return width, height, bytes(alpha)


def alpha_bbox_in_rect(
    alpha: bytes, image_width: int, rect: tuple[int, int, int, int]
) -> tuple[int, int, int, int] | None:
    x0, y0, w, h = rect
    min_x = min_y = 10**9
    max_x = max_y = -1
    for y in range(y0, y0 + h):
        row_start = y * image_width
        for x in range(x0, x0 + w):
            if alpha[row_start + x] != 0:
                local_x = x - x0
                local_y = y - y0
                min_x = min(min_x, local_x)
                min_y = min(min_y, local_y)
                max_x = max(max_x, local_x + 1)
                max_y = max(max_y, local_y + 1)
    if max_x < 0:
        return None
    return min_x, min_y, max_x, max_y


def alpha_frame_hash(alpha: bytes, image_width: int, rect: tuple[int, int, int, int]) -> str:
    x0, y0, w, h = rect
    digest = hashlib.sha1()
    for y in range(y0, y0 + h):
        start = y * image_width + x0
        digest.update(alpha[start : start + w])
    return digest.hexdigest()


def count_green_residue(path: Path) -> int:
    width, height, rgba = load_rgba(path)
    offenders = 0
    for i in range(width * height):
        r = rgba[i * 4]
        g = rgba[i * 4 + 1]
        b = rgba[i * 4 + 2]
        a = rgba[i * 4 + 3]
        if a and g > 90 and g > r * 1.18 and g > b * 1.18:
            offenders += 1
    return offenders


def require_no_green_residue(path: Path) -> None:
    offenders = count_green_residue(path)
    if offenders:
        fail(f"{path.relative_to(ROOT)} still contains {offenders} green-screen residue pixels")


def count_aatrox_green_spill(path: Path) -> int:
    width, height, rgba = load_rgba(path)
    offenders = 0
    for i in range(width * height):
        r = rgba[i * 4]
        g = rgba[i * 4 + 1]
        b = rgba[i * 4 + 2]
        a = rgba[i * 4 + 3]
        if a and g > 45 and g > b * 1.25 and g > r * 0.65:
            offenders += 1
    return offenders


def require_no_aatrox_green_spill(path: Path) -> None:
    offenders = count_aatrox_green_spill(path)
    if offenders:
        fail(f"{path.relative_to(ROOT)} has {offenders} green/cyan spill pixels in Aatrox red-black VFX")


def local_asset_path(asset: str) -> Path:
    prefix = f"asset/{MOD_ID}/"
    if not asset.startswith(prefix):
        fail(f"asset path must use {prefix}: {asset}")
    return ROOT / asset[len(prefix) :]


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")


def assert_jinx_fishbones_held_overlay() -> None:
    sheet = ROOT / "aseprite_resources" / "effects" / "jinx_fishbones_mode_aura#sheet.png"
    width, height, rgba = load_rgba(sheet)
    _, _, alpha = load_rgba_alpha(sheet)
    if (width, height) != (384, 64):
        fail("Jinx Fishbones visual must keep the 6-frame 64x64 held-weapon overlay contract")
    for frame_index in range(6):
        x0 = frame_index * 64
        bbox = alpha_bbox_in_rect(alpha, width, (x0, 0, 64, 64))
        if bbox is None:
            fail(f"Jinx Fishbones held overlay frame {frame_index} is empty")
        bw = bbox[2] - bbox[0]
        bh = bbox[3] - bbox[1]
        if bw > 44 or bh > 32:
            fail(
                f"Jinx Fishbones frame {frame_index} must be a compact held weapon, "
                f"not a rocket/smoke aura; bbox is {bw}x{bh}"
            )
        if bbox[0] < 16 or bbox[1] < 14 or bbox[3] > 50:
            fail(
                f"Jinx Fishbones frame {frame_index} must stay near the hand/shoulder weapon area; "
                f"bbox is {bbox}"
            )
        visible = 0
        flame_pixels = 0
        for y in range(bbox[1], bbox[3]):
            for x in range(bbox[0], bbox[2]):
                i = ((y * width) + x0 + x) * 4
                r = rgba[i]
                g = rgba[i + 1]
                b = rgba[i + 2]
                a = rgba[i + 3]
                if not a:
                    continue
                visible += 1
                if r > 180 and g > 70 and b < 80:
                    flame_pixels += 1
        if visible < 120:
            fail(f"Jinx Fishbones held overlay frame {frame_index} is too sparse to read as a weapon")
        if flame_pixels:
            fail(
                f"Jinx Fishbones held overlay frame {frame_index} still contains muzzle flame; "
                "fire and smoke belong in projectile/hit effects, not the actor buff"
            )


def require_aseprite_asset(asset: str) -> None:
    base = local_asset_path(asset)
    require_file(Path(f"{base}#sheet.png"))
    require_file(Path(f"{base}#anim.fanim"))


def require_png_asset(asset: str) -> None:
    require_file(local_asset_path(asset).with_suffix(".png"))


def require_wave_asset(event_name: str) -> dict[str, Any]:
    sound_info = ROOT / "sound" / "sfx" / f"{event_name}.sound_info"
    clip = ROOT / "sound" / "sfx" / f"{event_name}_clip.wav"
    require_file(sound_info)
    require_file(clip)
    info = load_json(sound_info)
    if not isinstance(info, dict):
        fail(f"{sound_info.relative_to(ROOT)} must contain a JSON object")
    plays = info.get("plays")
    if (
        not isinstance(plays, list)
        or not plays
        or not isinstance(plays[0], dict)
        or plays[0].get("clip") != f"{event_name}_clip"
    ):
        fail(f"{sound_info.relative_to(ROOT)} must point at {event_name}_clip")
    payload = clip.read_bytes()
    if len(payload) < 1000 or not payload.startswith(b"RIFF") or payload[8:12] != b"WAVE":
        fail(f"{clip.relative_to(ROOT)} must be a decoded official wav clip")
    return info


def require_sound_info_assets(event_name: str) -> dict[str, Any]:
    sound_info = ROOT / "sound" / "sfx" / f"{event_name}.sound_info"
    require_file(sound_info)
    info = load_json(sound_info)
    if not isinstance(info, dict):
        fail(f"{sound_info.relative_to(ROOT)} must contain a JSON object")
    plays = info.get("plays")
    if not isinstance(plays, list) or not plays:
        fail(f"{sound_info.relative_to(ROOT)} must contain at least one play")
    for index, play in enumerate(plays):
        if not isinstance(play, dict):
            fail(f"{sound_info.relative_to(ROOT)} plays[{index}] must be an object")
        clip_name = play.get("clip")
        if not isinstance(clip_name, str) or not clip_name:
            fail(f"{sound_info.relative_to(ROOT)} plays[{index}] must name a clip")
        clip = ROOT / "sound" / "sfx" / f"{clip_name}.wav"
        require_file(clip)
        payload = clip.read_bytes()
        if len(payload) < 1000 or not payload.startswith(b"RIFF") or payload[8:12] != b"WAVE":
            fail(f"{clip.relative_to(ROOT)} must be a decoded official wav clip")
        volume = play.get("volume")
        if not isinstance(volume, (int, float)) or volume <= 0:
            fail(f"{sound_info.relative_to(ROOT)} plays[{index}] must set a positive volume")
    return info


def assert_official_audio_sources(
    champion_name: str,
    source_file: str,
    bank_file: str,
    event_media_ids: dict[str, str] | dict[str, tuple[str, ...]],
    skill_events: set[str],
    volume_floor: float,
) -> None:
    official = load_json(ROOT / "qa" / f"{champion_name}_official_audio_sources.json")
    if not isinstance(official, dict):
        fail(f"qa/{champion_name}_official_audio_sources.json must contain a JSON object")
    if source_file not in str(official.get("source", "")):
        fail(f"{champion_name} audio source must document official {source_file}")
    if bank_file not in str(official.get("bank", "")):
        fail(f"{champion_name} audio source must document official {bank_file}")
    events = official.get("events")
    if not isinstance(events, dict):
        fail(f"qa/{champion_name}_official_audio_sources.json missing events object")
    overrides = load_json(ROOT / "mod.override_info")
    for event_name, expected_media in event_media_ids.items():
        row = events.get(event_name)
        if not isinstance(row, dict):
            fail(f"official {champion_name} audio event {event_name} is missing")
        sound_info = require_sound_info_assets(event_name)
        plays = sound_info.get("plays")
        assert isinstance(plays, list)
        expected_ids = expected_media if isinstance(expected_media, tuple) else (expected_media,)
        if len(expected_ids) == 1:
            if str(row.get("media_id")) != expected_ids[0]:
                fail(f"official {champion_name} audio event {event_name} must document media_id {expected_ids[0]}")
        else:
            clips = row.get("clips")
            if not isinstance(clips, list):
                fail(f"official {champion_name} audio event {event_name} must document clip media IDs")
            got_ids = tuple(str(item.get("media_id")) for item in clips if isinstance(item, dict))
            if got_ids != expected_ids:
                fail(f"official {champion_name} audio event {event_name} media IDs must be {expected_ids}, got {got_ids}")
        for suffix in ("", "_clip"):
            key = f"asset/base/sound/sfx/{event_name}{suffix}"
            if suffix == "_clip" and not (ROOT / "sound" / "sfx" / f"{event_name}_clip.wav").is_file():
                continue
            expected_remap = f"asset/bo_league_champions/sound/sfx/{event_name}{suffix}"
            override = overrides.get(key)
            if not isinstance(override, dict) or override.get("remapping") != expected_remap or override.get("type") != "override":
                fail(f"mod.override_info must override {key} to {expected_remap}")
        if event_name in skill_events:
            for index, play in enumerate(plays):
                volume = play.get("volume") if isinstance(play, dict) else None
                if not isinstance(volume, (int, float)) or volume < volume_floor:
                    fail(f"{event_name}.sound_info plays[{index}] volume must be at least {volume_floor}")


def walk_strings(node: Any) -> list[str]:
    if isinstance(node, str):
        return [node]
    if isinstance(node, list):
        out: list[str] = []
        for item in node:
            out.extend(walk_strings(item))
        return out
    if isinstance(node, dict):
        out: list[str] = []
        for value in node.values():
            out.extend(walk_strings(value))
        return out
    return []


def check_encyclopedia_search_terms(text: dict[str, Any]) -> None:
    for champion_id, terms_by_locale in REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS.items():
        for locale, required_terms in terms_by_locale.items():
            descriptions = text.get(locale, {}).get("description")
            if not isinstance(descriptions, dict):
                fail(f"text/champion.i18n locale {locale} missing description object")
            row = descriptions.get(champion_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {champion_id}")
            surface = " ".join(str(row.get(key, "")) for key in REQUIRED_DESCRIPTION_KEYS).casefold()
            missing = [term for term in required_terms if term.casefold() not in surface]
            if missing:
                fail(
                    f"text/champion.i18n locale {locale} {champion_id} "
                    f"is missing encyclopedia search terms {missing}"
                )


def description_refs(champion: dict[str, Any]) -> set[tuple[str, str]]:
    refs: set[tuple[str, str]] = set()
    prefix = "#asset/base/text/champion?description."
    for value in walk_strings(champion):
        if not value.startswith(prefix):
            continue
        rest = value[len(prefix) :]
        parts = rest.split(".")
        if len(parts) != 2:
            fail(f"bad champion description reference: {value}")
        refs.add((parts[0], parts[1]))
    return refs


def check_view_effect_types(path: Path, champion: dict[str, Any]) -> None:
    # view_projectiles accepts "Animated"; view_effects does not in this game build.
    # A bad view_effect enum rejects the whole data_champion at startup, which hides it from encyclopedia search.
    allowed = {"Animation", "LoopAnimation"}
    for index, effect in enumerate(champion.get("view_effects", [])):
        if not isinstance(effect, dict):
            fail(f"{path.relative_to(ROOT)} view_effects[{index}] must be an object")
        effect_type = effect.get("type")
        if effect_type not in allowed:
            fail(
                f"{path.relative_to(ROOT)} view_effects[{index}].type must be one of "
                f"{sorted(allowed)}, got {effect_type!r}"
            )


def check_effect_shapes(path: Path, node: Any) -> None:
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "applied_effects":
                if not isinstance(value, list):
                    fail(f"{path.relative_to(ROOT)} applied_effects must be a list")
                for index, item in enumerate(value):
                    if not isinstance(item, dict):
                        fail(f"{path.relative_to(ROOT)} applied_effects[{index}] must be an object")
                    has_wrapped_effect = isinstance(item.get("effect"), dict)
                    has_direct_effect = isinstance(item.get("type"), str)
                    if not has_wrapped_effect and not has_direct_effect:
                        fail(f"{path.relative_to(ROOT)} applied_effects[{index}] missing effect/type object")
                    if has_wrapped_effect and not isinstance(item.get("casting_type"), str):
                        fail(f"{path.relative_to(ROOT)} applied_effects[{index}] missing casting_type")
            check_effect_shapes(path, value)
    elif isinstance(node, list):
        for item in node:
            check_effect_shapes(path, item)


def check_mod_metadata() -> None:
    info = load_json(ROOT / "mod.mod_info")
    if info.get("id") != MOD_ID:
        fail(f"mod.mod_info id must be {MOD_ID}, got {info.get('id')!r}")
    if info.get("mod_id") != MOD_ID:
        fail(f"mod.mod_info mod_id must be {MOD_ID}, got {info.get('mod_id')!r}")
    if info.get("name") != "BO-League Champions":
        fail(f"mod.mod_info name must be BO-League Champions, got {info.get('name')!r}")

    overrides = load_json(ROOT / "mod.override_info")
    expected = {
        "asset/base/text/champion": ("asset/bo_league_champions/text/champion", "merge"),
        "asset/base/style/champion_view": ("asset/bo_league_champions/style/champion_view", "merge"),
    }
    for key, (remapping, override_type) in expected.items():
        row = overrides.get(key)
        if row is None:
            fail(f"mod.override_info must include {key}")
        if row.get("remapping") != remapping or row.get("type") != override_type:
            fail(f"{key} must remap to {remapping} as {override_type}, got {row!r}")


def check_no_process_images() -> None:
    offenders: list[str] = []
    for root_name in PROCESS_IMAGE_ROOTS:
        root = ROOT / root_name
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in PROCESS_IMAGE_SUFFIXES:
                offenders.append(str(path.relative_to(ROOT)))
    if offenders:
        fail(f"process/source images must not be committed after rebuild: {offenders}")


def check_roster_visibility_coverage() -> None:
    coverage = load_json(ROSTER_VISIBILITY_COVERAGE_PATH)
    if not isinstance(coverage, dict):
        fail("qa/roster_visibility_coverage.json must contain a JSON object")
    if coverage.get("native_retirement_mode") != "coverage-gated-staged-retirement":
        fail("roster visibility coverage must use coverage-gated-staged-retirement mode")
    if coverage.get("verified_hide_path") is not False:
        fail("roster visibility coverage must not claim native heroes are hidden until a verified path exists")
    champions = coverage.get("league_champions")
    if sorted(champions or []) != sorted(EXPECTED_CHAMPIONS):
        fail(
            "qa/roster_visibility_coverage.json league_champions must match champion/*.data_champion "
            f"{sorted(EXPECTED_CHAMPIONS)}"
        )
    visible_policy = coverage.get("visible_native_policy")
    if not isinstance(visible_policy, dict):
        fail("roster visibility coverage must define visible_native_policy")
    if visible_policy.get("new_untracked_native_leftovers") != "blocked":
        fail("new native leftovers must be blocked by roster visibility policy")
    accepted = visible_policy.get("accepted_statuses")
    if accepted != ["covered_by_league", "retire_pending_verified_hide_path"]:
        fail("roster visibility accepted statuses changed; update CI before changing native retirement semantics")
    queue = coverage.get("native_retirement_queue")
    if not isinstance(queue, list) or not queue:
        fail("native_retirement_queue must track currently visible native heroes until a hide path is proven")
    for index, row in enumerate(queue):
        if not isinstance(row, dict):
            fail(f"native_retirement_queue[{index}] must be an object")
        if row.get("status") not in accepted:
            fail(f"native_retirement_queue[{index}] has unsupported status {row.get('status')!r}")


def check_aatrox_rework_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_names = {
        "zh-hans": ("\u4e9a\u6258\u514b\u65af",),
        "zh-hant": ("\u4e9e\u6258\u514b\u65af",),
        "ko": ("\uc544\ud2b8\ub85d\uc2a4",),
    }
    expected_terms = {
        "zh-hans": (
            "\u6697\u88d4\u5229\u5203",
            "\u6076\u706b\u675f\u94fe",
            "\u5927\u706d",
        ),
        "zh-hant": (
            "\u51a5\u8840\u90aa\u528d",
            "\u60e1\u706b\u675f\u93c8",
            "World Ender",
        ),
    }
    for locale, expected_name_terms in expected_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for aatrox_id in AATROX_IDS:
            row = descriptions.get(aatrox_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {aatrox_id}")
            name = str(row.get("name", ""))
            for expected_name_term in expected_name_terms:
                if expected_name_term not in name:
                    fail(
                        f"text/champion.i18n locale {locale} {aatrox_id}.name "
                        f"must include {expected_name_term!r} for localized display"
                    )
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "�" in value:
                    fail(f"text/champion.i18n locale {locale} {aatrox_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {aatrox_id} missing term {term!r}")

    for aatrox_id in AATROX_IDS:
        view = entries.get(aatrox_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{aatrox_id}")
        face_x = view.get("face", {}).get("x")
        face_y = view.get("face", {}).get("y")
        center_y = view.get("center", {}).get("y")
        if face_x != 0 or face_y != -24:
            fail(f"style entry {aatrox_id}.face must keep Aatrox's compact portrait at x=0,y=-24")
        if center_y != -12:
            fail(f"style entry {aatrox_id}.center.y must keep Aatrox full-body display at -12")

    for path in (
        ROOT / "aseprite_resources" / "champions" / "aatrox#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_attack_slash#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_q1_cleave#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_q2_cleave#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_q3_cleave#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_w_chain#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_w_chain_snap#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "aatrox_world_ender_aura#sheet.png",
    ):
        require_file(path)
        require_no_green_residue(path)
        if path.parent.name == "effects":
            require_no_aatrox_green_spill(path)

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "aatrox#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "aatrox#sheet.png"
    )
    allowed_pixels: set[tuple[int, int]] = set()
    for allowed_x in AATROX_ALLOWED_FRAME_XS:
        for local_y in range(54):
            for local_x in range(57):
                allowed_pixels.add((allowed_x + local_x, local_y))
    for y in range(sheet_height):
        row_start = y * sheet_width
        for x in range(sheet_width):
            if sheet_alpha[row_start + x] and (x, y) not in allowed_pixels:
                fail(
                    f"Aatrox sheet has non-transparent pixels outside final approved frame slots at ({x},{y}); "
                    "old/generated candidate models must be cleared"
                )
    for x in AATROX_RETIRED_MODEL_FRAME_XS:
        bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, 0, 57, 54))
        if bbox is not None:
            fail(f"Aatrox retired old-model frame slot at x={x} must stay blank")
    idle_frames = fanim.get("anims", {}).get("idle", {}).get("frames")
    if not isinstance(idle_frames, list) or len(idle_frames) < 6:
        fail("Aatrox idle animation must have at least six stable display frames")
    run_frames = fanim.get("anims", {}).get("run", {}).get("frames")
    if not isinstance(run_frames, list) or len(run_frames) != 8:
        fail("Aatrox run must preserve its native eight-frame contract")

    expected_frame_xs = {
        "idle": AATROX_IDLE_FRAME_XS,
        "run": AATROX_RUN_FRAME_XS,
        "attack": AATROX_ATTACK_FRAME_XS,
        "skill": AATROX_SKILL_FRAME_XS,
        "skill2": AATROX_SKILL2_FRAME_XS,
        "hit": (AATROX_HIT_FRAME_X,),
        "dead": (AATROX_DEAD_FRAME_X,),
        "ult": (AATROX_ULT_FRAME_X,),
    }
    action_bboxes: dict[str, list[tuple[int, int, int, int]]] = {}
    action_hashes: dict[str, list[str]] = {}
    for action in AATROX_CORE_ACTIONS:
        frames = fanim.get("anims", {}).get(action, {}).get("frames")
        if not isinstance(frames, list) or not frames:
            fail(f"Aatrox {action} animation missing frames")
        expected_xs = expected_frame_xs.get(action)
        if expected_xs is not None:
            actual_xs = tuple(int(round(float(frame.get("data", {}).get("x", -1)))) for frame in frames)
            if actual_xs != expected_xs:
                fail(f"Aatrox {action} must use its own accepted action/portrait frame slots, got {actual_xs}")
        action_bboxes[action] = []
        action_hashes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Aatrox {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != AATROX_VIKTOR_FRAME_SIZE:
                fail(
                    f"Aatrox {action} frame {index} must use the Viktor-like "
                    f"{AATROX_VIKTOR_FRAME_SIZE[0]:.0f}x{AATROX_VIKTOR_FRAME_SIZE[1]:.0f} actor frame"
                )
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            if x < 0 or y < 0 or x + w > sheet_width or y + h > sheet_height:
                fail(f"Aatrox {action} frame {index} points outside aatrox#sheet.png")
            if x in AATROX_RETIRED_MODEL_FRAME_XS:
                fail(f"Aatrox {action} frame {index} must not reference retired old-model slot x={x}")
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Aatrox {action} frame {index} is blank")
            action_bboxes[action].append(bbox)
            action_hashes[action].append(alpha_frame_hash(sheet_alpha, sheet_width, (x, y, w, h)))
            body_height = bbox[3] - bbox[1]
            bottom_safe = h - bbox[3]
            if action in ("attack", "skill", "skill2", "dead"):
                max_body_height = AATROX_MAX_ACTION_BODY_HEIGHT
                min_bottom_safe = AATROX_MIN_ACTION_BOTTOM_SAFE_PIXELS
            else:
                max_body_height = AATROX_MAX_DISPLAY_BODY_HEIGHT
                min_bottom_safe = AATROX_MIN_DISPLAY_BOTTOM_SAFE_PIXELS
            if body_height > max_body_height:
                fail(
                    f"Aatrox {action} frame {index} body height {body_height}px exceeds "
                    f"{max_body_height}px, causing model-size jumps"
                )
            if bottom_safe < min_bottom_safe:
                fail(
                    f"Aatrox {action} frame {index} leaves only {bottom_safe}px bottom safety; "
                    "feet must stay above the name/health label like Viktor"
                )
            if action == "run" and frame.get("duration") != 0.065:
                fail(f"Aatrox run frame {index} must keep Viktor-like 0.065s timing")

    run_widths = [bbox[2] - bbox[0] for bbox in action_bboxes["run"]]
    run_heights = [bbox[3] - bbox[1] for bbox in action_bboxes["run"]]
    if max(run_widths) - min(run_widths) > 6:
        fail("Aatrox run frame widths must stay stable to avoid animation jitter")
    for action in ("attack", "skill", "skill2"):
        widths = [bbox[2] - bbox[0] for bbox in action_bboxes[action]]
        if max(widths) < min(run_widths):
            fail(f"Aatrox {action} must include readable weapon/body motion from the final model source")
        if len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Aatrox {action} must have visible body/weapon motion, not repeated static frames")
        if tuple(action_hashes[action][: len(action_hashes["run"])]) == tuple(action_hashes["run"][: len(action_hashes[action])]):
            fail(f"Aatrox {action} must not be a direct copy of the run cycle")
    for action in ("idle", "hit", "ult"):
        heights = [bbox[3] - bbox[1] for bbox in action_bboxes[action]]
        if max(abs(height - run_heights[0]) for height in heights) > 2:
            fail(f"Aatrox {action} model height must stay in the same scale class as run")

    foot_centers: list[float] = []
    foot_shapes: set[tuple[tuple[int, int], ...]] = set()
    for index, frame in enumerate(run_frames):
        data = frame["data"]
        x = int(round(float(data["x"])))
        y = int(round(float(data["y"])))
        w = int(round(float(data["w"])))
        local_points: list[tuple[int, int]] = []
        lower_points: list[tuple[int, int]] = []
        for local_y in range(30, 38):
            row_start = (y + local_y) * sheet_width
            for local_x in range(18, min(45, w)):
                if sheet_alpha[row_start + x + local_x] != 0:
                    lower_points.append((local_x, local_y))
        for local_y in range(31, 38):
            row_start = (y + local_y) * sheet_width
            for local_x in range(20, min(42, w)):
                if sheet_alpha[row_start + x + local_x] != 0:
                    local_points.append((local_x, local_y))
        if not local_points:
            fail(f"Aatrox run frame {index} has no readable foot pixels")
        if len(local_points) < AATROX_MIN_RUN_FOOT_PIXELS:
            fail(
                f"Aatrox run frame {index} has only {len(local_points)} foot pixels; "
                "do not replace the model with thin drawn legs"
            )
        if len(lower_points) < AATROX_MIN_RUN_LOWER_PIXELS:
            fail(
                f"Aatrox run frame {index} has only {len(lower_points)} lower-body pixels; "
                "the run cycle must keep the accepted compact model density"
            )
        foot_centers.append(sum(point[0] for point in local_points) / len(local_points))
        foot_shapes.add(tuple(local_points))
    if max(foot_centers) - min(foot_centers) < AATROX_MIN_RUN_FOOT_CENTER_RANGE:
        fail("Aatrox run must have Viktor-like alternating foot motion, not a zombie shuffle")
    if len(foot_shapes) < AATROX_MIN_RUN_FOOT_SHAPES:
        fail("Aatrox run must vary foot shapes across the eight-frame cycle")

    aatrox = load_json(ROOT / "champion" / "aatrox.data_champion")
    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in aatrox.get("view_projectiles", [])}
    for name, expected in AATROX_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/aatrox.data_champion projectile {name} must reference {expected}")
    projectile_z = {item.get("name"): item.get("z") for item in aatrox.get("view_projectiles", [])}
    for name in ("test_mod_aatrox_q1", "test_mod_aatrox_q2", "test_mod_aatrox_q3"):
        if projectile_z.get(name) != 1:
            fail(f"champion/aatrox.data_champion projectile {name} must render visibly above terrain at z=1")
    view_effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in aatrox.get("view_effects", [])}
    for name, expected in AATROX_ATTACK_CAST_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/aatrox.data_champion attack view_effect {name} must reference {expected}")
    attack_strings = set(walk_strings(aatrox.get("attack", {})))
    for name in AATROX_ATTACK_CAST_EFFECT_REFS:
        if name not in attack_strings:
            fail(f"champion/aatrox.data_champion attack.effect must trigger {name} for the basic attack slash VFX")
    for name, expected in AATROX_Q_CAST_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/aatrox.data_champion view_effect {name} must reference {expected}")
    skill_effect = aatrox.get("skill", {}).get("effect")
    if not isinstance(skill_effect, dict) or skill_effect.get("type") != "SwitchByBuff":
        fail("Aatrox Q must use staged SwitchByBuff recasts instead of firing all three Qs at once")
    if skill_effect.get("buff_name") != "test_mod_aatrox_q3_ready":
        fail("Aatrox Q top-level stage must branch on test_mod_aatrox_q3_ready")
    q2_switch = skill_effect.get("effect_none")
    if not isinstance(q2_switch, dict) or q2_switch.get("type") != "SwitchByBuff":
        fail("Aatrox Q must branch Q1/Q2 through test_mod_aatrox_q2_ready")
    if q2_switch.get("buff_name") != "test_mod_aatrox_q2_ready":
        fail("Aatrox Q second stage must branch on test_mod_aatrox_q2_ready")

    def assert_q_stage(branch: object, label: str, expected_projectile: str, expected_vfx: str) -> None:
        if not isinstance(branch, dict) or branch.get("type") != "Combine":
            fail(f"Aatrox {label} must be a single Combine branch")
        branch_strings = set(walk_strings(branch))
        if "Delayed" in branch_strings:
            fail(f"Aatrox {label} must not contain Delayed chained Q segments")
        for projectile in ("test_mod_aatrox_q1", "test_mod_aatrox_q2", "test_mod_aatrox_q3"):
            if (projectile == expected_projectile) != (projectile in branch_strings):
                fail(f"Aatrox {label} must contain only {expected_projectile}, got projectile refs {sorted(branch_strings & {'test_mod_aatrox_q1', 'test_mod_aatrox_q2', 'test_mod_aatrox_q3'})}")
        for vfx in ("test_mod_aatrox_q1_cast_vfx", "test_mod_aatrox_q2_cast_vfx", "test_mod_aatrox_q3_cast_vfx"):
            if (vfx == expected_vfx) != (vfx in branch_strings):
                fail(f"Aatrox {label} must contain only {expected_vfx}, got cast VFX refs {sorted(branch_strings & {'test_mod_aatrox_q1_cast_vfx', 'test_mod_aatrox_q2_cast_vfx', 'test_mod_aatrox_q3_cast_vfx'})}")
        if label == "Q1" and "test_mod_aatrox_q2_ready" not in branch_strings:
            fail("Aatrox Q1 must arm the Q2 recast window")
        if label == "Q2" and "test_mod_aatrox_q3_ready" not in branch_strings:
            fail("Aatrox Q2 must arm the Q3 recast window")
        if label == "Q3" and ("test_mod_aatrox_q2_ready" not in branch_strings or "test_mod_aatrox_q3_ready" not in branch_strings):
            fail("Aatrox Q3 must clear staged Q recast buffs")

    assert_q_stage(q2_switch.get("effect_none"), "Q1", "test_mod_aatrox_q1", "test_mod_aatrox_q1_cast_vfx")
    assert_q_stage(q2_switch.get("effect_buff"), "Q2", "test_mod_aatrox_q2", "test_mod_aatrox_q2_cast_vfx")
    assert_q_stage(skill_effect.get("effect_buff"), "Q3", "test_mod_aatrox_q3", "test_mod_aatrox_q3_cast_vfx")
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in aatrox.get("view_buffs", [])}
    for name, expected in AATROX_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/aatrox.data_champion buff {name} must reference {expected}")
    world_ender = next((item for item in aatrox.get("view_buffs", []) if item.get("name") == "test_mod_aatrox_world_ender"), None)
    if not isinstance(world_ender, dict) or world_ender.get("z") != -1:
        fail("Aatrox World Ender aura must render behind the actor instead of covering the battlefield")

    aura_fanim = load_json(ROOT / "aseprite_resources" / "effects" / "aatrox_world_ender_aura#anim.fanim")
    aura_frames = aura_fanim.get("anims", {}).get("loop", {}).get("frames")
    if not isinstance(aura_frames, list) or len(aura_frames) != 6:
        fail("Aatrox World Ender aura must have six restrained loop frames")
    for index, frame in enumerate(aura_frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict) or data.get("w") != 64.0 or data.get("h") != 64.0:
            fail(f"Aatrox World Ender aura frame {index} must stay within 64x64")

    assert_official_audio_sources(
        "aatrox",
        "Aatrox.wad.client",
        "aatrox_base_sfx_audio.bnk",
        AATROX_SOUND_MEDIA_IDS,
        {
            "test_mod_aatrox_cleave_cast",
            "test_mod_aatrox_cleave_hit",
            "test_mod_aatrox_dash_cast",
            "test_mod_aatrox_ult_cast",
            "test_mod_aatrox_ult_voice",
        },
        AATROX_SKILL_SOUND_VOLUME_FLOOR,
    )
    if "test_mod_aatrox_ult_voice" not in set(walk_strings(aatrox.get("ult", {}))):
        fail("Aatrox ult must play fixed official VO through test_mod_aatrox_ult_voice")
    overrides = load_json(ROOT / "mod.override_info")
    for clip_name in ("test_mod_aatrox_dash_voice_clip", "test_mod_aatrox_dash_effect_clip"):
        key = f"asset/base/sound/sfx/{clip_name}"
        expected_remap = f"asset/bo_league_champions/sound/sfx/{clip_name}"
        override = overrides.get(key)
        if not isinstance(override, dict) or override.get("remapping") != expected_remap or override.get("type") != "override":
            fail(f"mod.override_info must override {key} to {expected_remap}")


def check_kayn_rework_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_display_names = {
        "en": "Kayn (Shadow Reaper)",
        "zh-hans": "\u5f71\u6d41\u4e4b\u9570",
        "zh-hant": "\u5f71\u6d41\u4e4b\u942e",
    }
    expected_terms = {
        "en": ("Shadow Reaper", "Darkin Scythe", "Darkin Ascension"),
        "zh-hans": ("\u5f71\u6d41\u4e4b\u9570", "\u5de8\u9570\u6a2a\u626b", "\u5229\u5203\u7eb5\u8d2f", "\u88c2\u820d\u5f71", "\u6697\u88d4\u5347\u534e"),
        "zh-hant": ("\u5f71\u6d41\u4e4b\u942e", "\u5de8\u942e\u6a6b\u6383", "\u5229\u5203\u7e31\u8cab", "\u88c2\u820d\u5f71", "\u51a5\u8840\u5347\u83ef"),
    }
    for locale, expected_name in expected_display_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for kayn_id in KAYN_IDS:
            row = descriptions.get(kayn_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {kayn_id}")
            name = str(row.get("name", ""))
            if name != expected_name:
                fail(f"text/champion.i18n locale {locale} {kayn_id}.name must be short display name {expected_name!r}")
            if locale in {"zh-hans", "zh-hant"} and any(alias in name for alias in ("Kayn", "\u51ef\u9690", "\u6168\u5f71")):
                fail(f"text/champion.i18n locale {locale} {kayn_id}.name must not include search aliases")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "・ｽ" in value:
                    fail(f"text/champion.i18n locale {locale} {kayn_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("attack", "skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {kayn_id} missing term {term!r}")

    for kayn_id in KAYN_IDS:
        view = entries.get(kayn_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{kayn_id}")
        face_x = view.get("face", {}).get("x")
        face_y = view.get("face", {}).get("y")
        center_y = view.get("center", {}).get("y")
        if face_x != 4:
            fail(f"style entry {kayn_id}.face.x must keep Kayn's compact portrait centered")
        if face_y != -36:
            fail(f"style entry {kayn_id}.face.y must keep Kayn's compact portrait at -36")
        if not isinstance(center_y, (int, float)) or not -20 <= center_y <= -8:
            fail(f"style entry {kayn_id}.center.y must keep the full-body display above the name")

    for path in (
        ROOT / "aseprite_resources" / "champions" / "kayn#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "kayn_q_slash#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "kayn_w_blade_reach#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "kayn_r_entry#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "kayn_r_exit#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "kayn_darkin_aura#sheet.png",
        ROOT / "icons" / "kayn_skill.png",
        ROOT / "icons" / "kayn_skill2.png",
        ROOT / "icons" / "kayn_ult.png",
    ):
        require_file(path)
        require_no_green_residue(path)

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "kayn#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "kayn#sheet.png"
    )
    expected_counts = {
        "idle": 6,
        "run": 10,
        "attack": 6,
        "skill": 6,
        "skill2": 7,
        "ult": 7,
        "hit": 1,
        "dead": 1,
    }
    action_bboxes: dict[str, list[tuple[int, int, int, int]]] = {}
    for action in KAYN_CORE_ACTIONS:
        frames = fanim.get("anims", {}).get(action, {}).get("frames")
        if not isinstance(frames, list) or len(frames) != expected_counts[action]:
            fail(f"Kayn {action} animation must have {expected_counts[action]} frames")
        action_bboxes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Kayn {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != KAYN_FRAME_SIZE:
                fail(f"Kayn {action} frame {index} must use the {KAYN_FRAME_SIZE[0]:.0f}x{KAYN_FRAME_SIZE[1]:.0f} actor frame")
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            if x < 0 or y < 0 or x + w > sheet_width or y + h > sheet_height:
                fail(f"Kayn {action} frame {index} points outside kayn#sheet.png")
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Kayn {action} frame {index} is blank")
            action_bboxes[action].append(bbox)
            body_height = bbox[3] - bbox[1]
            bottom_safe = h - bbox[3]
            if body_height > 42:
                fail(f"Kayn {action} frame {index} body height {body_height}px is too large for the in-game label")
            if bottom_safe < 10:
                fail(f"Kayn {action} frame {index} leaves only {bottom_safe}px bottom safety above name/health labels")
            if action == "run" and frame.get("duration") != 0.065:
                fail(f"Kayn run frame {index} must keep Viktor-like 0.065s timing")

    run_frames = fanim.get("anims", {}).get("run", {}).get("frames")
    foot_centers: list[float] = []
    foot_shapes: set[tuple[tuple[int, int], ...]] = set()
    for index, frame in enumerate(run_frames):
        data = frame["data"]
        x = int(round(float(data["x"])))
        y = int(round(float(data["y"])))
        w = int(round(float(data["w"])))
        h = int(round(float(data["h"])))
        bbox = action_bboxes["run"][index]
        lower_points: list[tuple[int, int]] = []
        for local_y in range(max(bbox[1], 30), bbox[3]):
            row_start = (y + local_y) * sheet_width
            for local_x in range(bbox[0], bbox[2]):
                if 0 <= local_x < w and 0 <= local_y < h and sheet_alpha[row_start + x + local_x] != 0:
                    lower_points.append((local_x, local_y))
        if len(lower_points) < 120:
            fail(f"Kayn run frame {index} has only {len(lower_points)} lower-body pixels; keep a solid generated model")
        foot_centers.append(sum(point[0] for point in lower_points) / len(lower_points))
        foot_shapes.add(tuple(lower_points))
    if max(foot_centers) - min(foot_centers) < 1.5:
        fail("Kayn run must have alternating foot motion, not a sliding or zombie step")
    if len(foot_shapes) < 5:
        fail("Kayn run must vary lower-body shapes across the run cycle")

    kayn = load_json(ROOT / "champion" / "kayn.data_champion")
    strings = set(walk_strings(kayn))
    for required in (
        "SwitchByBuff",
        "test_mod_kayn_darkin_ascension",
        "RushTime",
        "LineRangeProjectile",
        "Invisible",
        "RushMoveToBack",
        "Airborne",
    ):
        if required not in strings:
            fail(f"champion/kayn.data_champion must include LoL Kayn mechanic token {required}")
    for action, sfx_name in (
        ("skill", "test_mod_kayn_q_cast"),
        ("skill2", "test_mod_kayn_w_cast"),
        ("ult", "test_mod_kayn_r_cast"),
    ):
        effect = kayn.get(action, {}).get("effect")
        effects = effect.get("effects") if isinstance(effect, dict) else None
        if (
            not isinstance(effect, dict)
            or effect.get("type") != "Combine"
            or not isinstance(effects, list)
            or len(effects) < 2
            or effects[0] != {"type": "Sfx", "name": sfx_name}
        ):
            fail(f"Kayn {action} must play {sfx_name} as the first top-level cast effect")
        if action in {"skill", "skill2"} and (not isinstance(effects[1], dict) or effects[1].get("type") != "SwitchByBuff"):
            fail(f"Kayn {action} must keep its form branch logic after the top-level cast SFX")
    if "test_mod_kayn_ult_voice" not in set(walk_strings(kayn.get("ult", {}))):
        fail("Kayn ult must play fixed official VO through test_mod_kayn_ult_voice")
    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in kayn.get("view_projectiles", [])}
    for name, expected in KAYN_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/kayn.data_champion projectile {name} must reference {expected}")
    effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in kayn.get("view_effects", [])}
    for name, expected in KAYN_VIEW_EFFECT_REFS.items():
        if effect_refs.get(name) != expected:
            fail(f"champion/kayn.data_champion view_effect {name} must reference {expected}")
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in kayn.get("view_buffs", [])}
    for name, expected in KAYN_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/kayn.data_champion buff {name} must reference {expected}")
    darkin = next((item for item in kayn.get("view_buffs", []) if item.get("name") == "test_mod_kayn_darkin_ascension"), None)
    if not isinstance(darkin, dict) or darkin.get("z") != -1:
        fail("Kayn Darkin Ascension aura must render behind the actor")

    official = load_json(ROOT / "qa" / "kayn_official_audio_sources.json")
    if not isinstance(official, dict):
        fail("qa/kayn_official_audio_sources.json must contain a JSON object")
    if "Kayn.wad.client" not in str(official.get("source", "")):
        fail("Kayn audio source must document the official Kayn.wad.client")
    if "kayn_base_sfx_audio.bnk" not in str(official.get("bank", "")):
        fail("Kayn audio source must document the official Kayn base SFX bank")
    events = official.get("events")
    if not isinstance(events, dict):
        fail("qa/kayn_official_audio_sources.json missing events object")
    overrides = load_json(ROOT / "mod.override_info")
    for event_name, media_id in KAYN_SOUND_MEDIA_IDS.items():
        row = events.get(event_name)
        if not isinstance(row, dict) or str(row.get("media_id")) != media_id:
            fail(f"official Kayn audio event {event_name} must document media_id {media_id}")
        sound_info = require_wave_asset(event_name)
        plays = sound_info.get("plays")
        volume = plays[0].get("volume") if isinstance(plays, list) and plays and isinstance(plays[0], dict) else None
        if event_name in KAYN_SKILL_SOUND_EVENTS:
            if not isinstance(volume, (int, float)) or volume < KAYN_SKILL_SOUND_VOLUME_FLOOR:
                fail(f"{event_name}.sound_info volume must be at least {KAYN_SKILL_SOUND_VOLUME_FLOOR} for audible skill feedback")
            if abs(float(row.get("volume")) - float(volume)) > 0.001:
                fail(f"qa/kayn_official_audio_sources.json volume for {event_name} must match sound_info volume")
        for suffix in ("", "_clip"):
            key = f"asset/base/sound/sfx/{event_name}{suffix}"
            expected_remap = f"asset/bo_league_champions/sound/sfx/{event_name}{suffix}"
            override = overrides.get(key)
            if not isinstance(override, dict) or override.get("remapping") != expected_remap or override.get("type") != "override":
                fail(f"mod.override_info must override {key} to {expected_remap}")


def check_yasuo_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_display_names = {
        "en": "Yasuo (Unforgiven)",
        "zh-hans": "\u75be\u98ce\u5251\u8c6a",
        "zh-hant": "\u75be\u98a8\u528d\u8c6a",
    }
    expected_terms = {
        "en": ("Steel Tempest", "Sweeping Blade", "Wind Wall", "Last Breath"),
        "zh-hans": ("\u65a9\u94a2\u95ea", "\u8e0f\u524d\u65a9", "\u98ce\u4e4b\u969c\u58c1", "\u72c2\u98ce\u7edd\u606f\u65a9"),
        "zh-hant": ("\u65ac\u92fc\u9583", "\u98a8\u7246", "\u596a\u547d\u6c23\u606f"),
    }
    for locale, expected_name in expected_display_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for yasuo_id in YASUO_IDS:
            row = descriptions.get(yasuo_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {yasuo_id}")
            name = str(row.get("name", ""))
            if name != expected_name:
                fail(f"text/champion.i18n locale {locale} {yasuo_id}.name must be short display name {expected_name!r}")
            if locale in {"zh-hans", "zh-hant"} and any(alias in name for alias in ("Yasuo", "\u4e9a\u7d22", "\u72bd\u5bbf")):
                fail(f"text/champion.i18n locale {locale} {yasuo_id}.name must not include search aliases")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "繝ｻ・ｽ" in value:
                    fail(f"text/champion.i18n locale {locale} {yasuo_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("attack", "skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {yasuo_id} missing term {term!r}")

    for yasuo_id in YASUO_IDS:
        view = entries.get(yasuo_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{yasuo_id}")
        if view.get("face", {}).get("x") != 4 or view.get("face", {}).get("y") != -26:
            fail(f"style entry {yasuo_id}.face must keep Yasuo compact portrait aligned at x=4,y=-26")
        if view.get("center", {}).get("y") != -12:
            fail(f"style entry {yasuo_id}.center.y must place the full model above the name")

    for path in (
        ROOT / "aseprite_resources" / "champions" / "yasuo#sheet.png",
        ROOT / "icons" / "yasuo_skill.png",
        ROOT / "icons" / "yasuo_skill2.png",
        ROOT / "icons" / "yasuo_ult.png",
    ):
        require_file(path)
        require_no_green_residue(path)
    for effect_name in (
        "yasuo_attack_slash",
        "yasuo_q_stab",
        "yasuo_q_tornado",
        "yasuo_sweeping_blade",
        "yasuo_wind_wall",
        "yasuo_last_breath",
        "yasuo_flow_shield",
        "yasuo_after_breath_aura",
    ):
        sheet = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#sheet.png"
        fanim = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#anim.fanim"
        require_file(sheet)
        require_file(fanim)
        require_no_green_residue(sheet)
        width, height, rgba = load_rgba(sheet)
        wind_pixels = 0
        off_palette_pixels = 0
        for i in range(width * height):
            r = rgba[i * 4]
            g = rgba[i * 4 + 1]
            b = rgba[i * 4 + 2]
            a = rgba[i * 4 + 3]
            if not a:
                continue
            wind_pixels += 1
            if not (b >= r + 12 and g >= r - 8 and (b >= 90 or g >= 90)):
                off_palette_pixels += 1
        if wind_pixels < 20:
            fail(f"{sheet.relative_to(ROOT)} must contain a visible generated wind/sword effect")
        if off_palette_pixels > max(25, wind_pixels // 8):
            fail(f"{sheet.relative_to(ROOT)} contains actor/body-colored pixels; effects must not include a duplicate champion body")

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "yasuo#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "yasuo#sheet.png"
    )
    expected_counts = {
        "idle": 6,
        "run": 10,
        "attack": 6,
        "skill": 6,
        "skill2": 7,
        "ult": 6,
        "hit": 1,
        "dead": 1,
    }
    action_hashes: dict[str, list[str]] = {}
    for action in YASUO_CORE_ACTIONS:
        frames = fanim.get("anims", {}).get(action, {}).get("frames")
        if not isinstance(frames, list) or len(frames) != expected_counts[action]:
            fail(f"Yasuo {action} animation must have {expected_counts[action]} frames")
        action_hashes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Yasuo {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != YASUO_FRAME_SIZE:
                fail(f"Yasuo {action} frame {index} must use the 57x54 actor frame")
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            if x < 0 or y < 0 or x + w > sheet_width or y + h > sheet_height:
                fail(f"Yasuo {action} frame {index} points outside yasuo#sheet.png")
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Yasuo {action} frame {index} is blank")
            body_height = bbox[3] - bbox[1]
            bottom_safe = h - bbox[3]
            if body_height > 45:
                fail(f"Yasuo {action} frame {index} body height {body_height}px is too large for UI/battle labels")
            if bottom_safe < 6:
                fail(f"Yasuo {action} frame {index} leaves only {bottom_safe}px bottom safety above labels")
            if action == "run" and frame.get("duration") != 0.085:
                fail(f"Yasuo run frame {index} must keep the slower 0.085s timing")
            action_hashes[action].append(alpha_frame_hash(sheet_alpha, sheet_width, (x, y, w, h)))
        if action in {"attack", "skill", "skill2", "ult"} and len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Yasuo {action} must have real action motion, not repeated idle frames")
    if tuple(action_hashes["attack"][: len(action_hashes["idle"])]) == tuple(action_hashes["idle"]):
        fail("Yasuo attack must not be a direct copy of idle")

    yasuo = load_json(ROOT / "champion" / "yasuo.data_champion")
    strings = set(walk_strings(yasuo))
    for required in (
        "test_mod_yasuo_q_stack_1",
        "test_mod_yasuo_q_stack_2",
        "test_mod_yasuo_last_breath_ready",
        "test_mod_yasuo_flow_shield_visual",
        "RushTime",
        "BlockMoveSkill",
        "Knockback",
        "LinearProjectile",
        "RushMoveToBack",
        "Airborne",
    ):
        if required not in strings:
            fail(f"champion/yasuo.data_champion must include LoL Yasuo mechanic token {required}")
    skill_effect = yasuo.get("skill", {}).get("effect")
    if not isinstance(skill_effect, dict) or skill_effect.get("type") != "SwitchByBuff":
        fail("Yasuo Q must use staged SwitchByBuff recasts")
    if skill_effect.get("buff_name") != "test_mod_yasuo_q_stack_2":
        fail("Yasuo Q top-level stage must branch on test_mod_yasuo_q_stack_2")
    q1_q2_switch = skill_effect.get("effect_none")
    if not isinstance(q1_q2_switch, dict) or q1_q2_switch.get("buff_name") != "test_mod_yasuo_q_stack_1":
        fail("Yasuo Q must branch Q1/Q2 through test_mod_yasuo_q_stack_1")

    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in yasuo.get("view_projectiles", [])}
    for name, expected in YASUO_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/yasuo.data_champion projectile {name} must reference {expected}")
    view_effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in yasuo.get("view_effects", [])}
    for name, expected in YASUO_VIEW_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/yasuo.data_champion view_effect {name} must reference {expected}")
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in yasuo.get("view_buffs", [])}
    for name, expected in YASUO_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/yasuo.data_champion buff {name} must reference {expected}")

    for action, sfx_name in (
        ("skill", "test_mod_yasuo_q_cast"),
        ("skill2", "test_mod_yasuo_dash_cast"),
        ("ult", "test_mod_yasuo_r_cast"),
    ):
        if sfx_name not in set(walk_strings(yasuo.get(action, {}))):
            fail(f"Yasuo {action} must trigger {sfx_name}")
    if "test_mod_yasuo_ult_voice" not in set(walk_strings(yasuo.get("ult", {}))):
        fail("Yasuo ult must play fixed official VO through test_mod_yasuo_ult_voice")

    assert_official_audio_sources(
        "yasuo",
        "Yasuo.wad.client",
        "yasuo_base_sfx_audio.bnk",
        YASUO_SOUND_MEDIA_IDS,
        YASUO_SKILL_SOUND_EVENTS,
        YASUO_SKILL_SOUND_VOLUME_FLOOR,
    )


def check_jinx_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_display_names = {
        "en": "Jinx (Loose Cannon)",
        "zh-hans": "\u66b4\u8d70\u841d\u8389",
        "zh-hant": "\u66b4\u8d70\u863f\u8389",
        "ko": "\uc9d5\ud06c\uc2a4",
    }
    expected_terms = {
        "en": ("Pow-Pow", "Fishbones", "Switcheroo", "Zap", "Flame Chompers", "Super Mega Death Rocket"),
        "zh-hans": ("\u7830\u7830\u67aa", "\u9c7c\u9aa8\u5934", "\u67aa\u70ae\u4ea4\u54cd\u66f2", "\u9707\u8361\u7535\u78c1\u6ce2", "\u56bc\u706b\u8005", "\u8d85\u7a76\u6781\u6b7b\u795e\u98de\u5f39"),
        "zh-hant": ("\u7830\u7830\u69cd", "\u9b5a\u9aa8\u982d", "\u69cd\u70ae\u4ea4\u97ff\u66f2", "\u9707\u76ea\u96fb\u78c1\u6ce2", "\u56bc\u706b\u8005", "\u8d85\u7a76\u6975\u6b7b\u795e\u98db\u5f48"),
    }
    for locale, expected_name in expected_display_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for jinx_id in JINX_IDS:
            row = descriptions.get(jinx_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {jinx_id}")
            name = str(row.get("name", ""))
            if name != expected_name:
                fail(f"text/champion.i18n locale {locale} {jinx_id}.name must be short display name {expected_name!r}")
            if locale in {"zh-hans", "zh-hant"} and any(alias in name for alias in ("Jinx", "\u91d1\u514b\u4e1d", "\u91d1\u514b\u7d72")):
                fail(f"text/champion.i18n locale {locale} {jinx_id}.name must not include search aliases")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "\ufffd" in value or "\u7e5d" in value:
                    fail(f"text/champion.i18n locale {locale} {jinx_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("attack", "skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {jinx_id} missing term {term!r}")

    for jinx_id in JINX_IDS:
        view = entries.get(jinx_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{jinx_id}")
        if view.get("face", {}).get("x") != -2 or view.get("face", {}).get("y") != -37:
            fail(f"style entry {jinx_id}.face must keep Jinx compact portrait aligned at x=-2,y=-37")
        if view.get("center", {}).get("y") != -16:
            fail(f"style entry {jinx_id}.center.y must keep the full model above the name at y=-16")

    for path in (
        ROOT / "aseprite_resources" / "champions" / "jinx#sheet.png",
        ROOT / "icons" / "jinx_skill.png",
        ROOT / "icons" / "jinx_skill2.png",
        ROOT / "icons" / "jinx_ult.png",
    ):
        require_file(path)
        require_no_green_residue(path)
    for effect_name in (
        "jinx_minigun_bullet",
        "jinx_rocket_attack",
        "jinx_zap",
        "jinx_flame_chompers",
        "jinx_super_mega_death_rocket",
        "jinx_switcheroo",
        "jinx_rocket_explosion",
        "jinx_get_excited_aura",
        "jinx_fishbones_mode_aura",
    ):
        sheet = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#sheet.png"
        fanim = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#anim.fanim"
        require_file(sheet)
        require_file(fanim)
        require_no_green_residue(sheet)
        width, height, rgba = load_rgba(sheet)
        visible_pixels = 0
        actor_skin_pixels = 0
        for i in range(width * height):
            r = rgba[i * 4]
            g = rgba[i * 4 + 1]
            b = rgba[i * 4 + 2]
            a = rgba[i * 4 + 3]
            if not a:
                continue
            visible_pixels += 1
            if r > 170 and 95 < g < 195 and 55 < b < 155 and r > b + 25 and abs(r - g) < 95:
                actor_skin_pixels += 1
        if visible_pixels < 20:
            fail(f"{sheet.relative_to(ROOT)} must contain a visible generated Jinx effect")
        if actor_skin_pixels > max(40, visible_pixels // 5):
            fail(f"{sheet.relative_to(ROOT)} contains too many actor/body-colored pixels; effects must stay separate from the champion body")
    assert_jinx_fishbones_held_overlay()

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "jinx#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "jinx#sheet.png"
    )
    expected_counts = {
        "idle": 8,
        "run": 10,
        "attack": 7,
        "skill": 6,
        "skill2": 7,
        "ult": 6,
        "hit": 1,
        "dead": 1,
    }
    action_hashes: dict[str, list[str]] = {}
    action_bboxes: dict[str, list[tuple[int, int, int, int]]] = {}
    for action in JINX_CORE_ACTIONS:
        frames = fanim.get("anims", {}).get(action, {}).get("frames")
        if not isinstance(frames, list) or len(frames) != expected_counts[action]:
            fail(f"Jinx {action} animation must have {expected_counts[action]} frames")
        action_hashes[action] = []
        action_bboxes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Jinx {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != JINX_FRAME_SIZE:
                fail(f"Jinx {action} frame {index} must use the 57x54 actor frame")
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            if x < 0 or y < 0 or x + w > sheet_width or y + h > sheet_height:
                fail(f"Jinx {action} frame {index} points outside jinx#sheet.png")
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Jinx {action} frame {index} is blank")
            action_bboxes[action].append(bbox)
            action_hashes[action].append(alpha_frame_hash(sheet_alpha, sheet_width, (x, y, w, h)))
            body_height = bbox[3] - bbox[1]
            bottom_safe = h - bbox[3]
            if action != "dead" and body_height > 45:
                fail(f"Jinx {action} frame {index} body height {body_height}px is too large for UI/battle labels")
            if action != "dead" and bottom_safe < 9:
                fail(f"Jinx {action} frame {index} leaves only {bottom_safe}px bottom safety above labels")
            if action == "run" and frame.get("duration") != 0.115:
                fail("Jinx run must use the slower 0.115s crossed-walk timing, not a sprint")
        if action in {"attack", "skill", "skill2", "ult"} and len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Jinx {action} must have real action motion, not repeated idle frames")

    for action in ("attack", "skill", "skill2", "ult", "hit"):
        if tuple(action_hashes[action][: len(action_hashes["idle"])]) == tuple(action_hashes["idle"][: len(action_hashes[action])]):
            fail(f"Jinx {action} must not be a direct copy of idle")

    run_frames = fanim.get("anims", {}).get("run", {}).get("frames")
    assert isinstance(run_frames, list)
    foot_centers: list[float] = []
    lower_shapes: set[tuple[tuple[int, int], ...]] = set()
    for index, frame in enumerate(run_frames):
        data = frame["data"]
        x = int(round(float(data["x"])))
        y = int(round(float(data["y"])))
        w = int(round(float(data["w"])))
        h = int(round(float(data["h"])))
        bbox = action_bboxes["run"][index]
        lower_points: list[tuple[int, int]] = []
        for local_y in range(max(26, bbox[1] + (bbox[3] - bbox[1]) // 2), min(h, bbox[3])):
            row_start = (y + local_y) * sheet_width
            for local_x in range(bbox[0], bbox[2]):
                if 0 <= local_x < w and sheet_alpha[row_start + x + local_x] != 0:
                    lower_points.append((local_x, local_y))
        if len(lower_points) < 65:
            fail(f"Jinx run frame {index} has only {len(lower_points)} lower-body pixels; keep the full generated legs visible")
        foot_centers.append(sum(point[0] for point in lower_points) / len(lower_points))
        lower_shapes.add(tuple(lower_points))
    if max(foot_centers) - min(foot_centers) < 1.25:
        fail("Jinx run must have crossed walking foot motion, not a sliding/zombie step")
    if len(lower_shapes) < 6:
        fail("Jinx run must vary lower-body shapes across the ten-frame walk cycle")

    jinx = load_json(ROOT / "champion" / "jinx.data_champion")
    strings = set(walk_strings(jinx))
    for required in (
        "SwitchByBuff",
        "TargetSplashProjectile",
        "LineRangeProjectile",
        "LinearProjectile",
        "test_mod_jinx_fishbones_mode",
        "test_mod_jinx_powpow_1",
        "test_mod_jinx_powpow_2",
        "test_mod_jinx_powpow_3",
        "test_mod_jinx_flame_chompers",
        "test_mod_jinx_get_excited",
        "test_mod_jinx_ult_voice",
    ):
        if required not in strings:
            fail(f"champion/jinx.data_champion must include LoL Jinx mechanic token {required}")
    if "test_mod_jinx_powpow_visual" in strings or "jinx_powpow_ready" in strings:
        fail("Jinx must not attach Pow-Pow/Fishbones weapon loops to the actor body; use projectiles or the held Fishbones overlay only")
    skill = jinx.get("skill", {})
    if not isinstance(skill, dict):
        fail("Jinx skill must be a JSON object")
    if skill.get("casting_type") != "Targeting" or skill.get("casting_target") != "Enemy":
        fail("Jinx Switcheroo must be AI-targeted at an enemy, not a no-target manual toggle")
    if int(skill.get("range", 0)) < int(jinx.get("attack", {}).get("range", 0)):
        fail("Jinx Switcheroo target range must cover her basic attack range")
    skill_strings = set(walk_strings(skill))
    if "SwitchByBuff" in skill_strings:
        fail("Jinx Switcheroo skill must be a short AI-targeted Fishbones window, not a permanent toggle")
    if "test_mod_jinx_fishbones_mode" not in skill_strings or "test_mod_jinx_switch_to_minigun" not in skill_strings:
        fail("Jinx Switcheroo must add Fishbones briefly and schedule a return-to-minigun sound")

    def find_named_buff_ticks(node: Any, buff_name: str) -> list[int]:
        ticks: list[int] = []
        if isinstance(node, dict):
            state = node.get("buff_state")
            if isinstance(state, dict) and state.get("name") == buff_name:
                duration = state.get("duration", {})
                if isinstance(duration, dict):
                    time = duration.get("Time")
                    if isinstance(time, dict) and isinstance(time.get("tick"), int):
                        ticks.append(time["tick"])
            for value in node.values():
                ticks.extend(find_named_buff_ticks(value, buff_name))
        elif isinstance(node, list):
            for value in node:
                ticks.extend(find_named_buff_ticks(value, buff_name))
        return ticks

    fishbones_ticks = find_named_buff_ticks(skill, "test_mod_jinx_fishbones_mode")
    if fishbones_ticks != [210]:
        fail(f"Jinx Switcheroo must use one 210-tick Fishbones window, got {fishbones_ticks}")
    fishbones_visual_ticks = find_named_buff_ticks(skill, "test_mod_jinx_fishbones_visual")
    if fishbones_visual_ticks != [210]:
        fail(f"Jinx Switcheroo must show one 210-tick held Fishbones overlay, got {fishbones_visual_ticks}")
    attack_visual_ticks = find_named_buff_ticks(jinx.get("attack", {}), "test_mod_jinx_fishbones_visual")
    if attack_visual_ticks:
        fail("Jinx basic attacks must not add the held Fishbones overlay directly; Switcheroo controls the form window")

    for action, sfx_names in (
        ("skill", {"test_mod_jinx_switch_to_minigun", "test_mod_jinx_switch_to_rocket"}),
        ("skill2", {"test_mod_jinx_zap_cast", "test_mod_jinx_chompers_cast"}),
        ("ult", {"test_mod_jinx_r_cast", "test_mod_jinx_ult_voice"}),
    ):
        action_strings = set(walk_strings(jinx.get(action, {})))
        missing = sfx_names - action_strings
        if missing:
            fail(f"Jinx {action} must trigger sound events {sorted(missing)}")

    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in jinx.get("view_projectiles", [])}
    for name, expected in JINX_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/jinx.data_champion projectile {name} must reference {expected}")
    effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in jinx.get("view_effects", [])}
    for name, expected in JINX_VIEW_EFFECT_REFS.items():
        if effect_refs.get(name) != expected:
            fail(f"champion/jinx.data_champion view_effect {name} must reference {expected}")
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in jinx.get("view_buffs", [])}
    for name, expected in JINX_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/jinx.data_champion buff {name} must reference {expected}")
    expected_buff_z = {
        "test_mod_jinx_get_excited": -1,
        "test_mod_jinx_fishbones_visual": 1,
    }
    for buff_name in JINX_BUFF_REFS:
        buff = next((item for item in jinx.get("view_buffs", []) if item.get("name") == buff_name), None)
        if not isinstance(buff, dict) or buff.get("z") != expected_buff_z[buff_name]:
            fail(f"Jinx buff {buff_name} must render at z={expected_buff_z[buff_name]}")

    assert_official_audio_sources(
        "jinx",
        "Jinx.wad.client",
        "jinx_base_sfx_audio.bnk",
        JINX_SOUND_MEDIA_IDS,
        JINX_SKILL_SOUND_EVENTS,
        JINX_SKILL_SOUND_VOLUME_FLOOR,
    )
    official = load_json(ROOT / "qa" / "jinx_official_audio_sources.json")
    if "Jinx.en_US.wad.client" not in str(official.get("voice_source", "")):
        fail("Jinx ult voice source must document the official Jinx.en_US.wad.client")


def check_champion_visibility() -> None:
    text = load_json(ROOT / "text" / "champion.i18n")
    style = load_json(ROOT / "style" / "champion_view.champion_view")
    entries = style.get("entries")
    if not isinstance(entries, dict):
        fail("style/champion_view.champion_view must contain an entries object")

    champion_files = sorted((ROOT / "champion").glob("*.data_champion"))
    stems = {path.stem for path in champion_files}
    if stems != EXPECTED_CHAMPIONS:
        fail(f"champion files mismatch: expected {sorted(EXPECTED_CHAMPIONS)}, got {sorted(stems)}")

    ids: set[str] = set()
    for path in champion_files:
        data = load_json(path)
        check_effect_shapes(path, data)
        check_view_effect_types(path, data)
        champion_name = path.stem
        champion_id = data.get("id")
        expected_id = f"{MOD_ID}_{champion_name}"
        if champion_id != expected_id:
            fail(f"{path.relative_to(ROOT)} id must be {expected_id}, got {champion_id!r}")
        if str(champion_id).startswith("test_mod_"):
            fail(f"{path.relative_to(ROOT)} still uses old test_mod id {champion_id!r}")
        ids.add(champion_id)

        require_aseprite_asset(data.get("sprite", ""))
        for icon in data.get("skill_icons", []):
            require_png_asset(icon)

        refs = description_refs(data)
        required_refs = {(champion_id, key) for key in REQUIRED_DESCRIPTION_KEYS if key != "name"}
        missing_refs = required_refs - refs
        if missing_refs:
            fail(f"{path.relative_to(ROOT)} missing required description refs: {sorted(missing_refs)}")
        for ref_id, _ in refs:
            if ref_id != champion_id:
                fail(f"{path.relative_to(ROOT)} references text id {ref_id}, expected {champion_id}")

        for projectile in data.get("view_projectiles", []):
            anim = projectile.get("anim")
            if anim:
                require_aseprite_asset(anim)
        for buff in data.get("view_buffs", []):
            anim = buff.get("anim")
            if anim:
                require_aseprite_asset(anim)
        for effect in data.get("view_effects", []):
            anim = effect.get("anim")
            if anim:
                require_aseprite_asset(anim)

        view = entries.get(champion_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{champion_id}")
        for camera in ("face", "center"):
            point = view.get(camera)
            if not isinstance(point, dict):
                fail(f"style entry {champion_id}.{camera} must exist")
            for axis in ("x", "y"):
                if not isinstance(point.get(axis), (int, float)):
                    fail(f"style entry {champion_id}.{camera}.{axis} must be numeric")

        for locale, locale_data in text.items():
            descriptions = locale_data.get("description") if isinstance(locale_data, dict) else None
            if not isinstance(descriptions, dict):
                fail(f"text/champion.i18n locale {locale} missing description object")
            row = descriptions.get(champion_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {champion_id}")
            missing_keys = [key for key in REQUIRED_DESCRIPTION_KEYS if not row.get(key)]
            if missing_keys:
                fail(f"text/champion.i18n locale {locale} {champion_id} missing {missing_keys}")

    if f"{MOD_ID}_aatrox" not in ids:
        fail("Aatrox encyclopedia chain is missing bo_league_champions_aatrox")
    if f"{MOD_ID}_kayn" not in ids:
        fail("Kayn encyclopedia chain is missing bo_league_champions_kayn")
    if f"{MOD_ID}_yasuo" not in ids:
        fail("Yasuo encyclopedia chain is missing bo_league_champions_yasuo")
    if f"{MOD_ID}_jinx" not in ids:
        fail("Jinx encyclopedia chain is missing bo_league_champions_jinx")
    check_encyclopedia_search_terms(text)
    check_aatrox_rework_contract(text, entries)
    check_kayn_rework_contract(text, entries)
    check_yasuo_contract(text, entries)
    check_jinx_contract(text, entries)


def main() -> int:
    try:
        check_mod_metadata()
        check_no_process_images()
        check_roster_visibility_coverage()
        check_champion_visibility()
    except AssertionError as exc:
        print(f"encyclopedia_visibility_check=fail: {exc}", file=sys.stderr)
        return 1
    print("encyclopedia_visibility_check=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
