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
    "kayn",
    "vayne",
    "veigar",
    "viktor",
}
REQUIRED_DESCRIPTION_KEYS = ("name", "attack", "skill", "skill2", "ult")
PROCESS_IMAGE_ROOTS = ("source", "qa")
PROCESS_IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".webp"}
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
AATROX_MIN_BOTTOM_SAFE_PIXELS = 16
AATROX_MAX_CORE_BODY_HEIGHT = 36
AATROX_MIN_RUN_FOOT_CENTER_RANGE = 0.9
AATROX_MIN_RUN_FOOT_SHAPES = 5
AATROX_MIN_RUN_FOOT_PIXELS = 24
AATROX_MIN_RUN_LOWER_PIXELS = 40
AATROX_ACCEPTED_MODEL_FRAME_X = 4224
AATROX_IDLE_FRAME_XS = (AATROX_ACCEPTED_MODEL_FRAME_X,) * 9
AATROX_RETIRED_MODEL_FRAME_XS = (5868, 5964, 6060, 6156, 6252, 6348, 6444, 6540, 6636)
AATROX_ATTACK_FRAME_XS = (4992, 5088, 5184, 5280, 5376, 5472, 5568, 5664, 5760)
AATROX_SKILL_FRAME_XS = (2784, 2880, 2976, 3072, 3168, 3264, 3360, 3456)
AATROX_SKILL2_FRAME_XS = (3552, 3648, 3744, 3840, 3936, 4032, 4128)
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
}
KAYN_SKILL_SOUND_EVENTS = {
    "test_mod_kayn_q_cast",
    "test_mod_kayn_q_hit",
    "test_mod_kayn_w_cast",
    "test_mod_kayn_w_hit",
    "test_mod_kayn_r_cast",
    "test_mod_kayn_r_hit",
}
KAYN_SKILL_SOUND_VOLUME_FLOOR = 0.72
KAYN_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
KAYN_FRAME_SIZE = (57.0, 54.0)


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


def local_asset_path(asset: str) -> Path:
    prefix = f"asset/{MOD_ID}/"
    if not asset.startswith(prefix):
        fail(f"asset path must use {prefix}: {asset}")
    return ROOT / asset[len(prefix) :]


def require_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")


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
        if face_x != 0 or face_y != -34:
            fail(f"style entry {aatrox_id}.face must keep Aatrox's compact portrait at x=0,y=-34")
        if center_y != -12:
            fail(f"style entry {aatrox_id}.center.y must keep Aatrox full-body display at -12")

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "aatrox#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "aatrox#sheet.png"
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
        "attack": AATROX_ATTACK_FRAME_XS,
        "skill": AATROX_SKILL_FRAME_XS,
        "skill2": AATROX_SKILL2_FRAME_XS,
        "hit": (AATROX_ACCEPTED_MODEL_FRAME_X,),
        "dead": (AATROX_ACCEPTED_MODEL_FRAME_X,),
        "ult": (AATROX_ACCEPTED_MODEL_FRAME_X,),
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
            if body_height > AATROX_MAX_CORE_BODY_HEIGHT:
                fail(
                    f"Aatrox {action} frame {index} body height {body_height}px exceeds "
                    f"{AATROX_MAX_CORE_BODY_HEIGHT}px, causing model-size jumps"
                )
            if bottom_safe < AATROX_MIN_BOTTOM_SAFE_PIXELS:
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
        heights = [bbox[3] - bbox[1] for bbox in action_bboxes[action]]
        if min(widths) + 6 < min(run_widths):
            fail(f"Aatrox {action} must keep the accepted compact run/body posture instead of swapping model")
        if max(abs(height - run_heights[0]) for height in heights) > 2:
            fail(f"Aatrox {action} model height must stay locked to the compact run scale")
        if len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Aatrox {action} must have visible body/weapon motion, not repeated static frames")
        if tuple(action_hashes[action][: len(action_hashes["run"])]) == tuple(action_hashes["run"][: len(action_hashes[action])]):
            fail(f"Aatrox {action} must not be a direct copy of the run cycle")
    for action in ("idle", "hit", "dead", "ult"):
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
    for name, expected in AATROX_Q_CAST_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/aatrox.data_champion view_effect {name} must reference {expected}")
    skill_effects = aatrox.get("skill", {}).get("effect", {}).get("effects", [])
    if not isinstance(skill_effects, list):
        fail("Aatrox Q skill must use a Combine effects list")
    if not any(item.get("type") == "CasterViewEffect" and item.get("name") == "test_mod_aatrox_q1_cast_vfx" for item in skill_effects if isinstance(item, dict)):
        fail("Aatrox Q1 must have an immediate visible caster-follow effect")
    delayed = {item.get("tick"): item.get("effects", []) for item in skill_effects if isinstance(item, dict) and item.get("type") == "Delayed"}
    for tick, name in ((18, "test_mod_aatrox_q2_cast_vfx"), (38, "test_mod_aatrox_q3_cast_vfx")):
        effects = delayed.get(tick)
        if not isinstance(effects, list) or not any(
            item.get("type") == "CasterViewEffect" and item.get("name") == name for item in effects if isinstance(item, dict)
        ):
            fail(f"Aatrox delayed Q at tick {tick} must have visible effect {name}")
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


def check_kayn_rework_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_names = {
        "en": ("Kayn",),
        "zh-hans": ("\u51ef\u9690",),
        "zh-hant": ("\u6168\u5f71",),
    }
    expected_terms = {
        "zh-hans": ("\u5de8\u9570\u6a2a\u626b", "\u5229\u5203\u7eb5\u8d2f", "\u88c2\u820d\u5f71", "\u6697\u88d4\u5347\u534e"),
        "zh-hant": ("\u5de8\u9430\u6a6b\u6383", "\u5229\u5203\u7e31\u8cab", "\u88c2\u820d\u5f71", "\u51a5\u8840\u5347\u83ef"),
    }
    for locale, expected_name_terms in expected_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for kayn_id in KAYN_IDS:
            row = descriptions.get(kayn_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {kayn_id}")
            name = str(row.get("name", ""))
            for expected_name_term in expected_name_terms:
                if expected_name_term not in name:
                    fail(f"text/champion.i18n locale {locale} {kayn_id}.name must include {expected_name_term!r}")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "・ｽ" in value:
                    fail(f"text/champion.i18n locale {locale} {kayn_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("skill", "skill2", "ult")):
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
    check_aatrox_rework_contract(text, entries)
    check_kayn_rework_contract(text, entries)


def main() -> int:
    try:
        check_mod_metadata()
        check_no_process_images()
        check_champion_visibility()
    except AssertionError as exc:
        print(f"encyclopedia_visibility_check=fail: {exc}", file=sys.stderr)
        return 1
    print("encyclopedia_visibility_check=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
