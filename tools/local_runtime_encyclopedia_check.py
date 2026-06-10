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
    f"{MOD_ID}_darius",
    f"{MOD_ID}_kayn",
    f"{MOD_ID}_yasuo",
    f"{MOD_ID}_jinx",
    f"{MOD_ID}_thresh",
    f"{MOD_ID}_viktor",
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
REQUIRED_DESCRIPTION_KEYS = ("name", "attack", "skill", "skill2", "ult")
REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS: dict[str, dict[str, tuple[str, ...]]] = {
    f"{MOD_ID}_aatrox": {
        "en": ("Aatrox",),
        "zh-hans": ("亚托克斯", "剑魔"),
        "zh-hant": ("亞托克斯", "劍魔"),
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
        "champion/darius.data_champion",
        "champion/kayn.data_champion",
        "champion/yasuo.data_champion",
        "champion/jinx.data_champion",
        "champion/thresh.data_champion",
        "champion/viktor.data_champion",
        "text/champion.i18n",
        "style/champion_view.champion_view",
        "aseprite_resources/champions/aatrox#sheet.png",
        "aseprite_resources/champions/aatrox#anim.fanim",
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
        "qa/aatrox_official_audio_sources.json",
        "qa/darius_official_audio_sources.json",
        "qa/kayn_official_audio_sources.json",
        "qa/yasuo_official_audio_sources.json",
        "qa/jinx_official_audio_sources.json",
        "qa/thresh_official_audio_sources.json",
        "qa/viktor_official_audio_sources.json",
        "qa/roster_visibility_coverage.json",
    ]
    for event_name in AATROX_SOUND_EVENTS:
        critical_files.append(f"sound/sfx/{event_name}.sound_info")
        if event_name == "test_mod_aatrox_dash_cast":
            critical_files.append("sound/sfx/test_mod_aatrox_dash_voice_clip.wav")
            critical_files.append("sound/sfx/test_mod_aatrox_dash_effect_clip.wav")
        else:
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

    for relative in (
        "aseprite_resources/effects/jinx_get_excited_aura#sheet.png",
        "aseprite_resources/effects/jinx_get_excited_aura#anim.fanim",
        "aseprite_resources/effects/jinx_fishbones_mode_aura#sheet.png",
        "aseprite_resources/effects/jinx_fishbones_mode_aura#anim.fanim",
    ):
        if (runtime_root / relative).exists():
            fail(f"runtime mod still contains retired actor-attached Jinx VFX: {runtime_root / relative}")

    for data_path in sorted((runtime_root / "champion").glob("*.data_champion")):
        check_view_effect_types(data_path, load_json(data_path))

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
                        "zh-hans": "魂锁典狱长",
                        "zh-hant": "魂鎖典獄長",
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
                        "Darius",
                        "诺手",
                        "諾手",
                        "凯隐",
                        "慨影",
                        "亚索",
                        "犽宿",
                        "金克丝",
                        "金克絲",
                        "锤石",
                        "瑟雷西",
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
                        "zh-hans": ("维克托", "奥术先驱", "光荣进化", "海克斯射线", "重力场", "奥术风暴"),
                        "zh-hant": ("維克特", "奧術先驅", "光榮進化", "海克斯射線", "重力場", "奧術風暴"),
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
