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


def main() -> int:
    try:
        check_mod_metadata()
        check_champion_visibility()
    except AssertionError as exc:
        print(f"encyclopedia_visibility_check=fail: {exc}", file=sys.stderr)
        return 1
    print("encyclopedia_visibility_check=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
