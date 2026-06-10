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
    f"{MOD_ID}_yasuo",
)
AATROX_SOUND_EVENTS = (
    "test_mod_aatrox_attack_cast",
    "test_mod_aatrox_attack_hit",
    "test_mod_aatrox_cleave_cast",
    "test_mod_aatrox_cleave_hit",
    "test_mod_aatrox_dash_cast",
    "test_mod_aatrox_ult_cast",
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
        "champion/yasuo.data_champion",
        "text/champion.i18n",
        "style/champion_view.champion_view",
        "aseprite_resources/champions/aatrox#sheet.png",
        "aseprite_resources/champions/aatrox#anim.fanim",
        "aseprite_resources/champions/kayn#sheet.png",
        "aseprite_resources/champions/kayn#anim.fanim",
        "aseprite_resources/champions/yasuo#sheet.png",
        "aseprite_resources/champions/yasuo#anim.fanim",
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
        "icons/kayn_skill.png",
        "icons/kayn_skill2.png",
        "icons/kayn_ult.png",
        "icons/yasuo_skill.png",
        "icons/yasuo_skill2.png",
        "icons/yasuo_ult.png",
        "qa/aatrox_official_audio_sources.json",
        "qa/kayn_official_audio_sources.json",
        "qa/yasuo_official_audio_sources.json",
    ]
    for event_name in AATROX_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        if event_name == "test_mod_aatrox_dash_cast":
            critical_files.append("sound/sfx/test_mod_aatrox_dash_voice_clip.wav")
            critical_files.append("sound/sfx/test_mod_aatrox_dash_effect_clip.wav")
        else:
            critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in KAYN_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        critical_files.append(f"sound/sfx/{event_name}_clip.wav")
    for event_name in YASUO_SOUND_EVENTS:
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
            if locale in {"zh-hans", "zh-hant"}:
                payload_text = json.dumps(row, ensure_ascii=False)
                if "??" in payload_text:
                    fail(f"runtime text locale {locale} description.{champion_id} still contains corrupted question marks")
                expected_display_names = {
                    f"{MOD_ID}_kayn": {
                        "zh-hans": "影流之镰",
                        "zh-hant": "影流之鐮",
                    },
                    f"{MOD_ID}_yasuo": {
                        "zh-hans": "疾风剑豪",
                        "zh-hant": "疾風劍豪",
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
                    forbidden_aliases = ("Kayn", "Yasuo", "凯隐", "慨影", "亚索", "犽宿")
                    if any(alias in actual_name for alias in forbidden_aliases):
                        fail(f"runtime text locale {locale} description.{champion_id}.name contains search alias")
                required_terms_by_champion = {
                    f"{MOD_ID}_kayn": {
                        "zh-hans": ("凯隐", "影流之镰", "巨镰横扫", "利刃纵贯", "裂舍影"),
                        "zh-hant": ("慨影", "影流之鐮", "巨鐮橫掃", "利刃縱貫", "裂舍影"),
                    },
                    f"{MOD_ID}_yasuo": {
                        "zh-hans": ("亚索", "疾风剑豪", "斩钢闪", "踏前斩", "狂风绝息斩"),
                        "zh-hant": ("犽宿", "疾風劍豪", "斬鋼閃", "風牆", "奪命氣息"),
                    },
                }
                required_by_locale = required_terms_by_champion.get(champion_id)
                if required_by_locale:
                    required_terms = required_by_locale[locale]
                    missing = [term for term in required_terms if term not in payload_text]
                    if missing:
                        fail(f"runtime text locale {locale} description.{champion_id} missing search aliases {missing}")


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
