from __future__ import annotations

import json
import sys
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


def fail(message: str) -> None:
    raise AssertionError(message)


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # pragma: no cover - failure path prints file context
        raise AssertionError(f"{path.relative_to(ROOT)} is not valid JSON: {exc}") from exc


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
        "zh-hans": ("\u5251\u9b54", "\u4e9a\u6258\u514b\u65af"),
        "zh-hant": ("\u528d\u9b54", "\u4e9e\u6258\u514b\u65af"),
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
                        f"must include {expected_name_term!r} for encyclopedia search"
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
        face_y = view.get("face", {}).get("y")
        center_y = view.get("center", {}).get("y")
        if not isinstance(face_y, (int, float)) or face_y > -30:
            fail(f"style entry {aatrox_id}.face.y must keep the portrait focused on the head/torso")
        if not isinstance(center_y, (int, float)) or not -20 <= center_y <= -8:
            fail(f"style entry {aatrox_id}.center.y must keep the full-body display centered")

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "aatrox#anim.fanim")
    idle_frames = fanim.get("anims", {}).get("idle", {}).get("frames")
    if not isinstance(idle_frames, list) or len(idle_frames) < 6:
        fail("Aatrox idle animation must have at least six stable display frames")
    for index, frame in enumerate(idle_frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict):
            fail(f"Aatrox idle frame {index} missing frame data")
        if data.get("w") != 54.0 or data.get("h") != 50.0:
            fail(f"Aatrox idle frame {index} must use the Viktor-like 54x50 display frame")

    aatrox = load_json(ROOT / "champion" / "aatrox.data_champion")
    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in aatrox.get("view_projectiles", [])}
    for name, expected in AATROX_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/aatrox.data_champion projectile {name} must reference {expected}")
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
    check_aatrox_rework_contract(text, entries)


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
