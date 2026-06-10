from __future__ import annotations

import hashlib
import json
import os
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MOD_ID = "bo_league_champions"
CHAMPION_IDS = (
    f"{MOD_ID}_aatrox",
    f"{MOD_ID}_kayn",
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
)


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

    critical_files = [
        "mod.mod_info",
        "mod.override_info",
        "champion/aatrox.data_champion",
        "champion/kayn.data_champion",
        "text/champion.i18n",
        "style/champion_view.champion_view",
        "aseprite_resources/champions/aatrox#sheet.png",
        "aseprite_resources/champions/aatrox#anim.fanim",
        "aseprite_resources/champions/kayn#sheet.png",
        "aseprite_resources/champions/kayn#anim.fanim",
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
        "icons/kayn_skill.png",
        "icons/kayn_skill2.png",
        "icons/kayn_ult.png",
        "qa/kayn_official_audio_sources.json",
    ]
    for event_name in KAYN_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
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
    if not isinstance(entries, dict):
        fail("runtime champion_view missing entries object")
    for champion_id in CHAMPION_IDS:
        if champion_id not in entries:
            fail(f"runtime champion_view missing entries.{champion_id}")

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
            if champion_id.endswith("_kayn") and locale in {"zh-hans", "zh-hant"}:
                payload_text = json.dumps(row, ensure_ascii=False)
                if "??" in payload_text:
                    fail(f"runtime text locale {locale} description.{champion_id} still contains corrupted question marks")


def check_custom_database_state() -> None:
    data_dir = appdata_data_dir()
    flag = data_dir / "custom_db_enabled.flag"
    custom_db = data_dir / "custom_database.tfm2db"
    if not flag.exists():
        return
    if not custom_db.exists():
        fail(f"{flag} exists but {custom_db} is missing")

    payload = custom_db.read_bytes()
    missing = [champion_id for champion_id in CHAMPION_IDS if champion_id.encode("utf-8") not in payload]
    if missing:
        fail(
            "custom_database.tfm2db is enabled but does not contain "
            f"{missing}; disable or regenerate the stale custom database before judging encyclopedia visibility"
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
