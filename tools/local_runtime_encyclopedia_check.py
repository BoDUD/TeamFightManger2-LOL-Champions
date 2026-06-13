from __future__ import annotations

import hashlib
import json
import os
import sys
import zlib
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD_ID = "bo_league_champions"
CHAMPION_IDS = (
    f"{MOD_ID}_aatrox",
    f"{MOD_ID}_blitzcrank",
    f"{MOD_ID}_darius",
    f"{MOD_ID}_kayn",
    f"{MOD_ID}_yasuo",
    f"{MOD_ID}_jinx",
    f"{MOD_ID}_thresh",
    f"{MOD_ID}_viktor",
    f"{MOD_ID}_fiddlesticks",
)
AATROX_SOUND_EVENTS = (
    "test_mod_aatrox_attack_cast",
    "test_mod_aatrox_attack_hit",
    "test_mod_aatrox_cleave_cast",
    "test_mod_aatrox_cleave_hit",
    "test_mod_aatrox_dash_cast",
    "test_mod_aatrox_ult_cast",
    "test_mod_aatrox_ult_voice",
)
DARIUS_SOUND_EVENTS = (
    "test_mod_darius_attack_cast",
    "test_mod_darius_attack_hit",
    "test_mod_darius_hemo_apply",
    "test_mod_darius_noxian_might",
    "test_mod_darius_q_cast",
    "test_mod_darius_q_hit",
    "test_mod_darius_q_heal",
    "test_mod_darius_e_cast",
    "test_mod_darius_e_hit",
    "test_mod_darius_w_hit",
    "test_mod_darius_r_cast",
    "test_mod_darius_r_hit",
    "test_mod_darius_ult_voice",
)
KAYN_SOUND_EVENTS = (
    "test_mod_kayn_attack_cast",
    "test_mod_kayn_attack_hit",
    "test_mod_kayn_q_cast",
    "test_mod_kayn_q_hit",
    "test_mod_kayn_w_cast",
    "test_mod_kayn_w_hit",
    "test_mod_kayn_r_cast",
    "test_mod_kayn_r_hit",
    "test_mod_kayn_ult_voice",
)
YASUO_SOUND_EVENTS = (
    "test_mod_yasuo_attack_cast",
    "test_mod_yasuo_attack_hit",
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
)
JINX_SOUND_EVENTS = (
    "test_mod_jinx_minigun_cast",
    "test_mod_jinx_minigun_hit",
    "test_mod_jinx_rocket_cast",
    "test_mod_jinx_rocket_hit",
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
)
THRESH_SOUND_EVENTS = (
    "test_mod_thresh_attack_cast",
    "test_mod_thresh_attack_hit",
    "test_mod_thresh_attack_empowered_hit",
    "test_mod_thresh_q_cast",
    "test_mod_thresh_q_hit",
    "test_mod_thresh_lantern_cast",
    "test_mod_thresh_lantern_shield",
    "test_mod_thresh_e_cast",
    "test_mod_thresh_e_hit",
    "test_mod_thresh_r_cast",
    "test_mod_thresh_r_hit",
    "test_mod_thresh_soul_gain",
    "test_mod_thresh_ult_voice",
)
THRESH_BOX_MIN_TICKS = 420
THRESH_BOX_MIN_ANIM_SECONDS = 5.0
VIKTOR_SOUND_EVENTS = (
    "test_mod_viktor_attack_cast",
    "test_mod_viktor_attack_hit",
    "test_mod_viktor_siphon_cast",
    "test_mod_viktor_siphon_empower_hit",
    "test_mod_viktor_laser_cast",
    "test_mod_viktor_laser_hit",
    "test_mod_viktor_laser_aftershock_hit",
    "test_mod_viktor_gravity_field_cast",
    "test_mod_viktor_gravity_field_slow",
    "test_mod_viktor_chaos_storm_cast",
    "test_mod_viktor_chaos_storm_duration",
    "test_mod_viktor_storm_impact",
    "test_mod_viktor_evolution",
    "test_mod_viktor_ult_voice",
)
VIKTOR_LASER_MIN_APPLY = 120
VIKTOR_AFTERSHOCK_MIN_APPLY = 132
VIKTOR_GRAVITY_MIN_TICKS = (300, 360)
VIKTOR_LASER_MIN_ANIM_SECONDS = 2.0
VIKTOR_AFTERSHOCK_MIN_ANIM_SECONDS = 2.0
VIKTOR_GRAVITY_MIN_ANIM_SECONDS = 5.0
VIKTOR_STORM_MIN_TICKS = (420, 480)
VIKTOR_STORM_MIN_ANIM_SECONDS = 6.0
BLITZCRANK_SOUND_EVENTS = (
    "test_mod_blitzcrank_attack_cast",
    "test_mod_blitzcrank_attack_hit",
    "test_mod_blitzcrank_power_fist_hit",
    "test_mod_blitzcrank_q_cast",
    "test_mod_blitzcrank_q_hit",
    "test_mod_blitzcrank_overdrive_cast",
    "test_mod_blitzcrank_barrier",
    "test_mod_blitzcrank_r_cast",
    "test_mod_blitzcrank_r_hit",
    "test_mod_blitzcrank_ult_voice",
)
AATROX_RUNTIME_FRAME_SIZE = (96, 72)
AATROX_RUNTIME_RUN_FRAME_XS = (4224, 4320, 4416, 4512, 4608, 4704, 4800, 4896)
AATROX_RUNTIME_ATTACK_FRAME_XS = (4992, 5088, 5184, 5280, 5376, 5472, 5568, 5664, 5760)
AATROX_RUNTIME_MAX_BASIC_ATTACK_WIDTH = 62
AATROX_RUNTIME_MIN_BASIC_ATTACK_UNIQUE_FRAMES = 7
AATROX_RUNTIME_MIN_BASIC_ATTACK_SWING_FRAMES = 2
AATROX_RUNTIME_MIN_BASIC_ATTACK_SWING_WIDTH = 58
AATROX_RUNTIME_MIN_BASIC_ATTACK_WIDTH_RANGE = 12
JHIN_RUNTIME_FRAME_SIZE = (64, 64)
JHIN_RUNTIME_RUN_FRAME_XS = tuple(range(0, 640, 64))
JHIN_RUNTIME_MIN_RUN_UNIQUE_FRAMES = 8
JHIN_RUNTIME_MAX_UPRIGHT_RUN_WIDTH = 50
JHIN_RUNTIME_MIN_UPRIGHT_RUN_HEIGHT = 47
JHIN_RUNTIME_MAX_UPRIGHT_RUN_TOP = 8
REQUIRED_DESCRIPTION_KEYS = ("name", "attack", "skill", "skill2", "ult")
REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS: dict[str, dict[str, tuple[str, ...]]] = {
    f"{MOD_ID}_aatrox": {
        "en": ("Aatrox",),
        "zh-hans": ("亚托克斯", "剑魔"),
        "zh-hant": ("亞托克斯", "劍魔"),
    },
    f"{MOD_ID}_blitzcrank": {
        "en": ("Blitzcrank", "Rocket Grab", "Overdrive", "Power Fist", "Static Field"),
        "zh-hans": ("\u84b8\u6c7d\u673a\u5668\u4eba", "\u5e03\u91cc\u8328", "\u673a\u68b0\u98de\u722a", "\u8fc7\u8f7d\u8fd0\u8f6c", "\u80fd\u91cf\u94c1\u62f3", "\u9759\u7535\u529b\u573a"),
        "zh-hant": ("\u84b8\u6c7d\u6a5f\u5668\u4eba", "\u5e03\u91cc\u8328", "\u6a5f\u68b0\u98db\u722a", "\u904e\u8f09\u904b\u8f49", "\u80fd\u91cf\u9435\u62f3", "\u975c\u96fb\u529b\u5834"),
    },
    f"{MOD_ID}_darius": {
        "en": ("Darius", "Hand of Noxus", "Hemorrhage", "Decimate", "Apprehend", "Crippling Strike", "Noxian Guillotine"),
        "zh-hans": ("诺克萨斯之手", "诺手", "Darius", "出血", "大杀四方", "无情铁手", "致残打击", "诺克萨斯断头台"),
        "zh-hant": ("諾克薩斯之手", "諾手", "Darius", "出血", "大殺四方", "無情鐵手", "致殘打擊", "諾克薩斯斷頭台"),
    },
    f"{MOD_ID}_kayn": {
        "en": ("Kayn", "Shadow Reaper"),
        "zh-hans": ("影流之镰", "凯隐"),
        "zh-hant": ("影流之鐮", "慨影"),
    },
    f"{MOD_ID}_yasuo": {
        "en": ("Yasuo", "Unforgiven"),
        "zh-hans": ("疾风剑豪", "亚索"),
        "zh-hant": ("疾風劍豪", "犽宿"),
    },
    f"{MOD_ID}_jinx": {
        "en": ("Jinx", "Loose Cannon"),
        "zh-hans": ("暴走萝莉", "金克丝"),
        "zh-hant": ("暴走蘿莉", "金克絲"),
    },
    f"{MOD_ID}_thresh": {
        "en": ("Thresh", "Chain Warden"),
        "zh-hans": ("魂锁典狱长", "锤石"),
        "zh-hant": ("魂鎖典獄長", "瑟雷西"),
    },
    f"{MOD_ID}_viktor": {
        "en": ("Viktor", "Herald of the Arcane", "Glorious Evolution", "Hextech Ray", "Gravity Field", "Arcane Storm"),
        "zh-hans": ("维克托", "奥术先驱", "光荣进化", "海克斯射线", "重力场", "奥术风暴"),
        "zh-hant": ("維克特", "奧術先驅", "光榮進化", "海克斯射線", "重力場", "奧術風暴"),
    },
}
REQUIRED_ENCYCLOPEDIA_NAME_TERMS: dict[str, dict[str, tuple[str, ...]]] = {
    f"{MOD_ID}_aatrox": {
        "zh-hans": ("\u6697\u88d4\u5251\u9b54",),
        "zh-hant": ("\u6697\u88d4\u528d\u9b54",),
    },
}
SIDE_CARD_STANDING_FACE_OFFSETS = {
    f"{MOD_ID}_aatrox": {"x": -8, "y": -6},
    f"{MOD_ID}_blitzcrank": {"x": 0, "y": -14},
    f"{MOD_ID}_darius": {"x": 0, "y": -12},
    f"{MOD_ID}_kayn": {"x": 4, "y": -18},
    f"{MOD_ID}_jhin": {"x": 0, "y": -28},
    f"{MOD_ID}_jinx": {"x": -2, "y": -16},
    f"{MOD_ID}_thresh": {"x": 0, "y": -15},
    f"{MOD_ID}_viktor": {"x": 0, "y": -28},
    f"{MOD_ID}_fiddlesticks": {"x": 0, "y": -2},
    f"{MOD_ID}_yasuo": {"x": 4, "y": -12},
}
SIDE_CARD_STANDING_CENTER_OFFSETS = {
    f"{MOD_ID}_aatrox": {"x": 4, "y": -16},
    f"{MOD_ID}_blitzcrank": {"x": 0, "y": -18},
    f"{MOD_ID}_darius": {"x": 0, "y": -12},
    f"{MOD_ID}_kayn": {"x": 0, "y": -12},
    f"{MOD_ID}_jhin": {"x": 0, "y": -22},
    f"{MOD_ID}_jinx": {"x": 0, "y": -16},
    f"{MOD_ID}_thresh": {"x": 0, "y": -15},
    f"{MOD_ID}_viktor": {"x": 0, "y": -12},
    f"{MOD_ID}_fiddlesticks": {"x": 0, "y": -14},
    f"{MOD_ID}_yasuo": {"x": 0, "y": -12},
}


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # pragma: no cover - used as a local QA script.
        raise AssertionError(f"{path} is not valid JSON: {exc}") from exc


def check_view_effect_types(path: Path, champion: object) -> None:
    if not isinstance(champion, dict):
        fail(f"{path} must contain a JSON object")
    effects = champion.get("view_effects", [])
    if not isinstance(effects, list):
        fail(f"{path} view_effects must be a list")
    allowed = {"Animation", "LoopAnimation"}
    for index, effect in enumerate(effects):
        if not isinstance(effect, dict):
            fail(f"{path} view_effects[{index}] must be an object")
        effect_type = effect.get("type")
        if effect_type not in allowed:
            fail(
                f"{path} view_effects[{index}].type must be one of "
                f"{sorted(allowed)}, got {effect_type!r}"
            )


def iter_mapping_nodes(node: object) -> list[dict[str, object]]:
    if isinstance(node, dict):
        out = [node]
        for value in node.values():
            out.extend(iter_mapping_nodes(value))
        return out
    if isinstance(node, list):
        out: list[dict[str, object]] = []
        for item in node:
            out.extend(iter_mapping_nodes(item))
        return out
    return []


def animation_total_duration(path: Path, tag: str) -> float:
    fanim = load_json(path)
    frames = fanim.get("anims", {}).get(tag, {}).get("frames") if isinstance(fanim, dict) else None
    if not isinstance(frames, list) or not frames:
        fail(f"{path} must expose {tag!r} frames")
    total = 0.0
    for index, frame in enumerate(frames):
        duration = frame.get("duration") if isinstance(frame, dict) else None
        if not isinstance(duration, (int, float)):
            fail(f"{path} {tag} frame {index} missing numeric duration")
        total += float(duration)
    return total


def load_rgba_alpha(path: Path) -> tuple[int, int, bytes]:
    raw = path.read_bytes()
    if not raw.startswith(b"\x89PNG\r\n\x1a\n"):
        fail(f"{path} is not a PNG file")

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
        fail(f"{path} missing PNG IHDR")
    if bit_depth != 8 or color_type != 6 or interlace != 0:
        fail(f"{path} must be non-interlaced 8-bit RGBA PNG for runtime alpha QA")

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
                fail(f"{path} has unsupported PNG row filter {filter_type}")
            row[i] = recon & 0xFF
        rows.append(row)

    alpha = bytearray(width * height)
    for y, row in enumerate(rows):
        for x in range(width):
            alpha[y * width + x] = row[x * bpp + 3]
    return width, height, bytes(alpha)


def alpha_bbox_in_rect(alpha: bytes, image_width: int, rect: tuple[int, int, int, int]) -> tuple[int, int, int, int] | None:
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


def check_aatrox_basic_attack_motion(runtime_root: Path) -> None:
    sheet_path = runtime_root / "aseprite_resources" / "champions" / "aatrox#sheet.png"
    sheet_width, _sheet_height, alpha = load_rgba_alpha(sheet_path)
    frame_w, frame_h = AATROX_RUNTIME_FRAME_SIZE
    run_hashes = {
        alpha_frame_hash(alpha, sheet_width, (x, 0, frame_w, frame_h))
        for x in AATROX_RUNTIME_RUN_FRAME_XS
    }
    attack_hashes: list[str] = []
    attack_widths: list[int] = []
    reused_run_frames: list[int] = []
    for index, x in enumerate(AATROX_RUNTIME_ATTACK_FRAME_XS, start=1):
        rect = (x, 0, frame_w, frame_h)
        bbox = alpha_bbox_in_rect(alpha, sheet_width, rect)
        if bbox is None:
            fail(f"runtime Aatrox attack frame {index} is blank")
        width = bbox[2] - bbox[0]
        if width > AATROX_RUNTIME_MAX_BASIC_ATTACK_WIDTH:
            fail(
                f"runtime Aatrox attack frame {index} is {width}px wide; "
                "basic attack must stay smaller than Q-sized cleaves"
            )
        frame_hash = alpha_frame_hash(alpha, sheet_width, rect)
        attack_hashes.append(frame_hash)
        attack_widths.append(width)
        if frame_hash in run_hashes:
            reused_run_frames.append(index)
    if reused_run_frames:
        fail(f"runtime Aatrox basic attack reuses run-frame silhouettes: {reused_run_frames}")
    if len(set(attack_hashes)) < AATROX_RUNTIME_MIN_BASIC_ATTACK_UNIQUE_FRAMES:
        fail("runtime Aatrox basic attack must have at least seven distinct actor silhouettes")
    wide_frames = sum(width >= AATROX_RUNTIME_MIN_BASIC_ATTACK_SWING_WIDTH for width in attack_widths)
    if wide_frames < AATROX_RUNTIME_MIN_BASIC_ATTACK_SWING_FRAMES:
        fail("runtime Aatrox basic attack must show at least two readable greatsword swing frames")
    if max(attack_widths) - min(attack_widths) < AATROX_RUNTIME_MIN_BASIC_ATTACK_WIDTH_RANGE:
        fail("runtime Aatrox basic attack must include visible windup-to-swing width change")


def check_jhin_upright_run_pose(runtime_root: Path) -> None:
    sheet_path = runtime_root / "aseprite_resources" / "champions" / "jhin#sheet.png"
    sheet_width, _sheet_height, alpha = load_rgba_alpha(sheet_path)
    frame_w, frame_h = JHIN_RUNTIME_FRAME_SIZE
    hashes: list[str] = []
    widths: list[int] = []
    heights: list[int] = []
    tops: list[int] = []
    for index, x in enumerate(JHIN_RUNTIME_RUN_FRAME_XS, start=1):
        rect = (x, 0, frame_w, frame_h)
        bbox = alpha_bbox_in_rect(alpha, sheet_width, rect)
        if bbox is None:
            fail(f"runtime Jhin run frame {index} is blank")
        hashes.append(alpha_frame_hash(alpha, sheet_width, rect))
        widths.append(bbox[2] - bbox[0])
        heights.append(bbox[3] - bbox[1])
        tops.append(bbox[1])
    if len(set(hashes)) < JHIN_RUNTIME_MIN_RUN_UNIQUE_FRAMES:
        fail("runtime Jhin run must keep at least eight distinct upright generated stride poses")
    if max(widths) > JHIN_RUNTIME_MAX_UPRIGHT_RUN_WIDTH:
        fail("runtime Jhin run is too wide and has regressed toward the horizontal rifle sprint")
    if min(heights) < JHIN_RUNTIME_MIN_UPRIGHT_RUN_HEIGHT:
        fail("runtime Jhin run is too short and has regressed toward crouched sprint poses")
    if max(tops) > JHIN_RUNTIME_MAX_UPRIGHT_RUN_TOP:
        fail("runtime Jhin run top is too low; keep an upright LoL-like posture")


def assert_no_negative_speed_fields(node: object, label: str) -> None:
    for mapping in iter_mapping_nodes(node):
        speed = mapping.get("speed")
        if isinstance(speed, (int, float)) and speed < 0:
            effect_type = mapping.get("type", "<unknown>")
            fail(f"{label} has invalid negative speed {speed!r} on {effect_type}; TFM2 expects unsigned movement speeds")


def check_darius_ult_visibility(path: Path, champion: object) -> None:
    if path.name != "darius.data_champion":
        return
    if not isinstance(champion, dict):
        fail(f"{path} must contain a JSON object")
    view_effects_by_name = {
        item.get("name"): item
        for item in champion.get("view_effects", [])
        if isinstance(item, dict) and isinstance(item.get("name"), str)
    }
    guillotine_cast_vfx = view_effects_by_name.get("test_mod_darius_noxian_guillotine_cast_vfx")
    if guillotine_cast_vfx is None:
        fail("runtime Darius R cast VFX must be defined")
    if guillotine_cast_vfx.get("is_follow") is not False:
        fail("runtime Darius R cast VFX must stay fixed on the target point instead of following a unit")
    if guillotine_cast_vfx.get("z", 0) < 4:
        fail("runtime Darius R cast VFX must render above units so the execution chop remains visible")
    caster_following_ult_chops = [
        node
        for node in iter_mapping_nodes(champion.get("ult", {}))
        if node.get("type") == "CasterViewEffect"
        and node.get("name") == "test_mod_darius_noxian_guillotine_cast_vfx"
    ]
    if caster_following_ult_chops:
        fail("runtime Darius R chop VFX must be target-anchored, not caster-following")
    ult_target_chop_branches: list[list[dict[str, object]]] = []
    for node in iter_mapping_nodes(champion.get("ult", {})):
        if node.get("type") != "Combine":
            continue
        effects = node.get("effects")
        if not isinstance(effects, list):
            continue
        has_r_cast_sound = any(
            isinstance(item, dict)
            and item.get("type") == "Sfx"
            and item.get("name") == "test_mod_darius_r_cast"
            for item in effects
        )
        has_direct_damage_combine = any(
            isinstance(item, dict)
            and item.get("type") == "Combine"
            and any(isinstance(child, dict) and child.get("type") == "FixedAttack" for child in item.get("effects", []))
            for item in effects
        )
        if has_r_cast_sound and has_direct_damage_combine:
            ult_target_chop_branches.append([item for item in effects if isinstance(item, dict)])
    if len(ult_target_chop_branches) != 7:
        fail(f"runtime Darius R must keep seven target-visible guillotine branches, got {len(ult_target_chop_branches)}")
    for branch_index, effects in enumerate(ult_target_chop_branches, start=1):
        chop_index = next(
            (
                index
                for index, item in enumerate(effects)
                if item.get("type") == "ViewEffect"
                and item.get("name") == "test_mod_darius_noxian_guillotine_cast_vfx"
            ),
            None,
        )
        damage_index = next(
            (
                index
                for index, item in enumerate(effects)
                if item.get("type") == "Combine"
                and any(isinstance(child, dict) and child.get("type") == "FixedAttack" for child in item.get("effects", []))
            ),
            None,
        )
        if chop_index is None:
            fail(f"runtime Darius R branch {branch_index} must directly spawn the target chop ViewEffect")
        if damage_index is None or chop_index > damage_index:
            fail(f"runtime Darius R branch {branch_index} must show the chop before damage resolves")


def check_viktor_ground_vfx(path: Path, champion: object) -> None:
    if path.name != "viktor.data_champion":
        return
    if not isinstance(champion, dict):
        fail(f"{path} must contain a JSON object")
    view_projectile_rows = champion.get("view_projectiles", [])
    if not isinstance(view_projectile_rows, list):
        fail(f"{path} view_projectiles must be a list")
    projectile_z = {item.get("name"): item.get("z") for item in view_projectile_rows if isinstance(item, dict)}
    projectile_repeat = {item.get("name"): item.get("repeat") for item in view_projectile_rows if isinstance(item, dict)}
    if projectile_z.get("test_mod_viktor_siphon_projectile") != 2:
        fail("runtime Viktor Siphon Power Q projectile must render at z=2 so it is visible in battle")
    if projectile_repeat.get("test_mod_viktor_siphon_projectile") is not True:
        fail("runtime Viktor Siphon Power Q projectile must repeat while travelling")
    for projectile_name in ("test_mod_viktor_laser", "test_mod_viktor_laser_aftershock"):
        z_value = projectile_z.get(projectile_name)
        if not isinstance(z_value, (int, float)) or z_value >= 0:
            fail(f"runtime Viktor {projectile_name} must render on the ground layer with negative z")
    skill = champion.get("skill", {})
    laser_nodes = [
        node
        for node in iter_mapping_nodes(skill)
        if node.get("type") == "LineRangeProjectile"
        and node.get("name") in {
            "test_mod_viktor_laser",
            "test_mod_viktor_laser_champion_bonus",
            "test_mod_viktor_laser_aftershock",
        }
    ]
    for projectile_name in ("test_mod_viktor_laser", "test_mod_viktor_laser_champion_bonus"):
        nodes = [node for node in laser_nodes if node.get("name") == projectile_name]
        if len(nodes) != 2:
            fail(f"runtime Viktor Hextech Ray must define two {projectile_name} projectiles")
        for node in nodes:
            if node.get("apply", 0) < VIKTOR_LASER_MIN_APPLY:
                fail(f"runtime Viktor {projectile_name} must persist for at least {VIKTOR_LASER_MIN_APPLY} ticks")
    aftershock_nodes = [node for node in laser_nodes if node.get("name") == "test_mod_viktor_laser_aftershock"]
    if len(aftershock_nodes) != 2:
        fail("runtime Viktor Hextech Ray must define aftershock ground projectiles in both normal and evolved branches")
    for node in aftershock_nodes:
        if node.get("apply", 0) < VIKTOR_AFTERSHOCK_MIN_APPLY:
            fail(f"runtime Viktor laser aftershock must persist for at least {VIKTOR_AFTERSHOCK_MIN_APPLY} ticks")
        if node.get("delay", 999) > 0:
            fail("runtime Viktor laser aftershock projectile should appear immediately after its Delayed wrapper")
    view_effect_rows = champion.get("view_effects", [])
    if not isinstance(view_effect_rows, list):
        fail(f"{path} view_effects must be a list")
    view_effect_z = {item.get("name"): item.get("z") for item in view_effect_rows if isinstance(item, dict)}
    if view_effect_z.get("test_mod_viktor_siphon_shield", 0) >= 0:
        fail("runtime Viktor Siphon shield ViewEffect must render behind the actor")
    if view_effect_z.get("test_mod_viktor_siphon_impact") != 2:
        fail("runtime Viktor Siphon Power Q impact must render at z=2 so the hit is visible")
    if view_effect_z.get("test_mod_viktor_gravity_field") != 1:
        fail("runtime Viktor Gravity Field must render at z=1 so the target-ground field is visible above terrain")
    if view_effect_z.get("test_mod_viktor_chaos_storm") != 2:
        fail("runtime Viktor Chaos Storm must render at z=2 so the target-ground ult remains visible")
    view_buff_rows = champion.get("view_buffs", [])
    if not isinstance(view_buff_rows, list):
        fail(f"{path} view_buffs must be a list")
    for buff_name in (
        "test_mod_viktor_siphon_empower",
        "test_mod_viktor_evolved_ray",
        "test_mod_viktor_evolved_field",
        "test_mod_viktor_evolved_storm",
    ):
        z_value = next((item.get("z") for item in view_buff_rows if isinstance(item, dict) and item.get("name") == buff_name), None)
        if not isinstance(z_value, (int, float)) or z_value >= 0:
            fail(f"runtime Viktor buff {buff_name} must render behind the actor")
    skill2 = champion.get("skill2", {})
    skill2_effect = skill2.get("effect", {}) if isinstance(skill2, dict) else {}
    skill2_effects = skill2_effect.get("effects", []) if isinstance(skill2_effect, dict) else []
    if not isinstance(skill2_effects, list):
        fail(f"{path} skill2.effect.effects must be a list")
    for node in skill2_effects:
        if not isinstance(node, dict):
            continue
        if node.get("type") == "CasterViewEffect" and node.get("name") == "test_mod_viktor_siphon_shield":
            fail("runtime Viktor skill2 still double-attaches the Siphon shield over the actor body")
        if node.get("type") == "ViewEffect" and node.get("name") == "test_mod_viktor_gravity_field":
            fail("runtime Viktor Gravity Field is still a caster-level ViewEffect instead of a target-ground anchor")

    siphon_projectiles = [
        (index, node)
        for index, node in enumerate(skill2_effects)
        if isinstance(node, dict)
        and node.get("type") == "ParabolicProjectile"
        and node.get("name") == "test_mod_viktor_siphon_projectile"
    ]
    if len(siphon_projectiles) != 1:
        fail("runtime Viktor Siphon Power Q must directly fire one visible projectile from skill2")
    siphon_index, siphon_projectile = siphon_projectiles[0]
    if siphon_projectile.get("travel_time", 999) > 8 or siphon_projectile.get("range", 0) < 72000:
        fail("runtime Viktor Siphon Power Q projectile must be fast and cover the full cast range")
    end_effects = siphon_projectile.get("end_effects")
    if not isinstance(end_effects, list) or not any(
        item.get("type") == "ViewEffect" and item.get("name") == "test_mod_viktor_siphon_impact"
        for item in end_effects
        if isinstance(item, dict)
    ):
        fail("runtime Viktor Siphon Power Q projectile must spawn the visible target impact")
    empower_index = next(
        (
            index
            for index, node in enumerate(skill2_effects)
            if isinstance(node, dict)
            and node.get("type") == "AddCasterBuff"
            and node.get("buff_state", {}).get("name") == "test_mod_viktor_siphon_empower"
        ),
        None,
    )
    gravity_index = next(
        (
            index
            for index, node in enumerate(skill2_effects)
            if isinstance(node, dict)
            and node.get("type") == "SwitchByBuff"
            and node.get("buff_name") == "test_mod_viktor_evolved_field"
        ),
        None,
    )
    if empower_index is None or gravity_index is None or siphon_index > empower_index or siphon_index > gravity_index:
        fail("runtime Viktor Siphon Power Q projectile must appear before the shield empower and Gravity Field follow-up")

    gravity_anchors = [
        node
        for node in iter_mapping_nodes(skill2)
        if node.get("type") == "ParabolicProjectile" and node.get("name") == "test_mod_viktor_gravity_field_anchor"
    ]
    if len(gravity_anchors) != 2:
        fail("runtime Viktor skill2 must use two gravity-field target-ground anchors")
    for index, anchor in enumerate(gravity_anchors, start=1):
        end_effects = anchor.get("end_effects")
        if not isinstance(end_effects, list):
            fail(f"runtime Viktor gravity anchor {index} must use end_effects")
        if not any(item.get("type") == "ViewEffect" and item.get("name") == "test_mod_viktor_gravity_field" for item in end_effects if isinstance(item, dict)):
            fail(f"runtime Viktor gravity anchor {index} must spawn Gravity Field at the target point")
        if any(item.get("type") == "ViewEffect" and item.get("name") == "test_mod_viktor_gravity_field" and item.get("is_follow") is True for item in end_effects if isinstance(item, dict)):
            fail(f"runtime Viktor gravity anchor {index} must keep Gravity Field on the terrain, not attached to the caster")
        field_pulses = [
            item
            for item in end_effects
            if isinstance(item, dict)
            and item.get("type") == "RangePeriodProjectile"
            and item.get("name") == "test_mod_viktor_gravity_field"
        ]
        if len(field_pulses) != 1:
            fail(f"runtime Viktor gravity anchor {index} must own the ground pulse")
        if int(field_pulses[0].get("tick", 0)) < VIKTOR_GRAVITY_MIN_TICKS[index - 1]:
            fail(
                f"runtime Viktor Gravity Field anchor {index} must persist for at least "
                f"{VIKTOR_GRAVITY_MIN_TICKS[index - 1]} ticks"
            )

    ult = champion.get("ult", {})
    ult_effect = ult.get("effect", {}) if isinstance(ult, dict) else {}
    ground_storm_names = {"test_mod_viktor_storm_impact", "test_mod_viktor_chaos_storm"}
    if isinstance(ult_effect, dict):
        for branch_name in ("effect_none", "effect_buff"):
            branch = ult_effect.get(branch_name, {})
            branch_effects = branch.get("effects", []) if isinstance(branch, dict) else []
            if not isinstance(branch_effects, list):
                fail(f"{path} ult.{branch_name}.effects must be a list")
            for node in branch_effects:
                if not isinstance(node, dict):
                    continue
                if node.get("type") in {"ViewEffect", "RangePeriodProjectile"} and node.get("name") in ground_storm_names:
                    fail(f"runtime Viktor ult {branch_name} still spawns storm terrain VFX outside the target-ground anchor")
    storm_anchors = [
        node
        for node in iter_mapping_nodes(ult)
        if node.get("type") == "ParabolicProjectile" and node.get("name") == "test_mod_viktor_chaos_storm_anchor"
    ]
    if len(storm_anchors) != 2:
        fail("runtime Viktor ult must use two Chaos Storm target-ground anchors")
    for index, anchor in enumerate(storm_anchors, start=1):
        end_effects = anchor.get("end_effects")
        if not isinstance(end_effects, list):
            fail(f"runtime Viktor Chaos Storm anchor {index} must use end_effects")
        end_names = {(item.get("type"), item.get("name")) for item in end_effects if isinstance(item, dict)}
        if ("ViewEffect", "test_mod_viktor_storm_impact") not in end_names or ("ViewEffect", "test_mod_viktor_chaos_storm") not in end_names:
            fail(f"runtime Viktor Chaos Storm anchor {index} must spawn both storm terrain VFX")
        if any(item.get("type") == "ViewEffect" and item.get("name") == "test_mod_viktor_chaos_storm" and item.get("is_follow") is True for item in end_effects if isinstance(item, dict)):
            fail(f"runtime Viktor Chaos Storm anchor {index} must keep the storm on the terrain, not attached to the caster")
        storm_pulses = [
            item
            for item in end_effects
            if isinstance(item, dict)
            and item.get("type") == "RangePeriodProjectile"
            and item.get("name") == "test_mod_viktor_chaos_storm"
        ]
        if not storm_pulses:
            fail(f"runtime Viktor Chaos Storm anchor {index} must own the persistent storm pulse")
        if storm_pulses[0].get("tick", 0) < VIKTOR_STORM_MIN_TICKS[index - 1]:
            fail(f"runtime Viktor Chaos Storm anchor {index} must persist for at least {VIKTOR_STORM_MIN_TICKS[index - 1]} ticks")
    runtime_root = path.parent.parent
    for anim_name, tag, label, min_seconds in (
        ("viktor_laser", "laser", "runtime Viktor Hextech Ray ground VFX", VIKTOR_LASER_MIN_ANIM_SECONDS),
        ("viktor_laser_aftershock", "burn", "runtime Viktor Hextech Ray aftershock VFX", VIKTOR_AFTERSHOCK_MIN_ANIM_SECONDS),
        ("viktor_gravity_field", "gravity_field", "runtime Viktor Gravity Field VFX", VIKTOR_GRAVITY_MIN_ANIM_SECONDS),
    ):
        anim_path = runtime_root / "aseprite_resources" / "effects" / f"{anim_name}#anim.fanim"
        total_duration = animation_total_duration(anim_path, tag)
        if total_duration < min_seconds:
            fail(
                f"{label} lasts only {total_duration:.2f}s; "
                f"must last at least {min_seconds:.2f}s so the terrain skill remains readable"
            )
    storm_anim = runtime_root / "aseprite_resources" / "effects" / "viktor_chaos_storm#anim.fanim"
    total_duration = animation_total_duration(storm_anim, "chaos_storm")
    if total_duration < VIKTOR_STORM_MIN_ANIM_SECONDS:
        fail(
            f"runtime Viktor Chaos Storm loop VFX lasts only {total_duration:.2f}s; "
            f"must last at least {VIKTOR_STORM_MIN_ANIM_SECONDS:.2f}s so the ground ult stays visible"
        )


def check_thresh_ult_visibility(path: Path, champion: object) -> None:
    if path.name != "thresh.data_champion":
        return
    if not isinstance(champion, dict):
        fail(f"{path} must contain a JSON object")
    q_nodes = iter_mapping_nodes(champion.get("skill", {}))
    q_move_to = [
        node
        for node in q_nodes
        if node.get("type") == "MoveTo"
    ]
    if not any(int(node.get("speed", 0)) >= 5200 and int(node.get("range", 999999)) <= 8000 for node in q_move_to):
        fail("runtime Thresh Q must strongly pull the hooked target back toward Thresh")
    q_stuns = [node for node in q_nodes if node.get("type") == "Stun"]
    if not any(int(node.get("duration", 0)) >= 50 for node in q_stuns):
        fail("runtime Thresh Q must hold the hooked target long enough for the pull-back to be visible")
    q_blocks = [node for node in q_nodes if node.get("type") == "BlockMoveSkill"]
    if not any(int(node.get("tick", 0)) >= 42 for node in q_blocks):
        fail("runtime Thresh Q must block movement skills long enough for Death Sentence pull-back to resolve")
    flay_nodes = [
        node
        for node in iter_mapping_nodes(champion.get("skill2", {}))
        if node.get("type") == "LineRangeProjectile" and node.get("name") == "test_mod_thresh_flay_sweep"
    ]
    if len(flay_nodes) != 1:
        fail("runtime Thresh E/Flay must use exactly one sweep projectile")
    flay = flay_nodes[0]
    if any(node.get("type") == "Knockback" for node in iter_mapping_nodes(flay)):
        fail("runtime Thresh E/Flay must not use Knockback; it should visibly pull enemies back toward Thresh")
    flay_move_to = [node for node in iter_mapping_nodes(flay) if node.get("type") == "MoveTo"]
    if not any(int(node.get("speed", 0)) >= 4800 and int(node.get("range", 999999)) <= 10000 for node in flay_move_to):
        fail("runtime Thresh E/Flay must include a strong MoveTo pull")
    flay_stuns = [node for node in iter_mapping_nodes(flay) if node.get("type") == "Stun"]
    if not any(int(node.get("duration", 0)) >= 16 for node in flay_stuns):
        fail("runtime Thresh E/Flay must briefly hold enemies after pulling them")
    flay_blocks = [node for node in iter_mapping_nodes(flay) if node.get("type") == "BlockMoveSkill"]
    if not any(int(node.get("tick", 0)) >= 20 for node in flay_blocks):
        fail("runtime Thresh E/Flay must block movement skills long enough for pull-back to read")
    view_effect_rows = champion.get("view_effects", [])
    if not isinstance(view_effect_rows, list):
        fail(f"{path} view_effects must be a list")
    view_effect_z = {item.get("name"): item.get("z") for item in view_effect_rows if isinstance(item, dict)}
    view_effect_type = {item.get("name"): item.get("type") for item in view_effect_rows if isinstance(item, dict)}
    view_effect_follow = {item.get("name"): item.get("is_follow") for item in view_effect_rows if isinstance(item, dict)}
    view_effect_ref = {item.get("name"): (item.get("anim"), item.get("tag")) for item in view_effect_rows if isinstance(item, dict)}
    if view_effect_ref.get("test_mod_thresh_lantern_visual") != (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_lantern",
        "loop",
    ):
        fail("runtime Thresh W lantern visual must be registered as a ground ViewEffect")
    if view_effect_type.get("test_mod_thresh_lantern_visual") != "Animation":
        fail("runtime Thresh W lantern visual must be one-shot Animation, not a lingering actor-attached loop")
    if view_effect_z.get("test_mod_thresh_lantern_visual") != 1:
        fail("runtime Thresh W lantern visual must render at z=1 near the ground")
    if view_effect_follow.get("test_mod_thresh_lantern_visual") is not False:
        fail("runtime Thresh W lantern visual must use is_follow=false to avoid second-Thresh afterimages")
    view_buff_rows = champion.get("view_buffs", [])
    if not isinstance(view_buff_rows, list):
        fail(f"{path} view_buffs must be a list")
    if view_buff_rows:
        names = [item.get("name") for item in view_buff_rows if isinstance(item, dict)]
        fail(f"runtime Thresh must not define actor-attached view_buffs that can look like a second body, got {names}")
    for node in iter_mapping_nodes(champion.get("skill2", {})):
        if node.get("type") == "AddCasterBuff" and node.get("buff_state", {}).get("name") == "test_mod_thresh_lantern_visual":
            fail("runtime Thresh W lantern visual must be a non-following ViewEffect, not AddCasterBuff")
    for name in ("test_mod_thresh_box", "test_mod_thresh_box_field"):
        if view_effect_z.get(name) != 3:
            fail(f"runtime Thresh {name} must render at z=3 so The Box remains obvious")
    box_fields = [
        node
        for node in iter_mapping_nodes(champion.get("ult", {}))
        if node.get("type") == "RangePeriodProjectile" and node.get("name") == "test_mod_thresh_box_field"
    ]
    if len(box_fields) != 1 or int(box_fields[0].get("tick", 0)) < THRESH_BOX_MIN_TICKS:
        fail(f"runtime Thresh R field must persist for at least {THRESH_BOX_MIN_TICKS} ticks")
    runtime_root = path.parent.parent
    box_anim = runtime_root / "aseprite_resources" / "effects" / "thresh_box#anim.fanim"
    total_duration = animation_total_duration(box_anim, "box")
    if total_duration < THRESH_BOX_MIN_ANIM_SECONDS:
        fail(
            f"runtime Thresh The Box VFX lasts only {total_duration:.2f}s; "
            f"must last at least {THRESH_BOX_MIN_ANIM_SECONDS:.2f}s so the terrain prison stays visible"
        )
    ult_effect = champion.get("ult", {}).get("effect", {})
    ult_direct_effects = ult_effect.get("effects") if isinstance(ult_effect, dict) else None
    if not isinstance(ult_direct_effects, list):
        fail("runtime Thresh R must keep its top-level Combine effects list")
    if any(isinstance(node, dict) and node.get("type") == "ViewEffect" and node.get("name", "").startswith("test_mod_thresh_box") for node in ult_direct_effects):
        fail("runtime Thresh R must use CasterViewEffect for self-centered ground walls")
    if any(isinstance(node, dict) and node.get("type") == "ParabolicProjectile" and node.get("name") == "test_mod_thresh_box_ground_anchor" for node in ult_direct_effects):
        fail("runtime Thresh R must not use the target-ground anchor that hides The Box away from Thresh")
    caster_vfx = {
        node.get("name")
        for node in ult_direct_effects
        if isinstance(node, dict) and node.get("type") == "CasterViewEffect"
    }
    for required_vfx in ("test_mod_thresh_box", "test_mod_thresh_box_field"):
        if required_vfx not in caster_vfx:
            fail(f"runtime Thresh R must spawn {required_vfx} from Thresh's cast point")
    with_self_effects = [
        effect
        for node in ult_direct_effects
        if isinstance(node, dict) and node.get("type") == "WithSelf" and isinstance(node.get("effects"), list)
        for effect in node["effects"]
        if isinstance(effect, dict)
    ]
    around_caster_hits = [
        node for node in with_self_effects
        if node.get("type") == "RangeEffect"
        and node.get("apply_type") == "AroundCaster"
        and node.get("target") == "EnemyWithoutTower"
    ]
    if len(around_caster_hits) != 1:
        fail("runtime Thresh R must apply its hit through exactly one WithSelf AroundCaster RangeEffect")
    box_shape = around_caster_hits[0].get("shape", {}).get("Circle", {}) if isinstance(around_caster_hits[0].get("shape"), dict) else {}
    if int(box_shape.get("radius", 0)) < 50000:
        fail("runtime Thresh R AroundCaster RangeEffect must keep a large enough radius")
    hit_effect_types = {effect.get("type") for effect in around_caster_hits[0].get("effects", []) if isinstance(effect, dict)}
    for required_effect in ("ApAttack", "AddBuff", "BlockMoveSkill", "TargetSfx"):
        if required_effect not in hit_effect_types:
            fail(f"runtime Thresh R AroundCaster RangeEffect must include {required_effect}")
    if not any(
        node.get("type") == "RangePeriodProjectile"
        and node.get("name") == "test_mod_thresh_box_field"
        and int(node.get("tick", 0)) >= THRESH_BOX_MIN_TICKS
        for node in with_self_effects
    ):
        fail("runtime Thresh R must own a long-lived WithSelf terrain field")


def check_fiddlesticks_ult_visibility(path: Path, champion: object) -> None:
    if path.name != "fiddlesticks.data_champion":
        return
    if not isinstance(champion, dict):
        fail(f"{path} must contain a JSON object")
    view_projectile_rows = champion.get("view_projectiles", [])
    view_buff_rows = champion.get("view_buffs", [])
    view_effect_rows = champion.get("view_effects", [])
    if not isinstance(view_projectile_rows, list) or not isinstance(view_buff_rows, list) or not isinstance(view_effect_rows, list):
        fail(f"{path} view_projectiles, view_buffs, and view_effects must be lists")
    projectile_rows = {item.get("name"): item for item in view_projectile_rows if isinstance(item, dict)}
    drain_projectile = projectile_rows.get("test_mod_fiddlesticks_drain_beam")
    if not isinstance(drain_projectile, dict):
        fail("runtime Fiddlesticks W must use a caster-to-target drain beam projectile")
    if (
        drain_projectile.get("anim") != "asset/bo_league_champions/aseprite_resources/effects/fiddlesticks_drain_tether"
        or drain_projectile.get("tag") != "tether"
        or drain_projectile.get("z") != 2
        or drain_projectile.get("repeat") is not True
    ):
        fail("runtime Fiddlesticks drain beam projectile must use the generated tether art at z=2 and repeat during the channel")
    buff_z = {item.get("name"): item.get("z") for item in view_buff_rows if isinstance(item, dict)}
    effect_rows = {item.get("name"): item for item in view_effect_rows if isinstance(item, dict)}
    effect_z = {name: item.get("z") for name, item in effect_rows.items()}
    if "test_mod_fiddlesticks_drain_tether" in effect_z:
        fail("runtime Fiddlesticks W must not attach a full tether ViewEffect at the target point")
    if buff_z.get("test_mod_fiddlesticks_crowstorm_active") != 0:
        fail("runtime Fiddlesticks Crowstorm buff must render at z=0 so the storm rings the feet instead of covering the model")
    channel_effect = effect_rows.get("test_mod_fiddlesticks_crowstorm_channel")
    if not isinstance(channel_effect, dict):
        fail("runtime Fiddlesticks Crowstorm must register a generated pre-cast channel ViewEffect")
    if (
        channel_effect.get("type") != "Animation"
        or channel_effect.get("anim") != "asset/bo_league_champions/aseprite_resources/effects/fiddlesticks_crowstorm_channel"
        or channel_effect.get("tag") != "channel"
        or channel_effect.get("z") != 3
        or channel_effect.get("is_follow") is not True
    ):
        fail("runtime Fiddlesticks Crowstorm channel must follow the caster as a z=3 generated wind-up effect")
    storm_effect = effect_rows.get("test_mod_fiddlesticks_crowstorm")
    if not isinstance(storm_effect, dict):
        fail("runtime Fiddlesticks Crowstorm must register the generated landing-zone ViewEffect")
    if (
        storm_effect.get("type") != "LoopAnimation"
        or storm_effect.get("anim") != "asset/bo_league_champions/aseprite_resources/effects/fiddlesticks_crowstorm"
        or storm_effect.get("tag") != "storm"
        or storm_effect.get("z") != 0
        or storm_effect.get("is_follow") is not False
    ):
        fail("runtime Fiddlesticks Crowstorm field must anchor on terrain as a z=0 generated foot-ring, not cover the caster")
    drain_beams = [
        node
        for node in iter_mapping_nodes(champion.get("skill2", {}))
        if node.get("type") == "LineRangeProjectile"
        and node.get("name") == "test_mod_fiddlesticks_drain_beam"
    ]
    if len(drain_beams) != 1:
        fail("runtime Fiddlesticks W must create exactly one source-to-target drain beam")
    drain_beam = drain_beams[0]
    if drain_beam.get("applied_target") != "EnemyWithoutTower":
        fail("runtime Fiddlesticks drain beam must connect to enemy units")
    if drain_beam.get("width") != 7000 or drain_beam.get("length") != 36000:
        fail("runtime Fiddlesticks drain beam must be a narrow line, not a wide body-covering strip")
    if drain_beam.get("delay") != 0 or drain_beam.get("apply", 0) < 72:
        fail("runtime Fiddlesticks drain beam must persist for the full W channel")
    if drain_beam.get("applied_effects") != []:
        fail("runtime Fiddlesticks drain beam must remain visual-only; W pulses own the damage/heal")
    if any(node.get("name") == "test_mod_fiddlesticks_drain_tether" for node in iter_mapping_nodes(champion.get("skill2", {}))):
        fail("runtime Fiddlesticks W still references the retired target-point drain tether")
    ult = champion.get("ult", {})
    if not isinstance(ult, dict):
        fail("runtime Fiddlesticks ult must be a JSON object")
    start_timing = ult.get("start_timing")
    if not isinstance(start_timing, (int, float)) or start_timing > 6:
        fail("runtime Fiddlesticks Crowstorm must start its visible pre-cast quickly")
    if ult.get("cancelable") is not False or ult.get("can_use_with_move") is not False:
        fail("runtime Fiddlesticks Crowstorm must lock movement during the pre-cast channel")
    ult_effect = ult.get("effect", {})
    ult_effects = ult_effect.get("effects") if isinstance(ult_effect, dict) else None
    if not isinstance(ult_effects, list):
        fail("runtime Fiddlesticks Crowstorm must use a Combine effect list")
    if any(isinstance(node, dict) and node.get("type") == "Teleport" for node in ult_effects):
        fail("runtime Fiddlesticks Crowstorm must not teleport immediately before the channel")
    if not any(
        isinstance(node, dict)
        and node.get("type") == "CasterViewEffect"
        and node.get("name") == "test_mod_fiddlesticks_crowstorm_channel"
        for node in ult_effects
    ):
        fail("runtime Fiddlesticks Crowstorm must show the generated pre-cast channel")
    bind_nodes = [
        node
        for node in iter_mapping_nodes(ult)
        if node.get("type") == "Bind"
        and isinstance(node.get("duration"), (int, float))
        and node.get("duration") >= 48
    ]
    if len(bind_nodes) != 1:
        fail("runtime Fiddlesticks Crowstorm pre-cast must bind the caster for the full 48 tick channel")
    delayed_landings = [
        node
        for node in ult_effects
        if isinstance(node, dict)
        and node.get("type") == "Delayed"
        and node.get("tick", 0) >= 48
        and any(isinstance(effect, dict) and effect.get("type") == "Teleport" for effect in node.get("effects", []))
    ]
    if len(delayed_landings) != 1:
        fail("runtime Fiddlesticks Crowstorm must have exactly one delayed teleport landing after the channel")
    crowstorm_buffs = [
        node
        for node in iter_mapping_nodes(champion.get("ult", {}))
        if node.get("type") == "AddCasterBuff"
        and node.get("buff_state", {}).get("name") == "test_mod_fiddlesticks_crowstorm_active"
    ]
    if len(crowstorm_buffs) != 1:
        fail("runtime Fiddlesticks ult must apply exactly one Crowstorm visual buff")
    duration_tick = crowstorm_buffs[0].get("buff_state", {}).get("duration", {}).get("Time", {}).get("tick")
    if not isinstance(duration_tick, (int, float)) or duration_tick < 420:
        fail("runtime Fiddlesticks Crowstorm visual buff must persist for at least 420 ticks")
    storm_fields = [
        node
        for node in iter_mapping_nodes(champion.get("ult", {}))
        if node.get("type") == "RangePeriodProjectile"
        and node.get("name") == "test_mod_fiddlesticks_crowstorm"
    ]
    if len(storm_fields) != 1:
        fail("runtime Fiddlesticks Crowstorm must create exactly one persistent landing field")
    storm_field = storm_fields[0]
    storm_radius = storm_field.get("shape", {}).get("Circle", {}).get("radius")
    storm_tick = storm_field.get("tick")
    storm_period = storm_field.get("period")
    if (
        not isinstance(storm_tick, (int, float))
        or storm_tick < 420
        or not isinstance(storm_period, (int, float))
        or storm_period > 30
        or storm_field.get("first_delay") != 0
        or not isinstance(storm_radius, (int, float))
        or storm_radius < 52000
        or storm_field.get("applied_target") != "EnemyWithoutTower"
    ):
        fail("runtime Fiddlesticks Crowstorm field must be a long, large ground AoE after the jump")
    fear_fields = [
        node
        for node in iter_mapping_nodes(champion.get("ult", {}))
        if node.get("type") == "RangeEffect"
        and node.get("target") == "EnemyChampion"
        and node.get("shape", {}).get("Circle", {}).get("radius", 0) >= 52000
        and any(isinstance(effect, dict) and effect.get("type") == "Fear" for effect in node.get("effects", []))
    ]
    if len(fear_fields) != 1:
        fail("runtime Fiddlesticks Crowstorm landing must fear enemy champions in the large landing circle")


def default_game_root() -> Path:
    if ROOT.parent.name.lower() == "github_publish":
        return ROOT.parent.parent
    return Path(r"D:\steam\steamapps\common\Teamfight Manager2")


def appdata_data_dir() -> Path:
    roaming = os.environ.get("APPDATA")
    if not roaming:
        fail("APPDATA is not set; cannot inspect Teamfight Manager 2 runtime database state")
    return Path(roaming) / "TeamSamoyed" / "TeamfightManager2" / "data"


def check_enabled_mod(game_root: Path) -> None:
    config_path = game_root / "config" / "game" / "mods.json"
    config = load_json(config_path)
    if not isinstance(config, dict):
        fail(f"{config_path} must contain a JSON object")
    enabled_mods = config.get("enabled_mods")
    if enabled_mods != [MOD_ID]:
        fail(f"{config_path} enabled_mods must be [{MOD_ID!r}], got {enabled_mods!r}")


def check_runtime_copy(game_root: Path) -> None:
    runtime_root = game_root / "mods" / MOD_ID
    if not runtime_root.is_dir():
        fail(f"installed runtime mod folder is missing: {runtime_root}")

    critical_files = [
        "mod.mod_info",
        "mod.override_info",
        "champion/aatrox.data_champion",
        "champion/blitzcrank.data_champion",
        "champion/darius.data_champion",
        "champion/kayn.data_champion",
        "champion/yasuo.data_champion",
        "champion/jinx.data_champion",
        "champion/thresh.data_champion",
        "champion/viktor.data_champion",
        "champion/fiddlesticks.data_champion",
        "champion/jhin.data_champion",
        "text/champion.i18n",
        "style/champion_view.champion_view",
        "aseprite_resources/champions/aatrox#sheet.png",
        "aseprite_resources/champions/aatrox#anim.fanim",
        "aseprite_resources/champions/blitzcrank#sheet.png",
        "aseprite_resources/champions/blitzcrank#anim.fanim",
        "aseprite_resources/effects/blitzcrank_attack_punch#sheet.png",
        "aseprite_resources/effects/blitzcrank_attack_punch#anim.fanim",
        "aseprite_resources/effects/blitzcrank_grab_hit#sheet.png",
        "aseprite_resources/effects/blitzcrank_grab_hit#anim.fanim",
        "aseprite_resources/effects/blitzcrank_mana_barrier#sheet.png",
        "aseprite_resources/effects/blitzcrank_mana_barrier#anim.fanim",
        "aseprite_resources/effects/blitzcrank_overdrive#sheet.png",
        "aseprite_resources/effects/blitzcrank_overdrive#anim.fanim",
        "aseprite_resources/effects/blitzcrank_power_fist_impact#sheet.png",
        "aseprite_resources/effects/blitzcrank_power_fist_impact#anim.fanim",
        "aseprite_resources/effects/blitzcrank_power_fist_ready#sheet.png",
        "aseprite_resources/effects/blitzcrank_power_fist_ready#anim.fanim",
        "aseprite_resources/effects/blitzcrank_punch_hit#sheet.png",
        "aseprite_resources/effects/blitzcrank_punch_hit#anim.fanim",
        "aseprite_resources/effects/blitzcrank_rocket_grab#sheet.png",
        "aseprite_resources/effects/blitzcrank_rocket_grab#anim.fanim",
        "aseprite_resources/effects/blitzcrank_static_field_cast#sheet.png",
        "aseprite_resources/effects/blitzcrank_static_field_cast#anim.fanim",
        "aseprite_resources/effects/blitzcrank_static_field_hit#sheet.png",
        "aseprite_resources/effects/blitzcrank_static_field_hit#anim.fanim",
        "aseprite_resources/effects/blitzcrank_static_field_linger#sheet.png",
        "aseprite_resources/effects/blitzcrank_static_field_linger#anim.fanim",
        "aseprite_resources/champions/darius#sheet.png",
        "aseprite_resources/champions/darius#anim.fanim",
        "aseprite_resources/effects/darius_attack_slash#sheet.png",
        "aseprite_resources/effects/darius_attack_slash#anim.fanim",
        "aseprite_resources/effects/darius_bleed_apply#sheet.png",
        "aseprite_resources/effects/darius_bleed_apply#anim.fanim",
        "aseprite_resources/effects/darius_noxian_might_aura#sheet.png",
        "aseprite_resources/effects/darius_noxian_might_aura#anim.fanim",
        "aseprite_resources/effects/darius_decimate#sheet.png",
        "aseprite_resources/effects/darius_decimate#anim.fanim",
        "aseprite_resources/effects/darius_decimate_heal#sheet.png",
        "aseprite_resources/effects/darius_decimate_heal#anim.fanim",
        "aseprite_resources/effects/darius_apprehend#sheet.png",
        "aseprite_resources/effects/darius_apprehend#anim.fanim",
        "aseprite_resources/effects/darius_crippling_strike#sheet.png",
        "aseprite_resources/effects/darius_crippling_strike#anim.fanim",
        "aseprite_resources/effects/darius_noxian_guillotine#sheet.png",
        "aseprite_resources/effects/darius_noxian_guillotine#anim.fanim",
        "aseprite_resources/effects/darius_noxian_guillotine_hit#sheet.png",
        "aseprite_resources/effects/darius_noxian_guillotine_hit#anim.fanim",
        "aseprite_resources/champions/kayn#sheet.png",
        "aseprite_resources/champions/kayn#anim.fanim",
        "aseprite_resources/champions/yasuo#sheet.png",
        "aseprite_resources/champions/yasuo#anim.fanim",
        "aseprite_resources/champions/jinx#sheet.png",
        "aseprite_resources/champions/jinx#anim.fanim",
        "aseprite_resources/champions/thresh#sheet.png",
        "aseprite_resources/champions/thresh#anim.fanim",
        "aseprite_resources/champions/viktor#sheet.png",
        "aseprite_resources/champions/viktor#anim.fanim",
        "aseprite_resources/champions/fiddlesticks#sheet.png",
        "aseprite_resources/champions/fiddlesticks#anim.fanim",
        "aseprite_resources/champions/jhin#sheet.png",
        "aseprite_resources/champions/jhin#anim.fanim",
        "aseprite_resources/effects/jhin_attack_shot#sheet.png",
        "aseprite_resources/effects/jhin_attack_shot#anim.fanim",
        "aseprite_resources/effects/jhin_attack_shot_4#sheet.png",
        "aseprite_resources/effects/jhin_attack_shot_4#anim.fanim",
        "aseprite_resources/effects/jhin_bullet_hit_small#sheet.png",
        "aseprite_resources/effects/jhin_bullet_hit_small#anim.fanim",
        "aseprite_resources/effects/jhin_fourth_shot_bloom#sheet.png",
        "aseprite_resources/effects/jhin_fourth_shot_bloom#anim.fanim",
        "aseprite_resources/effects/jhin_grenade#sheet.png",
        "aseprite_resources/effects/jhin_grenade#anim.fanim",
        "aseprite_resources/effects/jhin_deadly_flourish#sheet.png",
        "aseprite_resources/effects/jhin_deadly_flourish#anim.fanim",
        "aseprite_resources/effects/jhin_lotus_mark_apply#sheet.png",
        "aseprite_resources/effects/jhin_lotus_mark_apply#anim.fanim",
        "aseprite_resources/effects/jhin_lotus_trap_line#sheet.png",
        "aseprite_resources/effects/jhin_lotus_trap_line#anim.fanim",
        "aseprite_resources/effects/jhin_lotus_trap_bloom#sheet.png",
        "aseprite_resources/effects/jhin_lotus_trap_bloom#anim.fanim",
        "aseprite_resources/effects/jhin_deadly_flourish_root_bloom#sheet.png",
        "aseprite_resources/effects/jhin_deadly_flourish_root_bloom#anim.fanim",
        "aseprite_resources/effects/jhin_curtain_call_stage#sheet.png",
        "aseprite_resources/effects/jhin_curtain_call_stage#anim.fanim",
        "aseprite_resources/effects/jhin_curtain_call_shot#sheet.png",
        "aseprite_resources/effects/jhin_curtain_call_shot#anim.fanim",
        "aseprite_resources/effects/jhin_curtain_call_shot_4#sheet.png",
        "aseprite_resources/effects/jhin_curtain_call_shot_4#anim.fanim",
        "aseprite_resources/effects/jhin_curtain_call_hit_bloom#sheet.png",
        "aseprite_resources/effects/jhin_curtain_call_hit_bloom#anim.fanim",
        "aseprite_resources/effects/jhin_finale_bloom#sheet.png",
        "aseprite_resources/effects/jhin_finale_bloom#anim.fanim",
        "aseprite_resources/effects/jhin_fourth_shot_ready#sheet.png",
        "aseprite_resources/effects/jhin_fourth_shot_ready#anim.fanim",
        "aseprite_resources/effects/jhin_reload_circle#sheet.png",
        "aseprite_resources/effects/jhin_reload_circle#anim.fanim",
        "aseprite_resources/effects/kayn_q_slash#sheet.png",
        "aseprite_resources/effects/kayn_q_slash#anim.fanim",
        "aseprite_resources/effects/kayn_w_blade_reach#sheet.png",
        "aseprite_resources/effects/kayn_w_blade_reach#anim.fanim",
        "aseprite_resources/effects/kayn_r_entry#sheet.png",
        "aseprite_resources/effects/kayn_r_entry#anim.fanim",
        "aseprite_resources/effects/kayn_r_exit#sheet.png",
        "aseprite_resources/effects/kayn_r_exit#anim.fanim",
        "aseprite_resources/effects/kayn_darkin_aura#sheet.png",
        "aseprite_resources/effects/kayn_darkin_aura#anim.fanim",
        "aseprite_resources/effects/yasuo_attack_slash#sheet.png",
        "aseprite_resources/effects/yasuo_attack_slash#anim.fanim",
        "aseprite_resources/effects/yasuo_q_stab#sheet.png",
        "aseprite_resources/effects/yasuo_q_stab#anim.fanim",
        "aseprite_resources/effects/yasuo_q_tornado#sheet.png",
        "aseprite_resources/effects/yasuo_q_tornado#anim.fanim",
        "aseprite_resources/effects/yasuo_sweeping_blade#sheet.png",
        "aseprite_resources/effects/yasuo_sweeping_blade#anim.fanim",
        "aseprite_resources/effects/yasuo_wind_wall#sheet.png",
        "aseprite_resources/effects/yasuo_wind_wall#anim.fanim",
        "aseprite_resources/effects/yasuo_last_breath#sheet.png",
        "aseprite_resources/effects/yasuo_last_breath#anim.fanim",
        "aseprite_resources/effects/yasuo_flow_shield#sheet.png",
        "aseprite_resources/effects/yasuo_flow_shield#anim.fanim",
        "aseprite_resources/effects/yasuo_after_breath_aura#sheet.png",
        "aseprite_resources/effects/yasuo_after_breath_aura#anim.fanim",
        "aseprite_resources/effects/jinx_minigun_bullet#sheet.png",
        "aseprite_resources/effects/jinx_minigun_bullet#anim.fanim",
        "aseprite_resources/effects/jinx_rocket_attack#sheet.png",
        "aseprite_resources/effects/jinx_rocket_attack#anim.fanim",
        "aseprite_resources/effects/jinx_zap#sheet.png",
        "aseprite_resources/effects/jinx_zap#anim.fanim",
        "aseprite_resources/effects/jinx_flame_chompers#sheet.png",
        "aseprite_resources/effects/jinx_flame_chompers#anim.fanim",
        "aseprite_resources/effects/jinx_super_mega_death_rocket#sheet.png",
        "aseprite_resources/effects/jinx_super_mega_death_rocket#anim.fanim",
        "aseprite_resources/effects/jinx_switcheroo#sheet.png",
        "aseprite_resources/effects/jinx_switcheroo#anim.fanim",
        "aseprite_resources/effects/jinx_rocket_explosion#sheet.png",
        "aseprite_resources/effects/jinx_rocket_explosion#anim.fanim",
        "aseprite_resources/effects/kayn_attack_slash#sheet.png",
        "aseprite_resources/effects/kayn_attack_slash#anim.fanim",
        "aseprite_resources/effects/thresh_attack_chain#sheet.png",
        "aseprite_resources/effects/thresh_attack_chain#anim.fanim",
        "aseprite_resources/effects/thresh_attack_empowered#sheet.png",
        "aseprite_resources/effects/thresh_attack_empowered#anim.fanim",
        "aseprite_resources/effects/thresh_death_sentence_chain#sheet.png",
        "aseprite_resources/effects/thresh_death_sentence_chain#anim.fanim",
        "aseprite_resources/effects/thresh_death_sentence_hit#sheet.png",
        "aseprite_resources/effects/thresh_death_sentence_hit#anim.fanim",
        "aseprite_resources/effects/thresh_lantern#sheet.png",
        "aseprite_resources/effects/thresh_lantern#anim.fanim",
        "aseprite_resources/effects/thresh_flay_sweep#sheet.png",
        "aseprite_resources/effects/thresh_flay_sweep#anim.fanim",
        "aseprite_resources/effects/thresh_box#sheet.png",
        "aseprite_resources/effects/thresh_box#anim.fanim",
        "aseprite_resources/effects/thresh_soul_stack#sheet.png",
        "aseprite_resources/effects/thresh_soul_stack#anim.fanim",
        "aseprite_resources/effects/viktor_attack_projectile#sheet.png",
        "aseprite_resources/effects/viktor_attack_projectile#anim.fanim",
        "aseprite_resources/effects/viktor_laser#sheet.png",
        "aseprite_resources/effects/viktor_laser#anim.fanim",
        "aseprite_resources/effects/viktor_laser_aftershock#sheet.png",
        "aseprite_resources/effects/viktor_laser_aftershock#anim.fanim",
        "aseprite_resources/effects/viktor_siphon_projectile#sheet.png",
        "aseprite_resources/effects/viktor_siphon_projectile#anim.fanim",
        "aseprite_resources/effects/viktor_siphon_impact#sheet.png",
        "aseprite_resources/effects/viktor_siphon_impact#anim.fanim",
        "aseprite_resources/effects/viktor_gravity_field#sheet.png",
        "aseprite_resources/effects/viktor_gravity_field#anim.fanim",
        "aseprite_resources/effects/viktor_chaos_storm#sheet.png",
        "aseprite_resources/effects/viktor_chaos_storm#anim.fanim",
        "aseprite_resources/effects/viktor_siphon_shield#sheet.png",
        "aseprite_resources/effects/viktor_siphon_shield#anim.fanim",
        "aseprite_resources/effects/viktor_evolution_aura#sheet.png",
        "aseprite_resources/effects/viktor_evolution_aura#anim.fanim",
        "aseprite_resources/effects/viktor_storm_impact#sheet.png",
        "aseprite_resources/effects/viktor_storm_impact#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_attack_projectile#sheet.png",
        "aseprite_resources/effects/fiddlesticks_attack_projectile#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_fear_projectile#sheet.png",
        "aseprite_resources/effects/fiddlesticks_fear_projectile#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_fear_mark#sheet.png",
        "aseprite_resources/effects/fiddlesticks_fear_mark#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_drain#sheet.png",
        "aseprite_resources/effects/fiddlesticks_drain#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_drain_tether#sheet.png",
        "aseprite_resources/effects/fiddlesticks_drain_tether#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_crowstorm#sheet.png",
        "aseprite_resources/effects/fiddlesticks_crowstorm#anim.fanim",
        "aseprite_resources/effects/fiddlesticks_crowstorm_channel#sheet.png",
        "aseprite_resources/effects/fiddlesticks_crowstorm_channel#anim.fanim",
        "icons/fiddlesticks_skill.png",
        "icons/fiddlesticks_skill2.png",
        "icons/fiddlesticks_ult.png",
        "icons/blitzcrank_skill.png",
        "icons/blitzcrank_skill2.png",
        "icons/blitzcrank_ult.png",
        "icons/kayn_skill.png",
        "icons/kayn_skill2.png",
        "icons/kayn_ult.png",
        "icons/darius_skill.png",
        "icons/darius_skill2.png",
        "icons/darius_ult.png",
        "icons/yasuo_skill.png",
        "icons/yasuo_skill2.png",
        "icons/yasuo_ult.png",
        "icons/jinx_skill.png",
        "icons/jinx_skill2.png",
        "icons/jinx_ult.png",
        "icons/thresh_skill.png",
        "icons/thresh_skill2.png",
        "icons/thresh_ult.png",
        "icons/viktor_skill.png",
        "icons/viktor_skill2.png",
        "icons/viktor_ult.png",
        "icons/jhin_skill.png",
        "icons/jhin_skill2.png",
        "icons/jhin_ult.png",
        "qa/aatrox_official_audio_sources.json",
        "qa/darius_official_audio_sources.json",
        "qa/kayn_official_audio_sources.json",
        "qa/yasuo_official_audio_sources.json",
        "qa/jinx_official_audio_sources.json",
        "qa/thresh_official_audio_sources.json",
        "qa/viktor_official_audio_sources.json",
        "qa/jhin_imagegen_vgu.md",
        "qa/roster_visibility_coverage.json",
    ]
    for event_name in AATROX_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        if event_name == "test_mod_aatrox_dash_cast":
            critical_files.append("sound/sfx/test_mod_aatrox_dash_voice_clip.wav")
            critical_files.append("sound/sfx/test_mod_aatrox_dash_effect_clip.wav")
        else:
            critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in BLITZCRANK_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in DARIUS_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in KAYN_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in YASUO_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in JINX_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in THRESH_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in VIKTOR_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for relative in critical_files:
        repo_file = ROOT / relative
        runtime_file = runtime_root / relative
        if not runtime_file.is_file():
            fail(f"runtime mod is missing {runtime_file}")
        if sha256(repo_file) != sha256(runtime_file):
            fail(f"runtime mod file is stale or differs from repo: {runtime_file}")

    check_aatrox_basic_attack_motion(runtime_root)
    check_jhin_upright_run_pose(runtime_root)

    for relative in (
        "aseprite_resources/effects/jinx_get_excited_aura#sheet.png",
        "aseprite_resources/effects/jinx_get_excited_aura#anim.fanim",
        "aseprite_resources/effects/jinx_fishbones_mode_aura#sheet.png",
        "aseprite_resources/effects/jinx_fishbones_mode_aura#anim.fanim",
    ):
        if (runtime_root / relative).exists():
            fail(f"runtime mod still contains retired actor-attached Jinx VFX: {runtime_root / relative}")

    for data_path in sorted((runtime_root / "champion").glob("*.data_champion")):
        data = load_json(data_path)
        check_view_effect_types(data_path, data)
        assert_no_negative_speed_fields(data, str(data_path))
        check_darius_ult_visibility(data_path, data)
        check_viktor_ground_vfx(data_path, data)
        check_thresh_ult_visibility(data_path, data)
        check_fiddlesticks_ult_visibility(data_path, data)

    style = load_json(runtime_root / "style" / "champion_view.champion_view")
    if not isinstance(style, dict):
        fail("runtime champion_view must contain a JSON object")
    entries = style.get("entries")
    if not isinstance(entries, dict):
        fail("runtime champion_view missing entries object")
    for champion_id in CHAMPION_IDS:
        if champion_id not in entries:
            fail(f"runtime champion_view missing entries.{champion_id}")
    for champion_id, expected_face in SIDE_CARD_STANDING_FACE_OFFSETS.items():
        view = entries.get(champion_id)
        if not isinstance(view, dict):
            fail(f"runtime champion_view missing entries.{champion_id}")
        face = view.get("face")
        if not isinstance(face, dict):
            fail(f"runtime champion_view entries.{champion_id}.face must be an object")
        if face.get("x") != expected_face["x"] or face.get("y") != expected_face["y"]:
            fail(
                f"runtime champion_view entries.{champion_id}.face must be {expected_face} "
                "so compact HUD/scoreboard portraits stay aligned"
            )
    for champion_id, expected_center in SIDE_CARD_STANDING_CENTER_OFFSETS.items():
        view = entries.get(champion_id)
        if not isinstance(view, dict):
            fail(f"runtime champion_view missing entries.{champion_id}")
        center = view.get("center")
        if not isinstance(center, dict):
            fail(f"runtime champion_view entries.{champion_id}.center must be an object")
        if center.get("x") != expected_center["x"] or center.get("y") != expected_center["y"]:
            fail(
                f"runtime champion_view entries.{champion_id}.center must be {expected_center} "
                "so exchange standing cards show feet and weapons"
            )

    text = load_json(runtime_root / "text" / "champion.i18n")
    if not isinstance(text, dict):
        fail("runtime champion text must contain a JSON object")
    for locale, payload in text.items():
        descriptions = payload.get("description") if isinstance(payload, dict) else None
        if not isinstance(descriptions, dict):
            fail(f"runtime text locale {locale} missing description object")
        for champion_id in CHAMPION_IDS:
            if champion_id not in descriptions:
                fail(f"runtime text locale {locale} missing description.{champion_id}")
            row = descriptions[champion_id]
            if locale in {"zh-hans", "zh-hant"}:
                payload_text = json.dumps(row, ensure_ascii=False)
                if "??" in payload_text:
                    fail(f"runtime text locale {locale} description.{champion_id} still contains corrupted question marks")
                expected_display_names = {
                    f"{MOD_ID}_blitzcrank": {
                        "zh-hans": "\u84b8\u6c7d\u673a\u5668\u4eba",
                        "zh-hant": "\u84b8\u6c7d\u6a5f\u5668\u4eba",
                    },
                    f"{MOD_ID}_darius": {
                        "zh-hans": "诺克萨斯之手",
                        "zh-hant": "諾克薩斯之手",
                    },
                    f"{MOD_ID}_kayn": {
                        "zh-hans": "影流之镰",
                        "zh-hant": "影流之鐮",
                    },
                    f"{MOD_ID}_yasuo": {
                        "zh-hans": "疾风剑豪",
                        "zh-hant": "疾風劍豪",
                    },
                    f"{MOD_ID}_jinx": {
                        "zh-hans": "暴走萝莉",
                        "zh-hant": "暴走蘿莉",
                    },
                    f"{MOD_ID}_thresh": {
                        "zh-hans": "锤石",
                        "zh-hant": "瑟雷西",
                    },
                    f"{MOD_ID}_viktor": {
                        "zh-hans": "维克托",
                        "zh-hant": "維克特",
                    },
                }
                display_by_locale = expected_display_names.get(champion_id)
                if display_by_locale:
                    expected_name = display_by_locale[locale]
                    actual_name = str(row.get("name", ""))
                    if actual_name != expected_name:
                        fail(
                            f"runtime text locale {locale} description.{champion_id}.name "
                            f"must be short display name {expected_name!r}, got {actual_name!r}"
                        )
                    forbidden_aliases = (
                        "Kayn",
                        "Yasuo",
                        "Jinx",
                        "Thresh",
                        "Viktor",
                        "Blitzcrank",
                        "Darius",
                        "诺手",
                        "諾手",
                        "凯隐",
                        "慨影",
                        "亚索",
                        "犽宿",
                        "金克丝",
                        "金克絲",
                        "奥术先驱",
                        "奧術先驅",
                    )
                    if any(alias in actual_name for alias in forbidden_aliases):
                        fail(f"runtime text locale {locale} description.{champion_id}.name contains search alias")
                required_terms_by_champion = {
                    f"{MOD_ID}_darius": {
                        "zh-hans": ("诺克萨斯之手", "诺手", "Darius", "出血", "大杀四方", "无情铁手", "致残打击", "诺克萨斯断头台"),
                        "zh-hant": ("諾克薩斯之手", "諾手", "Darius", "出血", "大殺四方", "無情鐵手", "致殘打擊", "諾克薩斯斷頭台"),
                    },
                    f"{MOD_ID}_kayn": {
                        "zh-hans": ("凯隐", "影流之镰", "巨镰横扫", "利刃纵贯", "裂舍影"),
                        "zh-hant": ("慨影", "影流之鐮", "巨鐮橫掃", "利刃縱貫", "裂舍影"),
                    },
                    f"{MOD_ID}_yasuo": {
                        "zh-hans": ("亚索", "疾风剑豪", "斩钢闪", "踏前斩", "狂风绝息斩"),
                        "zh-hant": ("犽宿", "疾風劍豪", "斬鋼閃", "風牆", "奪命氣息"),
                    },
                    f"{MOD_ID}_jinx": {
                        "zh-hans": ("暴走萝莉", "砰砰枪", "鱼骨头", "枪炮交响曲", "嚼火者", "超究极死神飞弹"),
                        "zh-hant": ("暴走蘿莉", "砰砰槍", "魚骨頭", "槍炮交響曲", "嚼火者", "超究極死神飛彈"),
                    },
                    f"{MOD_ID}_thresh": {
                        "zh-hans": ("锤石", "魂锁典狱长", "死亡判决", "魂引之灯", "厄运钟摆", "幽冥监牢"),
                        "zh-hant": ("瑟雷西", "魂鎖典獄長", "死亡判決", "冥燈引路", "厄運鐘擺", "幽冥監牢"),
                    },
                    f"{MOD_ID}_viktor": {
                        "zh-hans": ("维克托", "奥术先驱", "机械先驱", "光荣进化", "海克斯射线", "重力场", "奥术风暴"),
                        "zh-hant": ("維克特", "奧術先驅", "機械先驅", "光榮進化", "海克斯射線", "重力場", "奧術風暴"),
                    },
                }
                required_by_locale = required_terms_by_champion.get(champion_id)
                if required_by_locale:
                    required_terms = required_by_locale[locale]
                    missing = [term for term in required_terms if term not in payload_text]
                    if missing:
                        fail(f"runtime text locale {locale} description.{champion_id} missing search aliases {missing}")
    check_encyclopedia_search_terms(text)


def check_encyclopedia_search_terms(text: object) -> None:
    if not isinstance(text, dict):
        fail("runtime champion text must contain a JSON object")
    for champion_id, terms_by_locale in REQUIRED_ENCYCLOPEDIA_NAME_TERMS.items():
        for locale, required_terms in terms_by_locale.items():
            payload = text.get(locale)
            descriptions = payload.get("description") if isinstance(payload, dict) else None
            if not isinstance(descriptions, dict):
                fail(f"runtime text locale {locale} missing description object")
            row = descriptions.get(champion_id)
            if not isinstance(row, dict):
                fail(f"runtime text locale {locale} missing description.{champion_id}")
            name = str(row.get("name", ""))
            missing = [term for term in required_terms if term not in name]
            if missing:
                fail(
                    f"runtime text locale {locale} description.{champion_id}.name "
                    f"is missing encyclopedia name search terms {missing}"
                )
    for champion_id, terms_by_locale in REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS.items():
        for locale, required_terms in terms_by_locale.items():
            payload = text.get(locale)
            descriptions = payload.get("description") if isinstance(payload, dict) else None
            if not isinstance(descriptions, dict):
                fail(f"runtime text locale {locale} missing description object")
            row = descriptions.get(champion_id)
            if not isinstance(row, dict):
                fail(f"runtime text locale {locale} missing description.{champion_id}")
            surface = " ".join(str(row.get(key, "")) for key in REQUIRED_DESCRIPTION_KEYS).casefold()
            missing = [term for term in required_terms if term.casefold() not in surface]
            if missing:
                fail(
                    f"runtime text locale {locale} description.{champion_id} "
                    f"is missing encyclopedia search terms {missing}"
                )


def check_custom_database_state() -> None:
    data_dir = appdata_data_dir()
    flag = data_dir / "custom_db_enabled.flag"
    custom_db = data_dir / "custom_database.tfm2db"
    if not custom_db.exists():
        return

    payload = custom_db.read_bytes()
    missing = [champion_id for champion_id in CHAMPION_IDS if champion_id.encode("utf-8") not in payload]
    if missing:
        state = "enabled" if flag.exists() else "present"
        fail(
            f"custom_database.tfm2db is {state} but does not contain {missing}; "
            "archive or regenerate the stale custom database before judging encyclopedia visibility"
        )


def check_latest_startup_log() -> None:
    log_path = appdata_data_dir() / "log.log"
    if not log_path.exists():
        return

    text = log_path.read_text(encoding="utf-8", errors="replace")
    marker = "game start.."
    latest_startup = text.rsplit(marker, 1)[-1] if marker in text else text
    if "data_champion load error" in latest_startup:
        fail(
            "latest startup log contains data_champion load error; "
            "fix runtime registration before judging encyclopedia visibility"
        )


def main() -> int:
    game_root = Path(os.environ.get("TFM2_GAME_ROOT", default_game_root()))
    try:
        check_enabled_mod(game_root)
        check_runtime_copy(game_root)
        check_custom_database_state()
        check_latest_startup_log()
    except AssertionError as exc:
        print(f"local_runtime_encyclopedia_check=fail: {exc}", file=sys.stderr)
        return 1
    print("local_runtime_encyclopedia_check=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
