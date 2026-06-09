from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD_ID = "bo_league_champions"
CHAMPION_ID = f"{MOD_ID}_aatrox"


def fail(message: str) -> None:
    raise AssertionError(message)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8-sig"))
    except Exception as exc:  # pragma: no cover - used as a local QA script.
        raise AssertionError(f"{path} is not valid JSON: {exc}") from exc


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

    critical_files = (
        "mod.mod_info",
        "mod.override_info",
        "champion/aatrox.data_champion",
        "text/champion.i18n",
        "style/champion_view.champion_view",
    )
    for relative in critical_files:
        repo_file = ROOT / relative
        runtime_file = runtime_root / relative
        if not runtime_file.is_file():
            fail(f"runtime mod is missing {runtime_file}")
        if sha256(repo_file) != sha256(runtime_file):
            fail(f"runtime mod file is stale or differs from repo: {runtime_file}")

    style = load_json(runtime_root / "style" / "champion_view.champion_view")
    if not isinstance(style, dict):
        fail("runtime champion_view must contain a JSON object")
    entries = style.get("entries")
    if not isinstance(entries, dict) or CHAMPION_ID not in entries:
        fail(f"runtime champion_view missing entries.{CHAMPION_ID}")

    text = load_json(runtime_root / "text" / "champion.i18n")
    if not isinstance(text, dict):
        fail("runtime champion text must contain a JSON object")
    for locale, payload in text.items():
        descriptions = payload.get("description") if isinstance(payload, dict) else None
        if not isinstance(descriptions, dict) or CHAMPION_ID not in descriptions:
            fail(f"runtime text locale {locale} missing description.{CHAMPION_ID}")


def check_custom_database_state() -> None:
    data_dir = appdata_data_dir()
    flag = data_dir / "custom_db_enabled.flag"
    custom_db = data_dir / "custom_database.tfm2db"
    if not flag.exists():
        return
    if not custom_db.exists():
        fail(f"{flag} exists but {custom_db} is missing")

    payload = custom_db.read_bytes()
    needle = CHAMPION_ID.encode("utf-8")
    if needle not in payload:
        fail(
            "custom_database.tfm2db is enabled but does not contain "
            f"{CHAMPION_ID}; disable or regenerate the stale custom database before judging encyclopedia visibility"
        )


def main() -> int:
    game_root = Path(os.environ.get("TFM2_GAME_ROOT", default_game_root()))
    try:
        check_enabled_mod(game_root)
        check_runtime_copy(game_root)
        check_custom_database_state()
    except AssertionError as exc:
        print(f"local_runtime_encyclopedia_check=fail: {exc}", file=sys.stderr)
        return 1
    print("local_runtime_encyclopedia_check=ok")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
