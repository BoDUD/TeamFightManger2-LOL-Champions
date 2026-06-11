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
    "darius",
    "ezreal",
    "fiddlesticks",
    "fizz",
    "jhin",
    "jinx",
    "kayn",
    "thresh",
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
AATROX_DISPLAY_FRAME_SIZE = (54.0, 50.0)
AATROX_ACTION_FRAME_SIZE = (96.0, 72.0)
AATROX_MIN_DISPLAY_BOTTOM_SAFE_PIXELS = 8
AATROX_MIN_ACTION_BOTTOM_SAFE_PIXELS = 12
AATROX_MIN_DISPLAY_BODY_HEIGHT = 39
AATROX_MAX_DISPLAY_BODY_HEIGHT = 48
AATROX_MAX_ACTION_BODY_HEIGHT = 50
AATROX_MAX_BATTLE_SCALE_DELTA = 8
AATROX_MAX_BASIC_ATTACK_WIDTH = 62
AATROX_MIN_RUN_FOOT_CENTER_RANGE = 0.9
AATROX_MIN_RUN_FOOT_SHAPES = 5
AATROX_MIN_RUN_UNIQUE_FRAMES = 5
AATROX_MIN_RUN_FOOT_PIXELS = 24
AATROX_MIN_RUN_LOWER_PIXELS = 40
AATROX_RUN_FRAME_DURATION = 0.16
AATROX_MAX_RUN_WIDTH_RANGE = 8
AATROX_RUN_DETACHED_BLADE_MIN_X = 74
AATROX_RUN_DETACHED_BLADE_MIN_Y = 45
AATROX_IDLE_FRAME_XS = (0, 96, 192, 288, 384, 480, 576, 672, 768)
AATROX_ULT_FRAME_X = 864
AATROX_HIT_FRAME_X = 960
AATROX_DEAD_FRAME_X = 1056
AATROX_RETIRED_MODEL_FRAME_XS = (5868, 5964, 6060, 6156, 6252, 6348, 6444, 6540, 6636)
AATROX_RUN_FRAME_XS = (4224, 4320, 4416, 4512, 4608, 4704, 4800, 4896)
AATROX_ATTACK_FRAME_XS = (4992, 5088, 5184, 5280, 5376, 5472, 5568, 5664, 5760)
AATROX_SKILL_FRAME_XS = (2784, 2880, 2976, 3072, 3168, 3264, 3360, 3456)
AATROX_SKILL2_FRAME_XS = (3552, 3648, 3744, 3840, 3936, 4032, 4128)
AATROX_FRAME_SIZES = {
    "idle": AATROX_DISPLAY_FRAME_SIZE,
    "run": AATROX_ACTION_FRAME_SIZE,
    "attack": AATROX_ACTION_FRAME_SIZE,
    "skill": AATROX_ACTION_FRAME_SIZE,
    "skill2": AATROX_ACTION_FRAME_SIZE,
    "hit": AATROX_DISPLAY_FRAME_SIZE,
    "dead": AATROX_DISPLAY_FRAME_SIZE,
    "ult": AATROX_DISPLAY_FRAME_SIZE,
}
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
DARIUS_IDS = ("bo_league_champions_darius", "test_mod_darius")
DARIUS_FRAME_SIZE = (57.0, 54.0)
DARIUS_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
DARIUS_EFFECT_REFS = {
    "test_mod_darius_apprehend": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_apprehend",
        "chain",
    ),
}
DARIUS_VIEW_EFFECT_REFS = {
    "test_mod_darius_attack_slash_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_attack_slash",
        "slash",
    ),
    "test_mod_darius_bleed_apply_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_bleed_apply",
        "hit",
    ),
    "test_mod_darius_decimate_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_decimate",
        "swing",
    ),
    "test_mod_darius_decimate_heal_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_decimate_heal",
        "heal",
    ),
    "test_mod_darius_crippling_strike_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_crippling_strike",
        "hit",
    ),
    "test_mod_darius_noxian_guillotine_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_noxian_guillotine",
        "cast",
    ),
    "test_mod_darius_noxian_guillotine_hit_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_noxian_guillotine_hit",
        "hit",
    ),
}
DARIUS_BUFF_REFS = {
    "test_mod_darius_noxian_might_visual": (
        "asset/bo_league_champions/aseprite_resources/effects/darius_noxian_might_aura",
        "loop",
    ),
}
DARIUS_SOUND_MEDIA_IDS = {
    "test_mod_darius_attack_cast": "720364500",
    "test_mod_darius_attack_hit": "332456238",
    "test_mod_darius_hemo_apply": "4425754",
    "test_mod_darius_noxian_might": "9103428",
    "test_mod_darius_q_cast": "392706208",
    "test_mod_darius_q_hit": "448140634",
    "test_mod_darius_q_heal": "649971236",
    "test_mod_darius_e_cast": "154735781",
    "test_mod_darius_e_hit": "607726065",
    "test_mod_darius_w_hit": "982525424",
    "test_mod_darius_r_cast": "264287498",
    "test_mod_darius_r_hit": "493187816",
    "test_mod_darius_ult_voice": "offset_3621937",
}
DARIUS_SKILL_SOUND_EVENTS = set(DARIUS_SOUND_MEDIA_IDS)
DARIUS_SKILL_SOUND_VOLUME_FLOOR = 0.84
DARIUS_FORBIDDEN_VIEW_EFFECTS = {"test_mod_darius_apprehend_cast_vfx"}
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
    "test_mod_kayn_attack_slash_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_attack_slash",
        "slash",
    ),
    "test_mod_kayn_q_slash_cast_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/kayn_q_slash",
        "slash",
    ),
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
JINX_BUFF_REFS: dict[str, tuple[str, str]] = {}
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
THRESH_IDS = ("bo_league_champions_thresh", "test_mod_thresh")
THRESH_FRAME_SIZE = (57.0, 54.0)
THRESH_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
THRESH_MIN_BOTTOM_SAFE = 8
THRESH_MAX_BODY_WIDTH = 52
THRESH_FORBIDDEN_CASTER_FOLLOW_VFX = {
    "test_mod_thresh_lantern_cast_vfx",
    "test_mod_thresh_flay_cast_vfx",
    "test_mod_thresh_box_cast_vfx",
}
THRESH_EFFECT_REFS = {
    "test_mod_thresh_attack_chain": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_attack_chain",
        "chain",
    ),
    "test_mod_thresh_attack_empowered": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_attack_empowered",
        "burst",
    ),
    "test_mod_thresh_death_sentence_chain": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_death_sentence_chain",
        "chain",
    ),
    "test_mod_thresh_flay_sweep": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_flay_sweep",
        "sweep",
    ),
}
THRESH_VIEW_EFFECT_REFS = {
    "test_mod_thresh_q_hit_vfx": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_death_sentence_hit",
        "hit",
    ),
    "test_mod_thresh_box": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_box",
        "box",
    ),
    "test_mod_thresh_box_field": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_box",
        "box",
    ),
}
THRESH_BUFF_REFS = {
    "test_mod_thresh_lantern_visual": (
        "asset/bo_league_champions/aseprite_resources/effects/thresh_lantern",
        "loop",
    ),
}
THRESH_SOUND_MEDIA_IDS = {
    "test_mod_thresh_attack_cast": "682908905",
    "test_mod_thresh_attack_hit": "571119671",
    "test_mod_thresh_attack_empowered_hit": "930660182",
    "test_mod_thresh_q_cast": "1056922765",
    "test_mod_thresh_q_hit": "46212495",
    "test_mod_thresh_lantern_cast": "490224665",
    "test_mod_thresh_lantern_shield": "546270553",
    "test_mod_thresh_e_cast": "415529881",
    "test_mod_thresh_e_hit": "1064069440",
    "test_mod_thresh_r_cast": "37758497",
    "test_mod_thresh_r_hit": "127153748",
    "test_mod_thresh_soul_gain": "662125189",
    "test_mod_thresh_ult_voice": "offset_86766",
}
THRESH_SKILL_SOUND_EVENTS = {
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
}
THRESH_SKILL_SOUND_VOLUME_FLOOR = 0.84
VIKTOR_IDS = ("bo_league_champions_viktor", "test_mod_viktor")
VIKTOR_FRAME_SIZE = (57.0, 54.0)
VIKTOR_CORE_ACTIONS = ("idle", "run", "attack", "skill", "skill2", "hit", "dead", "ult")
VIKTOR_MIN_BOTTOM_SAFE = 7
VIKTOR_MAX_CLEAN_CAST_WIDTH = 43
VIKTOR_LASER_MIN_APPLY = 60
VIKTOR_AFTERSHOCK_MIN_APPLY = 72
VIKTOR_STORM_MIN_TICKS = (300, 360)
VIKTOR_EFFECT_REFS = {
    "test_mod_viktor_attack_projectile": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_attack_projectile",
        "projectile",
    ),
    "test_mod_viktor_laser": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_laser",
        "laser",
    ),
    "test_mod_viktor_laser_aftershock": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_laser_aftershock",
        "burn",
    ),
}
VIKTOR_VIEW_EFFECT_REFS = {
    "test_mod_viktor_siphon_shield": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_siphon_shield",
        "shield",
    ),
    "test_mod_viktor_gravity_field": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_gravity_field",
        "gravity_field",
    ),
    "test_mod_viktor_chaos_storm": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_chaos_storm",
        "chaos_storm",
    ),
    "test_mod_viktor_storm_impact": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_storm_impact",
        "impact",
    ),
}
VIKTOR_BUFF_REFS = {
    "test_mod_viktor_siphon_empower": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_siphon_shield",
        "shield",
    ),
    "test_mod_viktor_evolved_ray": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_evolution_aura",
        "ray",
    ),
    "test_mod_viktor_evolved_field": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_evolution_aura",
        "field",
    ),
    "test_mod_viktor_evolved_storm": (
        "asset/bo_league_champions/aseprite_resources/effects/viktor_evolution_aura",
        "storm",
    ),
}
VIKTOR_SOUND_MEDIA_IDS = {
    "test_mod_viktor_attack_cast": "366956455",
    "test_mod_viktor_attack_hit": "638215974",
    "test_mod_viktor_siphon_cast": "718200240",
    "test_mod_viktor_siphon_empower_hit": "492941568",
    "test_mod_viktor_laser_cast": "265099124",
    "test_mod_viktor_laser_hit": "531075080",
    "test_mod_viktor_laser_aftershock_hit": "748611133",
    "test_mod_viktor_gravity_field_cast": "626995735",
    "test_mod_viktor_gravity_field_slow": "526229873",
    "test_mod_viktor_chaos_storm_cast": "648540030",
    "test_mod_viktor_chaos_storm_duration": "90156452",
    "test_mod_viktor_storm_impact": "103931219",
    "test_mod_viktor_evolution": "760600724",
    "test_mod_viktor_ult_voice": "offset_85528",
}
VIKTOR_SKILL_SOUND_EVENTS = {
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
}
VIKTOR_SKILL_SOUND_VOLUME_FLOOR = 0.84
COMPACT_DISPLAY_LIMITS = {
    "darius": {"max_width": 42, "max_height": 40, "min_bottom_safe": 12},
    "thresh": {"max_width": 42, "max_height": 40, "min_bottom_safe": 12},
    "viktor": {"max_width": 39, "max_height": 42, "min_bottom_safe": 11},
}
SIDE_CARD_STANDING_FACE_OFFSETS = {
    "aatrox": {"x": 2, "y": -16},
    "darius": {"x": 2, "y": -12},
    "kayn": {"x": 4, "y": -18},
    "thresh": {"x": 0, "y": -12},
    "viktor": {"x": 0, "y": -28},
}
SIDE_CARD_STANDING_CENTER_OFFSETS = {
    "aatrox": {"x": 4, "y": -12},
    "darius": {"x": 0, "y": -12},
    "kayn": {"x": 0, "y": -12},
    "thresh": {"x": 0, "y": -12},
    "viktor": {"x": 0, "y": -12},
}
REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS: dict[str, dict[str, tuple[str, ...]]] = {}
for _champion_id in AATROX_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Aatrox",),
        "zh-hans": ("\u4e9a\u6258\u514b\u65af", "\u5251\u9b54"),
        "zh-hant": ("\u4e9e\u6258\u514b\u65af", "\u528d\u9b54"),
    }
for _champion_id in DARIUS_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Darius", "Hand of Noxus", "Hemorrhage", "Decimate", "Apprehend", "Crippling Strike", "Noxian Guillotine"),
        "zh-hans": ("\u8bfa\u514b\u8428\u65af\u4e4b\u624b", "\u8bfa\u624b", "Darius", "\u51fa\u8840", "\u5927\u6740\u56db\u65b9", "\u65e0\u60c5\u94c1\u624b", "\u81f4\u6b8b\u6253\u51fb", "\u8bfa\u514b\u8428\u65af\u65ad\u5934\u53f0"),
        "zh-hant": ("\u8afe\u514b\u85a9\u65af\u4e4b\u624b", "\u8afe\u624b", "Darius", "\u51fa\u8840", "\u5927\u6bba\u56db\u65b9", "\u7121\u60c5\u9435\u624b", "\u81f4\u6b98\u6253\u64ca", "\u8afe\u514b\u85a9\u65af\u65b7\u982d\u53f0"),
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
for _champion_id in THRESH_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Thresh", "Chain Warden"),
        "zh-hans": ("\u9b42\u9501\u5178\u72f1\u957f", "\u9524\u77f3"),
        "zh-hant": ("\u9b42\u9396\u5178\u7344\u9577", "\u745f\u96f7\u897f"),
    }
for _champion_id in VIKTOR_IDS:
    REQUIRED_ENCYCLOPEDIA_SEARCH_TERMS[_champion_id] = {
        "en": ("Viktor", "Herald of the Arcane", "Glorious Evolution", "Hextech Ray", "Gravity Field", "Arcane Storm"),
        "zh-hans": ("\u7ef4\u514b\u6258", "\u5965\u672f\u5148\u9a71", "\u673a\u68b0\u5148\u9a71", "\u5149\u8363\u8fdb\u5316", "\u6d77\u514b\u65af\u5c04\u7ebf", "\u91cd\u529b\u573a", "\u5965\u672f\u98ce\u66b4"),
        "zh-hant": ("\u7dad\u514b\u7279", "\u5967\u8853\u5148\u9a45", "\u6a5f\u68b0\u5148\u9a45", "\u5149\u69ae\u9032\u5316", "\u6d77\u514b\u65af\u5c04\u7dda", "\u91cd\u529b\u5834", "\u5967\u8853\u98a8\u66b4"),
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


def alpha_visible_pixels_in_rect(alpha: bytes, image_width: int, rect: tuple[int, int, int, int]) -> int:
    x0, y0, w, h = rect
    visible = 0
    for y in range(y0, y0 + h):
        row_start = y * image_width
        for x in range(x0, x0 + w):
            if alpha[row_start + x] != 0:
                visible += 1
    return visible


def dark_actor_pixels_in_rect(rgba: bytes, image_width: int, rect: tuple[int, int, int, int]) -> int:
    x0, y0, w, h = rect
    dark_pixels = 0
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            index = (y * image_width + x) * 4
            r = rgba[index]
            g = rgba[index + 1]
            b = rgba[index + 2]
            a = rgba[index + 3]
            if a <= 60:
                continue
            dark_or_grey_body = (r < 85 and g < 120 and b < 110) or (
                abs(r - g) < 30 and abs(g - b) < 35 and r < 150
            )
            if dark_or_grey_body:
                dark_pixels += 1
    return dark_pixels


def rgba_frame_stats(
    rgba: bytes, image_width: int, rect: tuple[int, int, int, int]
) -> tuple[int, int, tuple[int, int, int, int] | None, float]:
    x0, y0, w, h = rect
    min_x = min_y = 10**9
    max_x = max_y = -1
    visible = 0
    colors: set[tuple[int, int, int]] = set()
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            index = (y * image_width + x) * 4
            r = rgba[index]
            g = rgba[index + 1]
            b = rgba[index + 2]
            a = rgba[index + 3]
            if a <= 20:
                continue
            local_x = x - x0
            local_y = y - y0
            visible += 1
            colors.add((r // 8, g // 8, b // 8))
            min_x = min(min_x, local_x)
            min_y = min(min_y, local_y)
            max_x = max(max_x, local_x + 1)
            max_y = max(max_y, local_y + 1)
    if max_x < 0:
        return visible, len(colors), None, 0.0
    bbox = (min_x, min_y, max_x, max_y)
    bbox_area = max(1, (max_x - min_x) * (max_y - min_y))
    return visible, len(colors), bbox, visible / bbox_area


def assert_generated_vfx_volume(
    sheet: Path,
    fanim_path: Path,
    tag: str,
    label: str,
    *,
    min_visible: int,
    min_color_bins: int,
    min_height: int,
    min_fill_ratio: float,
    max_width: int | None = None,
) -> None:
    fanim = load_json(fanim_path)
    frames = fanim.get("anims", {}).get(tag, {}).get("frames") if isinstance(fanim, dict) else None
    if not isinstance(frames, list):
        fail(f"{fanim_path.relative_to(ROOT)} must expose {tag!r} frames for {label}")
    image_width, _image_height, rgba = load_rgba(sheet)
    for index, frame in enumerate(frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict):
            fail(f"{label} frame {index} missing frame data")
        rect = (
            int(round(float(data.get("x", -1)))),
            int(round(float(data.get("y", -1)))),
            int(round(float(data.get("w", 0)))),
            int(round(float(data.get("h", 0)))),
        )
        visible, color_bins, bbox, fill_ratio = rgba_frame_stats(rgba, image_width, rect)
        if bbox is None:
            fail(f"{label} frame {index} is blank")
        frame_width = bbox[2] - bbox[0]
        frame_height = bbox[3] - bbox[1]
        if visible < min_visible:
            fail(f"{label} frame {index} has only {visible} visible pixels; image-generated VFX must not regress to line art")
        if color_bins < min_color_bins:
            fail(f"{label} frame {index} has only {color_bins} color bins; VFX must use raster image texture, not flat line strokes")
        if frame_height < min_height:
            fail(f"{label} frame {index} height {frame_height}px is too thin; hook/pull skills must have visible body volume")
        if fill_ratio < min_fill_ratio:
            fail(f"{label} frame {index} fill ratio {fill_ratio:.2f} is too sparse; avoid wire/arrow/guide-line skills")
        if max_width is not None and frame_width > max_width:
            fail(f"{label} frame {index} spans {frame_width}px; avoid full-width line/tether VFX in a single projectile frame")


def assert_effect_frames_not_edge_cut(
    sheet: Path,
    fanim_path: Path,
    tag: str,
    label: str,
    *,
    border: int = 2,
    max_border_pixels: int = 0,
) -> None:
    fanim = load_json(fanim_path)
    frames = fanim.get("anims", {}).get(tag, {}).get("frames") if isinstance(fanim, dict) else None
    if not isinstance(frames, list):
        fail(f"{fanim_path.relative_to(ROOT)} must expose {tag!r} frames for {label}")
    image_width, _image_height, rgba = load_rgba(sheet)
    for index, frame in enumerate(frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict):
            fail(f"{label} frame {index} missing frame data")
        x0 = int(round(float(data.get("x", -1))))
        y0 = int(round(float(data.get("y", -1))))
        w = int(round(float(data.get("w", 0))))
        h = int(round(float(data.get("h", 0))))
        border_pixels = 0
        for y in range(y0, y0 + h):
            local_y = y - y0
            for x in range(x0, x0 + w):
                local_x = x - x0
                if border <= local_x < w - border and border <= local_y < h - border:
                    continue
                if rgba[(y * image_width + x) * 4 + 3] > 20:
                    border_pixels += 1
        if border_pixels > max_border_pixels:
            fail(
                f"{label} frame {index} has {border_pixels} visible pixels touching the cell edge; "
                "repack the VFX into the native cell instead of letting it flash as a cut-off half-effect"
            )


def collect_weapon_palette_from_rect(path: Path, rect: tuple[int, int, int, int]) -> set[tuple[int, int, int]]:
    image_width, _image_height, rgba = load_rgba(path)
    x0, y0, w, h = rect
    colors: set[tuple[int, int, int]] = set()
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            index = (y * image_width + x) * 4
            r = rgba[index]
            g = rgba[index + 1]
            b = rgba[index + 2]
            a = rgba[index + 3]
            if a <= 80:
                continue
            if r > 120 and 55 < g < 125 and 30 < b < 95:
                continue
            steel = abs(r - g) < 42 and abs(g - b) < 48 and r > 45
            red = r > 70 and r > g * 1.25 and r > b * 1.1
            dark = r < 70 and g < 60 and b < 65
            if steel or red or dark:
                colors.add((r, g, b))
    return colors


def count_palette_matches_in_rect(
    rgba: bytes,
    image_width: int,
    rect: tuple[int, int, int, int],
    palette: set[tuple[int, int, int]],
    *,
    tolerance: int,
) -> int:
    x0, y0, w, h = rect
    matches = 0
    palette_list = list(palette)
    for y in range(y0, y0 + h):
        for x in range(x0, x0 + w):
            index = (y * image_width + x) * 4
            r = rgba[index]
            g = rgba[index + 1]
            b = rgba[index + 2]
            a = rgba[index + 3]
            if a <= 80:
                continue
            for pr, pg, pb in palette_list:
                if abs(r - pr) + abs(g - pg) + abs(b - pb) <= tolerance:
                    matches += 1
                    break
    return matches


def assert_compact_idle_bottom_safety(champion: str, *, min_bottom_safe: int = 10) -> None:
    fanim_path = ROOT / "aseprite_resources" / "champions" / f"{champion}#anim.fanim"
    sheet_path = ROOT / "aseprite_resources" / "champions" / f"{champion}#sheet.png"
    fanim = load_json(fanim_path)
    frames = fanim.get("anims", {}).get("idle", {}).get("frames") if isinstance(fanim, dict) else None
    if not isinstance(frames, list) or not frames:
        fail(f"{fanim_path.relative_to(ROOT)} must expose idle frames for compact portrait safety")
    data = frames[0].get("data") if isinstance(frames[0], dict) else None
    if not isinstance(data, dict):
        fail(f"{champion} first idle frame missing frame data for compact portrait safety")
    rect = (
        int(round(float(data.get("x", -1)))),
        int(round(float(data.get("y", -1)))),
        int(round(float(data.get("w", 0)))),
        int(round(float(data.get("h", 0)))),
    )
    sheet_width, _sheet_height, sheet_alpha = load_rgba_alpha(sheet_path)
    bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, rect)
    if bbox is None:
        fail(f"{champion} first idle frame is blank; compact portraits need a full body")
    bottom_safe = rect[3] - bbox[3]
    if bottom_safe < min_bottom_safe:
        fail(
            f"{champion} first idle frame leaves only {bottom_safe}px below the feet/weapon; "
            f"compact exchange/side-card portraits need at least {min_bottom_safe}px so legs stay visible"
        )


def assert_compact_display_frame_size(champion: str) -> None:
    limits = COMPACT_DISPLAY_LIMITS.get(champion)
    if not limits:
        return
    fanim_path = ROOT / "aseprite_resources" / "champions" / f"{champion}#anim.fanim"
    sheet_path = ROOT / "aseprite_resources" / "champions" / f"{champion}#sheet.png"
    fanim = load_json(fanim_path)
    anims = fanim.get("anims") if isinstance(fanim, dict) else None
    if not isinstance(anims, dict):
        fail(f"{fanim_path.relative_to(ROOT)} must contain anims")
    sheet_width, _sheet_height, sheet_alpha = load_rgba_alpha(sheet_path)
    seen_rects: set[tuple[int, int, int, int]] = set()
    for action in ("idle", "recall", "return"):
        frames = anims.get(action, {}).get("frames") if isinstance(anims.get(action), dict) else None
        if not isinstance(frames, list) or not frames:
            fail(f"{champion} {action} frames must exist for compact HUD portrait checks")
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"{champion} {action} frame {index} missing frame data for compact HUD portrait checks")
            rect = (
                int(round(float(data.get("x", -1)))),
                int(round(float(data.get("y", -1)))),
                int(round(float(data.get("w", 0)))),
                int(round(float(data.get("h", 0)))),
            )
            if rect in seen_rects:
                continue
            seen_rects.add(rect)
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, rect)
            if bbox is None:
                fail(f"{champion} {action} frame {index} is blank; compact HUD portraits need a readable body")
            body_width = bbox[2] - bbox[0]
            body_height = bbox[3] - bbox[1]
            bottom_safe = rect[3] - bbox[3]
            if body_width > limits["max_width"] or body_height > limits["max_height"]:
                fail(
                    f"{champion} {action} frame {index} body {body_width}x{body_height}px is too large for compact HUD/side-list avatars; "
                    f"limit is {limits['max_width']}x{limits['max_height']}px"
                )
            if bottom_safe < limits["min_bottom_safe"]:
                fail(
                    f"{champion} {action} frame {index} leaves only {bottom_safe}px bottom safety; "
                    f"compact HUD/side-list avatars need at least {limits['min_bottom_safe']}px so feet do not disappear under names"
                )


def check_standard_compact_idle_bottom_safety() -> None:
    for fanim_path in sorted((ROOT / "aseprite_resources" / "champions").glob("*#anim.fanim")):
        champion = fanim_path.name.split("#", 1)[0]
        fanim = load_json(fanim_path)
        frames = fanim.get("anims", {}).get("idle", {}).get("frames") if isinstance(fanim, dict) else None
        if not isinstance(frames, list) or not frames:
            continue
        data = frames[0].get("data") if isinstance(frames[0], dict) else None
        if not isinstance(data, dict):
            continue
        frame_size = (float(data.get("w", 0)), float(data.get("h", 0)))
        if frame_size != (57.0, 54.0):
            continue
        assert_compact_idle_bottom_safety(champion)
        assert_compact_display_frame_size(champion)


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


def assert_static_recall_tags(champion_name: str) -> None:
    fanim = load_json(ROOT / "aseprite_resources" / "champions" / f"{champion_name}#anim.fanim")
    anims = fanim.get("anims") if isinstance(fanim, dict) else None
    if not isinstance(anims, dict):
        fail(f"{champion_name}#anim.fanim must contain anims")
    idle_frames = anims.get("idle", {}).get("frames") if isinstance(anims.get("idle"), dict) else None
    if not isinstance(idle_frames, list) or not idle_frames:
        fail(f"{champion_name} idle animation must exist before adding static recall tags")
    idle_data = idle_frames[0].get("data") if isinstance(idle_frames[0], dict) else None
    if not isinstance(idle_data, dict):
        fail(f"{champion_name} idle frame 0 missing frame data")
    for tag in ("recall", "return"):
        frames = anims.get(tag, {}).get("frames") if isinstance(anims.get(tag), dict) else None
        if not isinstance(frames, list) or len(frames) != 1:
            fail(f"{champion_name} {tag} must be a one-frame static animation for return-to-base")
        frame = frames[0]
        if not isinstance(frame, dict) or frame.get("data") != idle_data:
            fail(f"{champion_name} {tag} must reuse idle frame 0 so recall does not wobble")
        if frame.get("duration") != 0.2:
            fail(f"{champion_name} {tag} must use a stable 0.2s hold frame")


def effect_frame_bboxes(path: Path, frame_w: int, frame_h: int) -> list[tuple[int, int, int, int]]:
    width, height, alpha = load_rgba_alpha(path)
    if height != frame_h or width % frame_w:
        fail(f"{path.relative_to(ROOT)} must use {frame_w}x{frame_h} effect frames")
    bboxes: list[tuple[int, int, int, int]] = []
    for frame_index in range(width // frame_w):
        bbox = alpha_bbox_in_rect(alpha, width, (frame_index * frame_w, 0, frame_w, frame_h))
        if bbox is None:
            fail(f"{path.relative_to(ROOT)} frame {frame_index} is empty")
        bboxes.append(bbox)
    return bboxes


def assert_aatrox_darkin_blade_vfx_identity() -> None:
    q1 = effect_frame_bboxes(ROOT / "aseprite_resources" / "effects" / "aatrox_q1_cleave#sheet.png", 192, 96)
    q2 = effect_frame_bboxes(ROOT / "aseprite_resources" / "effects" / "aatrox_q2_cleave#sheet.png", 192, 96)
    q3 = effect_frame_bboxes(ROOT / "aseprite_resources" / "effects" / "aatrox_q3_cleave#sheet.png", 192, 96)
    q1_widths = [bbox[2] - bbox[0] for bbox in q1[:5]]
    q1_heights = [bbox[3] - bbox[1] for bbox in q1[:5]]
    q2_widths = [bbox[2] - bbox[0] for bbox in q2[:5]]
    q3_heights = [bbox[3] - bbox[1] for bbox in q3[:4]]
    if max(q1_widths) > 135:
        fail(f"Aatrox Q1 VFX must read as a compact ground cleave, not a long spear projectile; widths={q1_widths}")
    if min(q1_heights[:3]) < 55:
        fail(f"Aatrox Q1 VFX must keep a visible vertical sword-impact core; heights={q1_heights}")
    if max(q2_widths) < 165:
        fail(f"Aatrox Q2 VFX must remain the wider side sweep; widths={q2_widths}")
    if max(q2_widths) - max(q1_widths) < 30:
        fail("Aatrox Q1 and Q2 VFX must have visibly different hit-shape width")
    if max(q3_heights) < 90:
        fail(f"Aatrox Q3 VFX must read as a vertical slam/impact burst; heights={q3_heights}")


def assert_kayn_skill_vfx_no_actor_body() -> None:
    for name, frame_w, frame_h in (
        ("kayn_r_entry", 192, 96),
        ("kayn_r_exit", 192, 96),
        ("kayn_darkin_aura", 64, 64),
    ):
        path = ROOT / "aseprite_resources" / "effects" / f"{name}#sheet.png"
        width, height, rgba = load_rgba(path)
        if height != frame_h or width % frame_w:
            fail(f"{path.relative_to(ROOT)} must use {frame_w}x{frame_h} frames")
        for frame_index in range(width // frame_w):
            bodylike_pixels = 0
            for y in range(frame_h):
                for x in range(frame_w):
                    pixel_index = ((y * width) + frame_index * frame_w + x) * 4
                    r = rgba[pixel_index]
                    g = rgba[pixel_index + 1]
                    b = rgba[pixel_index + 2]
                    a = rgba[pixel_index + 3]
                    if not a:
                        continue
                    purple = b > 115 and r > 65 and g < 110
                    red = r > 130 and g < 95 and b < 155
                    blue = b > 130 and g > 70 and r < 125
                    neutral_or_white = max(r, g, b) < 130 or (r > 145 and g > 140 and b > 130)
                    if frame_w == 64:
                        in_body_zone = 18 <= x <= 46 and 4 <= y <= 62
                    else:
                        in_body_zone = 58 <= x <= 134 and 4 <= y <= 92
                    if in_body_zone and neutral_or_white and not (purple or red or blue):
                        bodylike_pixels += 1
            if bodylike_pixels:
                fail(
                    f"{path.relative_to(ROOT)} frame {frame_index} contains {bodylike_pixels} "
                    "neutral actor-body pixels; Kayn skill VFX must be aura/slash only"
                )


def assert_kayn_q_and_attack_vfx_readable() -> None:
    for name, frame_w, frame_h, min_bright, max_width in (
        ("kayn_q_slash", 192, 96, 260, 150),
        ("kayn_attack_slash", 96, 72, 80, 92),
    ):
        path = ROOT / "aseprite_resources" / "effects" / f"{name}#sheet.png"
        width, height, rgba = load_rgba(path)
        if height != frame_h or width % frame_w:
            fail(f"{path.relative_to(ROOT)} must use {frame_w}x{frame_h} frames")
        frame_count = width // frame_w
        bright_counts: list[int] = []
        widths: list[int] = []
        _, _, alpha = load_rgba_alpha(path)
        for frame_index in range(frame_count):
            bbox = alpha_bbox_in_rect(alpha, width, (frame_index * frame_w, 0, frame_w, frame_h))
            if bbox is None:
                fail(f"{path.relative_to(ROOT)} frame {frame_index} is empty")
            widths.append(bbox[2] - bbox[0])
            bright = 0
            for y in range(frame_h):
                for x in range(frame_w):
                    i = ((y * width) + frame_index * frame_w + x) * 4
                    r = rgba[i]
                    g = rgba[i + 1]
                    b = rgba[i + 2]
                    a = rgba[i + 3]
                    if a and (b > 145 or r > 180) and max(r, g, b) - min(r, g, b) > 35:
                        bright += 1
            bright_counts.append(bright)
        if max(bright_counts) < min_bright:
            fail(f"{path.relative_to(ROOT)} must have a visible bright slash; bright counts={bright_counts}")
        if max(widths) > max_width:
            fail(f"{path.relative_to(ROOT)} is too wide for its role; widths={widths}")


def assert_jinx_r_big_projectile() -> None:
    path = ROOT / "aseprite_resources" / "effects" / "jinx_super_mega_death_rocket#sheet.png"
    bboxes = effect_frame_bboxes(path, 128, 64)
    widths = [bbox[2] - bbox[0] for bbox in bboxes]
    heights = [bbox[3] - bbox[1] for bbox in bboxes]
    if min(widths) < 95 or min(heights) < 35:
        fail(f"Jinx R projectile must read as a large Super Mega Death Rocket; widths={widths}, heights={heights}")


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
            expected_id = expected_ids[0]
            if expected_id.startswith("offset_"):
                row_offset = row.get("source_offset")
                documented_offset = f"offset_{row_offset}" if row_offset is not None else str(row.get("media_id"))
                if documented_offset != expected_id:
                    fail(f"official {champion_name} audio event {event_name} must document source_offset {expected_id}")
            elif str(row.get("media_id")) != expected_id:
                fail(f"official {champion_name} audio event {event_name} must document media_id {expected_id}")
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


def iter_mapping_nodes(node: Any) -> list[dict[str, Any]]:
    if isinstance(node, dict):
        out = [node]
        for value in node.values():
            out.extend(iter_mapping_nodes(value))
        return out
    if isinstance(node, list):
        out: list[dict[str, Any]] = []
        for item in node:
            out.extend(iter_mapping_nodes(item))
        return out
    return []


def assert_no_negative_speed_fields(node: Any, label: str) -> None:
    for mapping in iter_mapping_nodes(node):
        speed = mapping.get("speed")
        if isinstance(speed, (int, float)) and speed < 0:
            effect_type = mapping.get("type", "<unknown>")
            fail(f"{label} has invalid negative speed {speed!r} on {effect_type}; TFM2 expects unsigned movement speeds")


def find_effect_nodes(node: Any, effect_type: str) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if isinstance(node, dict):
        if node.get("type") == effect_type:
            out.append(node)
        for value in node.values():
            out.extend(find_effect_nodes(value, effect_type))
    elif isinstance(node, list):
        for item in node:
            out.extend(find_effect_nodes(item, effect_type))
    return out


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


def check_full_body_compact_portraits(entries: dict[str, Any]) -> None:
    for champion in sorted(EXPECTED_CHAMPIONS):
        for style_id in (f"{MOD_ID}_{champion}", f"test_mod_{champion}"):
            view = entries.get(style_id)
            if not isinstance(view, dict):
                fail(f"style/champion_view.champion_view missing entries.{style_id}")
            face = view.get("face")
            center = view.get("center")
            if not isinstance(face, dict) or not isinstance(center, dict):
                fail(f"style entry {style_id} must define both face and center cameras")
            expected_side_face = SIDE_CARD_STANDING_FACE_OFFSETS.get(champion)
            if expected_side_face is not None:
                if face.get("x") != expected_side_face["x"] or face.get("y") != expected_side_face["y"]:
                    fail(
                        f"style entry {style_id}.face must be {expected_side_face} so pick/ban side cards show standing feet"
                    )
                expected_side_center = SIDE_CARD_STANDING_CENTER_OFFSETS.get(champion)
                if not isinstance(expected_side_center, dict):
                    fail(f"CI missing side-card center offset for {champion}")
                if center.get("x") != expected_side_center["x"] or center.get("y") != expected_side_center["y"]:
                    fail(
                        f"style entry {style_id}.center must be {expected_side_center} so exchange standing cards show feet; "
                        f"got center={center!r}"
                    )
            elif face.get("y") != center.get("y"):
                fail(
                    f"style entry {style_id}.face.y must match center.y for full-body compact portraits; "
                    f"got face.y={face.get('y')!r}, center.y={center.get('y')!r}"
                )


def check_aatrox_rework_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_names = {
        "zh-hans": ("\u6697\u88d4\u5251\u9b54",),
        "zh-hant": ("\u6697\u88d4\u528d\u9b54",),
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
        center_x = view.get("center", {}).get("x")
        center_y = view.get("center", {}).get("y")
        if face_x != 2 or face_y != -16:
            fail(f"style entry {aatrox_id}.face must keep Aatrox HUD/scoreboard portrait centered at x=2,y=-16")
        if center_x != 4 or center_y != -12:
            fail(f"style entry {aatrox_id}.center must keep Aatrox exchange standing sword and feet visible at x=4,y=-12")

    for path in (
        ROOT / "aseprite_resources" / "champions" / "aatrox#sheet.png",
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
    assert_aatrox_darkin_blade_vfx_identity()

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "aatrox#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "aatrox#sheet.png"
    )
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
    allowed_pixels: set[tuple[int, int]] = set()
    for action, frame_xs in expected_frame_xs.items():
        expected_w, expected_h = AATROX_FRAME_SIZES[action]
        for allowed_x in frame_xs:
            for local_y in range(int(expected_h)):
                for local_x in range(int(expected_w)):
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
        retired_w = min(int(AATROX_ACTION_FRAME_SIZE[0]), sheet_width - x)
        if retired_w <= 0:
            continue
        bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, 0, retired_w, int(AATROX_ACTION_FRAME_SIZE[1])))
        if bbox is not None:
            fail(f"Aatrox retired old-model frame slot at x={x} must stay blank")
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
            expected_frame_size = AATROX_FRAME_SIZES[action]
            if (data.get("w"), data.get("h")) != expected_frame_size:
                fail(
                    f"Aatrox {action} frame {index} must use the requested final-model "
                    f"{expected_frame_size[0]:.0f}x{expected_frame_size[1]:.0f} actor frame"
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
            if action in ("run", "attack", "skill", "skill2"):
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
            if action in ("idle", "run", "hit", "ult") and body_height < AATROX_MIN_DISPLAY_BODY_HEIGHT:
                fail(
                    f"Aatrox {action} frame {index} body height {body_height}px is too small; "
                    "the accepted Darkin model must stay imposing like the current enlarged source"
                )
            if bottom_safe < min_bottom_safe:
                fail(
                    f"Aatrox {action} frame {index} leaves only {bottom_safe}px bottom safety; "
                    "feet must stay above the name/health label like Viktor"
                )
            if action == "run":
                if frame.get("duration") != AATROX_RUN_FRAME_DURATION:
                    fail(f"Aatrox run frame {index} must use calmer {AATROX_RUN_FRAME_DURATION}s timing")
                detached_pixels = 0
                for local_y in range(AATROX_RUN_DETACHED_BLADE_MIN_Y, h):
                    row_start = (y + local_y) * sheet_width
                    for local_x in range(AATROX_RUN_DETACHED_BLADE_MIN_X, w):
                        if sheet_alpha[row_start + x + local_x] != 0:
                            detached_pixels += 1
                if detached_pixels:
                    fail(
                        f"Aatrox run frame {index} has {detached_pixels} detached right-side blade pixels; "
                        "clear actor fragments so the model does not flicker beside itself"
                    )

    run_widths = [bbox[2] - bbox[0] for bbox in action_bboxes["run"]]
    run_heights = [bbox[3] - bbox[1] for bbox in action_bboxes["run"]]
    run_tops = [bbox[1] for bbox in action_bboxes["run"]]
    run_bottoms = [bbox[3] for bbox in action_bboxes["run"]]
    run_hashes = action_hashes["run"]
    idle_widths = [bbox[2] - bbox[0] for bbox in action_bboxes["idle"]]
    if min(idle_widths) < 42:
        fail("Aatrox idle frames must keep the greatsword visible in compact portraits and recall")
    battle_body_heights = [
        bbox[3] - bbox[1]
        for action in ("idle", "run", "attack", "skill", "skill2", "hit", "ult")
        for bbox in action_bboxes[action]
    ]
    display_reference_heights = [
        bbox[3] - bbox[1]
        for action in ("idle", "hit", "ult")
        for bbox in action_bboxes[action]
    ]
    if max(battle_body_heights) - min(display_reference_heights) > AATROX_MAX_BATTLE_SCALE_DELTA:
        fail(
            "Aatrox battle frames must stay in one body scale class; "
            "run/skill frames must not grow larger than idle/hit/ult"
        )
    if max(run_widths) - min(run_widths) > AATROX_MAX_RUN_WIDTH_RANGE:
        fail("Aatrox run frame widths must stay stable to avoid animation jitter")
    if max(run_tops) - min(run_tops) > 1 or max(run_bottoms) - min(run_bottoms) > 1:
        fail("Aatrox run body vertical anchor must stay stable; remove jumping/crouching frame pops")
    if len(set(run_hashes)) < AATROX_MIN_RUN_UNIQUE_FRAMES:
        fail("Aatrox run must have at least five distinct frames; a two-pose ABAB cycle reads like a zombie shuffle")
    if len(run_hashes) == 8 and len(set(run_hashes[0::2])) == 1 and len(set(run_hashes[1::2])) == 1:
        fail("Aatrox run must not alternate the same two poses across all eight frames")
    for action in ("attack", "skill", "skill2"):
        widths = [bbox[2] - bbox[0] for bbox in action_bboxes[action]]
        if action == "attack" and max(widths) > AATROX_MAX_BASIC_ATTACK_WIDTH:
            fail(
                f"Aatrox basic attack width {max(widths)}px is too large; "
                "auto attacks must keep a stable forward-facing body and avoid Q-sized side cleaves"
            )
        if max(widths) < min(run_widths):
            fail(f"Aatrox {action} must include readable weapon/body motion from the final model source")
        if len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Aatrox {action} must have visible body/weapon motion, not repeated static frames")
        if tuple(action_hashes[action][: len(action_hashes["run"])]) == tuple(action_hashes["run"][: len(action_hashes[action])]):
            fail(f"Aatrox {action} must not be a direct copy of the run cycle")
    for action in ("idle", "hit", "ult"):
        heights = [bbox[3] - bbox[1] for bbox in action_bboxes[action]]
        if max(heights) > AATROX_MAX_DISPLAY_BODY_HEIGHT or min(heights) < AATROX_MIN_DISPLAY_BODY_HEIGHT:
            fail(f"Aatrox {action} display frame height must stay readable in champion views")

    foot_centers: list[float] = []
    foot_shapes: set[tuple[tuple[int, int], ...]] = set()
    for index, frame in enumerate(run_frames):
        data = frame["data"]
        x = int(round(float(data["x"])))
        y = int(round(float(data["y"])))
        w = int(round(float(data["w"])))
        bbox = action_bboxes["run"][index]
        body_height = bbox[3] - bbox[1]
        lower_start = bbox[1] + (body_height * 2) // 3
        foot_start = bbox[1] + (body_height * 3) // 4
        local_points: list[tuple[int, int]] = []
        lower_points: list[tuple[int, int]] = []
        for local_y in range(lower_start, bbox[3]):
            row_start = (y + local_y) * sheet_width
            for local_x in range(bbox[0], min(bbox[2], w)):
                if sheet_alpha[row_start + x + local_x] != 0:
                    lower_points.append((local_x, local_y))
        for local_y in range(foot_start, bbox[3]):
            row_start = (y + local_y) * sheet_width
            for local_x in range(bbox[0], min(bbox[2], w)):
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
    attack_strings = set(walk_strings(aatrox.get("attack", {})))
    if "test_mod_aatrox_attack_slash_vfx" in attack_strings or "test_mod_aatrox_attack_slash_vfx" in view_effect_refs:
        fail("Aatrox basic attack must not trigger the oversized skill-like attack slash VFX")
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
        if label == "Q3":
            for required in ("Airborne", "Stun", "BlockMoveSkill"):
                if required not in branch_strings:
                    fail(f"Aatrox Q3 must include {required} for the heavy third Darkin Blade impact")

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
        if face_y != -18:
            fail(f"style entry {kayn_id}.face.y must keep Kayn's HUD/scoreboard portrait centered at -18")
        if not isinstance(center_y, (int, float)) or not -20 <= center_y <= -8:
            fail(f"style entry {kayn_id}.center.y must keep the full-body display above the name")

    for path in (
        ROOT / "aseprite_resources" / "champions" / "kayn#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "kayn_attack_slash#sheet.png",
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
    assert_kayn_skill_vfx_no_actor_body()
    assert_kayn_q_and_attack_vfx_readable()

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
    kayn_ult = kayn.get("ult", {})
    if kayn_ult.get("range") < 80000 or kayn_ult.get("cooltime") > 3000 or kayn_ult.get("can_use_with_move") is not True:
        fail("Kayn ult must keep AI-usable range/cooldown/cast-while-moving settings")
    if kayn_ult.get("duration") > 60 or kayn_ult.get("start_timing") > 8:
        fail("Kayn ult must enter quickly so AI casts do not stall before target selection")
    if "36" not in json.dumps(kayn_ult, ensure_ascii=False):
        fail("Kayn ult must use the shortened 36-tick trespass/stasis window")
    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in kayn.get("view_projectiles", [])}
    for name, expected in KAYN_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/kayn.data_champion projectile {name} must reference {expected}")
    effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in kayn.get("view_effects", [])}
    for name, expected in KAYN_VIEW_EFFECT_REFS.items():
        if effect_refs.get(name) != expected:
            fail(f"champion/kayn.data_champion view_effect {name} must reference {expected}")
    attack_strings = set(walk_strings(kayn.get("attack", {})))
    if "test_mod_kayn_attack_slash_vfx" not in attack_strings:
        fail("Kayn basic attack must trigger a small scythe slash VFX")
    skill_strings = set(walk_strings(kayn.get("skill", {})))
    if "test_mod_kayn_q_slash_cast_vfx" not in skill_strings:
        fail("Kayn Q must trigger a visible caster-side slash VFX as well as the line projectile")
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
        if view.get("face", {}).get("x") != 4 or view.get("face", {}).get("y") != -12:
            fail(f"style entry {yasuo_id}.face must keep Yasuo full-body compact portrait aligned at x=4,y=-12")
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
        if view.get("face", {}).get("x") != -2 or view.get("face", {}).get("y") != -16:
            fail(f"style entry {jinx_id}.face must keep Jinx full-body compact portrait aligned at x=-2,y=-16")
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
    for retired in (
        ROOT / "aseprite_resources" / "effects" / "jinx_get_excited_aura#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "jinx_get_excited_aura#anim.fanim",
        ROOT / "aseprite_resources" / "effects" / "jinx_fishbones_mode_aura#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "jinx_fishbones_mode_aura#anim.fanim",
    ):
        if retired.exists():
            fail(f"{retired.relative_to(ROOT)} is retired; Jinx form/ultimate state must not attach VFX to the actor body")
    for effect_name in (
        "jinx_minigun_bullet",
        "jinx_rocket_attack",
        "jinx_zap",
        "jinx_flame_chompers",
        "jinx_super_mega_death_rocket",
        "jinx_switcheroo",
        "jinx_rocket_explosion",
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
    assert_jinx_r_big_projectile()

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
            if action in {"skill2", "ult"} and body_height < 36:
                fail(f"Jinx {action} frame {index} lost the actor body to a projectile/effect-only frame")
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
    all_jinx_strings = set(walk_strings(jinx))
    if "test_mod_jinx_fishbones_visual" in all_jinx_strings or "jinx_fishbones_mode_aura" in all_jinx_strings:
        fail("Jinx Fishbones form must not attach a body overlay; Switcheroo should only change the attack mode")
    if "test_mod_jinx_get_excited" in set(walk_strings(jinx.get("view_buffs", []))):
        fail("Jinx R/Get Excited must not attach a model-deforming actor aura")

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
    if buff_refs:
        fail(f"Jinx must not define actor-attached view_buffs while model overlays are unstable, got {sorted(buff_refs)}")
    for name, expected in JINX_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/jinx.data_champion buff {name} must reference {expected}")

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


def check_darius_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_display_names = {
        "en": "Darius",
        "zh-hans": "\u8bfa\u514b\u8428\u65af\u4e4b\u624b",
        "zh-hant": "\u8afe\u514b\u85a9\u65af\u4e4b\u624b",
        "ko": "Darius",
        "ja": "Darius",
    }
    expected_terms = {
        "en": ("Hemorrhage", "Hand of Noxus", "Decimate", "Apprehend", "Crippling Strike", "Noxian Guillotine"),
        "zh-hans": ("\u8bfa\u624b", "\u51fa\u8840", "\u5927\u6740\u56db\u65b9", "\u65e0\u60c5\u94c1\u624b", "\u81f4\u6b8b\u6253\u51fb", "\u8bfa\u514b\u8428\u65af\u65ad\u5934\u53f0"),
        "zh-hant": ("\u8afe\u624b", "\u51fa\u8840", "\u5927\u6bba\u56db\u65b9", "\u7121\u60c5\u9435\u624b", "\u81f4\u6b98\u6253\u64ca", "\u8afe\u514b\u85a9\u65af\u65b7\u982d\u53f0"),
    }
    for locale, expected_name in expected_display_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for darius_id in DARIUS_IDS:
            row = descriptions.get(darius_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {darius_id}")
            name = str(row.get("name", ""))
            if name != expected_name:
                fail(f"text/champion.i18n locale {locale} {darius_id}.name must be short display name {expected_name!r}")
            if locale in {"zh-hans", "zh-hant"} and any(alias in name for alias in ("Darius", "\u8bfa\u624b", "\u8afe\u624b")):
                fail(f"text/champion.i18n locale {locale} {darius_id}.name must not include search aliases")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "\ufffd" in value or "\u7e5d" in value:
                    fail(f"text/champion.i18n locale {locale} {darius_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("attack", "skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {darius_id} missing term {term!r}")

    for darius_id in DARIUS_IDS:
        view = entries.get(darius_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{darius_id}")
        if view.get("face", {}).get("x") != 2 or view.get("face", {}).get("y") != -12:
            fail(f"style entry {darius_id}.face must recenter Darius side-card standing portrait to x=2,y=-12")
        if view.get("center", {}).get("x") != 0 or view.get("center", {}).get("y") != -12:
            fail(f"style entry {darius_id}.center must recenter Darius exchange standing display to x=0,y=-12")
    assert_compact_idle_bottom_safety("darius")

    for path in (
        ROOT / "champion" / "darius.data_champion",
        ROOT / "aseprite_resources" / "champions" / "darius#sheet.png",
        ROOT / "aseprite_resources" / "champions" / "darius#anim.fanim",
        ROOT / "icons" / "darius_skill.png",
        ROOT / "icons" / "darius_skill2.png",
        ROOT / "icons" / "darius_ult.png",
        ROOT / "qa" / "darius_official_audio_sources.json",
    ):
        require_file(path)
        if path.suffix == ".png":
            require_no_green_residue(path)

    for icon_path in (
        ROOT / "icons" / "darius_skill.png",
        ROOT / "icons" / "darius_skill2.png",
        ROOT / "icons" / "darius_ult.png",
    ):
        width, height, rgba = load_rgba(icon_path)
        if (width, height) != (64, 64):
            fail(f"{icon_path.relative_to(ROOT)} must be a polished 64x64 generated skill icon")
        visible_pixels = 0
        red_or_steel_pixels = 0
        colors: set[tuple[int, int, int, int]] = set()
        for i in range(width * height):
            pixel = tuple(rgba[i * 4 : i * 4 + 4])
            colors.add(pixel)
            r, g, b, a = pixel
            if not a:
                continue
            visible_pixels += 1
            if (r > 85 and r > g * 1.15 and r > b * 0.9) or (abs(r - g) < 28 and abs(g - b) < 35 and r > 55):
                red_or_steel_pixels += 1
        if visible_pixels < 3000 or len(colors) < 450:
            fail(f"{icon_path.relative_to(ROOT)} must be detailed image-generated icon art, not a flat VFX thumbnail")
        if red_or_steel_pixels < max(700, visible_pixels // 6):
            fail(f"{icon_path.relative_to(ROOT)} must keep Darius's red/steel Noxian icon palette")

    effect_tags = {
        "darius_attack_slash": "slash",
        "darius_bleed_apply": "hit",
        "darius_noxian_might_aura": "loop",
        "darius_decimate": "swing",
        "darius_decimate_heal": "heal",
        "darius_apprehend": "chain",
        "darius_crippling_strike": "hit",
        "darius_noxian_guillotine": "cast",
        "darius_noxian_guillotine_hit": "hit",
    }
    for effect_name, required_tag in effect_tags.items():
        sheet = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#sheet.png"
        fanim_path = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#anim.fanim"
        require_file(sheet)
        require_file(fanim_path)
        require_no_green_residue(sheet)
        fanim = load_json(fanim_path)
        frames = fanim.get("anims", {}).get(required_tag, {}).get("frames") if isinstance(fanim, dict) else None
        if not isinstance(frames, list) or len(frames) < 5:
            fail(f"{fanim_path.relative_to(ROOT)} must expose tag {required_tag!r} with at least five readable frames")
        width, height, rgba = load_rgba(sheet)
        visible_pixels = 0
        red_pixels = 0
        for i in range(width * height):
            r = rgba[i * 4]
            g = rgba[i * 4 + 1]
            b = rgba[i * 4 + 2]
            a = rgba[i * 4 + 3]
            if not a:
                continue
            visible_pixels += 1
            if r > 95 and r > g * 1.25 and r > b * 0.75:
                red_pixels += 1
        if visible_pixels < 30:
            fail(f"{sheet.relative_to(ROOT)} must contain a visible generated Darius effect")
        if effect_name not in {"darius_decimate_heal"} and red_pixels < max(20, visible_pixels // 10):
            fail(f"{sheet.relative_to(ROOT)} must keep Darius's red-black Noxian VFX palette")

    assert_generated_vfx_volume(
        ROOT / "aseprite_resources" / "effects" / "darius_apprehend#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "darius_apprehend#anim.fanim",
        "chain",
        "Darius Apprehend axe-pull VFX",
        min_visible=1500,
        min_color_bins=800,
        min_height=54,
        min_fill_ratio=0.38,
        max_width=150,
    )
    darius_axe_palette = collect_weapon_palette_from_rect(
        ROOT / "aseprite_resources" / "champions" / "darius#sheet.png",
        (1197, 3, 38, 30),
    )
    if len(darius_axe_palette) < 80:
        fail("Darius current axe palette could not be sampled; Apprehend VFX cannot prove it uses the model weapon")
    apprehend_fanim = load_json(ROOT / "aseprite_resources" / "effects" / "darius_apprehend#anim.fanim")
    apprehend_frames = apprehend_fanim.get("anims", {}).get("chain", {}).get("frames")
    apprehend_width, _apprehend_height, apprehend_rgba = load_rgba(
        ROOT / "aseprite_resources" / "effects" / "darius_apprehend#sheet.png"
    )
    if not isinstance(apprehend_frames, list):
        fail("Darius Apprehend fanim must expose chain frames")
    for index, frame in enumerate(apprehend_frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict):
            fail(f"Darius Apprehend frame {index} missing frame data")
        rect = (
            int(round(float(data.get("x", -1)))),
            int(round(float(data.get("y", -1)))),
            int(round(float(data.get("w", 0)))),
            int(round(float(data.get("h", 0)))),
        )
        matches = count_palette_matches_in_rect(
            apprehend_rgba,
            apprehend_width,
            rect,
            darius_axe_palette,
            tolerance=28,
        )
        if matches < 900:
            fail(
                f"Darius Apprehend frame {index} has only {matches} pixels matching the current axe palette; "
                "E must use Darius's held weapon, not a generic generated axe"
            )

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "darius#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "darius#sheet.png"
    )
    expected_counts = {
        "idle": 8,
        "run": 10,
        "attack": 8,
        "skill": 8,
        "skill2": 8,
        "ult": 6,
        "hit": 1,
        "dead": 1,
    }
    expected_durations = {
        "idle": 0.12,
        "run": 0.11,
        "attack": 0.07,
        "skill": 0.075,
        "skill2": 0.07,
        "ult": 0.09,
        "hit": 0.12,
        "dead": 0.2,
    }
    action_hashes: dict[str, list[str]] = {}
    action_bboxes: dict[str, list[tuple[int, int, int, int]]] = {}
    for action in DARIUS_CORE_ACTIONS:
        frames = fanim.get("anims", {}).get(action, {}).get("frames")
        if not isinstance(frames, list) or len(frames) != expected_counts[action]:
            fail(f"Darius {action} animation must have {expected_counts[action]} frames")
        action_hashes[action] = []
        action_bboxes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Darius {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != DARIUS_FRAME_SIZE:
                fail(f"Darius {action} frame {index} must use the 57x54 actor frame")
            if frame.get("duration") != expected_durations[action]:
                fail(f"Darius {action} frame {index} must keep duration {expected_durations[action]}")
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            if x < 0 or y < 0 or x + w > sheet_width or y + h > sheet_height:
                fail(f"Darius {action} frame {index} points outside darius#sheet.png")
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Darius {action} frame {index} is blank")
            action_bboxes[action].append(bbox)
            action_hashes[action].append(alpha_frame_hash(sheet_alpha, sheet_width, (x, y, w, h)))
            body_height = bbox[3] - bbox[1]
            body_width = bbox[2] - bbox[0]
            bottom_safe = h - bbox[3]
            if action != "dead" and body_height > 49:
                fail(f"Darius {action} frame {index} body height {body_height}px is too large for UI/battle labels")
            if action not in {"dead", "hit"} and body_height < 33:
                fail(f"Darius {action} frame {index} body height {body_height}px is too small for a readable Noxian silhouette")
            if action == "ult" and body_width < 38:
                fail(f"Darius ult frame {index} collapsed into a warped/dive pose instead of a stable guillotine chop")
            if action != "dead" and bottom_safe < 8:
                fail(f"Darius {action} frame {index} leaves only {bottom_safe}px bottom safety above labels")
        if action in {"attack", "skill", "skill2", "ult"} and len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Darius {action} must have real action motion, not repeated idle frames")

    for action in ("attack", "skill", "skill2", "ult", "hit"):
        if tuple(action_hashes[action][: len(action_hashes["idle"])]) == tuple(action_hashes["idle"][: len(action_hashes[action])]):
            fail(f"Darius {action} must not be a direct copy of idle")

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
        for local_y in range(max(25, bbox[1] + (bbox[3] - bbox[1]) // 2), min(h, bbox[3])):
            row_start = (y + local_y) * sheet_width
            for local_x in range(bbox[0], bbox[2]):
                if 0 <= local_x < w and sheet_alpha[row_start + x + local_x] != 0:
                    lower_points.append((local_x, local_y))
        if len(lower_points) < 45:
            fail(f"Darius run frame {index} has only {len(lower_points)} lower-body pixels; keep the full generated legs visible")
        foot_centers.append(sum(point[0] for point in lower_points) / len(lower_points))
        lower_shapes.add(tuple(lower_points))
    if max(foot_centers) - min(foot_centers) < 1.0:
        fail("Darius run must have weighted walking foot motion, not a sliding/zombie step")
    if len(lower_shapes) < 5:
        fail("Darius run must vary lower-body shapes across the ten-frame walk cycle")

    darius = load_json(ROOT / "champion" / "darius.data_champion")
    strings = set(walk_strings(darius))
    for required in (
        "SwitchByBuff",
        "RangeEffect",
        "LineRangeProjectile",
        "FixedAttack",
        "Heal",
        "Stun",
        "BlockMoveSkill",
        "test_mod_darius_hemo_1",
        "test_mod_darius_hemo_2",
        "test_mod_darius_hemo_3",
        "test_mod_darius_hemo_4",
        "test_mod_darius_hemo_5",
        "test_mod_darius_noxian_might",
        "test_mod_darius_crippling_strike_ready",
        "test_mod_darius_apprehend_slow",
        "test_mod_darius_execution_momentum",
        "test_mod_darius_q_heal",
        "test_mod_darius_ult_voice",
    ):
        if required not in strings:
            fail(f"champion/darius.data_champion must include LoL Darius mechanic token {required}")

    darius_category = darius.get("category")
    assert_no_negative_speed_fields(darius, "champion/darius.data_champion")
    if darius_category != "Melee":
        fail(f"champion/darius.data_champion category must be Melee, got {darius_category!r}")
    tags = set(darius.get("tags", []))
    for tag in ("AD", "Melee", "Tank", "CC"):
        if tag not in tags:
            fail(f"champion/darius.data_champion tags must include {tag}")

    attack_effect = darius.get("attack", {}).get("effect")
    if not isinstance(attack_effect, dict) or attack_effect.get("type") != "SwitchByBuff":
        fail("Darius attack must branch on Crippling Strike/Noxian Might state")
    if attack_effect.get("buff_name") != "test_mod_darius_crippling_strike_ready":
        fail("Darius attack must first consume test_mod_darius_crippling_strike_ready")
    skill_effect = darius.get("skill", {}).get("effect")
    if not isinstance(skill_effect, dict) or skill_effect.get("type") != "SwitchByBuff":
        fail("Darius Q must branch on Noxian Might for empowered Decimate")
    skill2_strings = set(walk_strings(darius.get("skill2", {})))
    if "test_mod_darius_apprehend" not in skill2_strings or "test_mod_darius_crippling_strike_ready" not in skill2_strings:
        fail("Darius E/W must hook with Apprehend and prime Crippling Strike")
    if darius.get("skill2", {}).get("casting_target") != "EnemyChampion":
        fail("Darius Apprehend must target champions first so AI does not waste the pull read on minions or towers")
    if darius.get("skill2", {}).get("range") != 66000:
        fail("Darius Apprehend must expose enough AI cast range to be seen and used in battle")
    skill2_projectiles = find_effect_nodes(darius.get("skill2", {}), "LineRangeProjectile")
    apprehend = next((node for node in skill2_projectiles if node.get("name") == "test_mod_darius_apprehend"), None)
    if not isinstance(apprehend, dict):
        fail("Darius E/W must fire test_mod_darius_apprehend")
    if apprehend.get("applied_target") != "EnemyChampion":
        fail("Darius Apprehend projectile must apply to enemy champions so the hook visibly pulls heroes")
    if apprehend.get("width") != 24000 or apprehend.get("length") != 66000:
        fail("Darius Apprehend must use a readable one-direction axe-pull lane, not a broad front/back sweep or an invisible needle")
    if apprehend.get("delay") != 5 or apprehend.get("apply") != 14:
        fail("Darius Apprehend timing must keep the axe-chain visible before the pull resolves")
    if "MoveTo" not in set(walk_strings(apprehend)):
        fail("Darius Apprehend must include a MoveTo hit effect so the hook pulls/locks targets near Darius instead of only drawing a chain")
    move_to_nodes = find_effect_nodes(apprehend, "MoveTo")
    if not move_to_nodes or move_to_nodes[0].get("range") != 9000 or move_to_nodes[0].get("speed") != 4800:
        fail("Darius Apprehend MoveTo must pull targets tightly in front of Darius without warping the actor body")
    if "test_mod_darius_apprehend_cast_vfx" in skill2_strings:
        fail("Darius Apprehend must not also play a caster-follow copy of the chain; that creates the double/front-back hook read")
    if "Knockback" in skill2_strings:
        fail("Darius Apprehend must not use data-only Knockback; negative speed breaks loading and positive speed pushes targets away")
    ult_strings = set(walk_strings(darius.get("ult", {})))
    if "test_mod_darius_hemo_5" not in ult_strings or "test_mod_darius_noxian_might" not in ult_strings:
        fail("Darius R must scale/branch on Hemorrhage stacks and Noxian Might")
    if "RushMoveToBack" in ult_strings:
        fail("Darius R must be a stable targeted guillotine chop, not a RushMoveToBack actor warp")

    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in darius.get("view_projectiles", [])}
    for name, expected in DARIUS_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/darius.data_champion projectile {name} must reference {expected}")
    projectile_repeat = {item.get("name"): item.get("repeat") for item in darius.get("view_projectiles", [])}
    if projectile_repeat.get("test_mod_darius_apprehend") is not True:
        fail("Darius Apprehend projectile must repeat long enough to read as a pull chain")
    view_effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in darius.get("view_effects", [])}
    for forbidden in DARIUS_FORBIDDEN_VIEW_EFFECTS:
        if forbidden in view_effect_refs:
            fail(f"champion/darius.data_champion view_effect {forbidden} is retired because it creates duplicate caster-following axe chains")
    for name, expected in DARIUS_VIEW_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/darius.data_champion view_effect {name} must reference {expected}")
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in darius.get("view_buffs", [])}
    for name, expected in DARIUS_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/darius.data_champion buff {name} must reference {expected}")

    for action, sfx_names in (
        ("attack", {"test_mod_darius_attack_cast", "test_mod_darius_attack_hit", "test_mod_darius_w_hit", "test_mod_darius_hemo_apply"}),
        ("skill", {"test_mod_darius_q_cast", "test_mod_darius_q_hit", "test_mod_darius_q_heal", "test_mod_darius_hemo_apply"}),
        ("skill2", {"test_mod_darius_e_cast", "test_mod_darius_e_hit"}),
        ("ult", {"test_mod_darius_r_cast", "test_mod_darius_r_hit", "test_mod_darius_ult_voice"}),
    ):
        action_strings = set(walk_strings(darius.get(action, {})))
        missing = sfx_names - action_strings
        if missing:
            fail(f"Darius {action} must trigger sound events {sorted(missing)}")

    assert_official_audio_sources(
        "darius",
        "Darius.wad.client",
        "Darius.wad.client",
        DARIUS_SOUND_MEDIA_IDS,
        DARIUS_SKILL_SOUND_EVENTS,
        DARIUS_SKILL_SOUND_VOLUME_FLOOR,
    )
    official = load_json(ROOT / "qa" / "darius_official_audio_sources.json")
    if "Darius.en_US.wad.client" not in str(official.get("source", "")):
        fail("Darius ult voice source must document the official Darius.en_US.wad.client")


def check_thresh_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_display_names = {
        "en": "Thresh",
        "zh-hans": "\u9524\u77f3",
        "zh-hant": "\u745f\u96f7\u897f",
        "ko": "\uc4f0\ub808\uc26c",
    }
    expected_terms = {
        "en": ("Damnation", "Death Sentence", "Dark Passage", "Flay", "The Box"),
        "zh-hans": ("\u9524\u77f3", "\u5730\u72f1\u8bc5\u5492", "\u6b7b\u4ea1\u5224\u51b3", "\u9b42\u5f15\u4e4b\u706f", "\u5384\u8fd0\u949f\u6446", "\u5e7d\u51a5\u76d1\u7262"),
        "zh-hant": ("\u745f\u96f7\u897f", "\u5730\u7344\u8a5b\u5492", "\u6b7b\u4ea1\u5224\u6c7a", "\u51a5\u71c8\u5f15\u8def", "\u5384\u904b\u9418\u64fa", "\u5e7d\u51a5\u76e3\u7262"),
    }
    for locale, expected_name in expected_display_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for thresh_id in THRESH_IDS:
            row = descriptions.get(thresh_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {thresh_id}")
            name = str(row.get("name", ""))
            if name != expected_name:
                fail(f"text/champion.i18n locale {locale} {thresh_id}.name must be searchable display name {expected_name!r}")
            if locale in {"zh-hans", "zh-hant"} and "Thresh" in name:
                fail(f"text/champion.i18n locale {locale} {thresh_id}.name must stay localized")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "\ufffd" in value or "\u7e5d" in value:
                    fail(f"text/champion.i18n locale {locale} {thresh_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("attack", "skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {thresh_id} missing term {term!r}")

    for thresh_id in THRESH_IDS:
        view = entries.get(thresh_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{thresh_id}")
        if view.get("face", {}).get("x") != 0 or view.get("face", {}).get("y") != -12:
            fail(f"style entry {thresh_id}.face must keep Thresh roster card centered at x=0,y=-12")
        if view.get("center", {}).get("x") != 0 or view.get("center", {}).get("y") != -12:
            fail(f"style entry {thresh_id}.center must keep Thresh exchange standing display centered at x=0,y=-12")
    assert_compact_idle_bottom_safety("thresh")

    for path in (
        ROOT / "champion" / "thresh.data_champion",
        ROOT / "aseprite_resources" / "champions" / "thresh#sheet.png",
        ROOT / "aseprite_resources" / "champions" / "thresh#anim.fanim",
        ROOT / "icons" / "thresh_skill.png",
        ROOT / "icons" / "thresh_skill2.png",
        ROOT / "icons" / "thresh_ult.png",
        ROOT / "qa" / "thresh_official_audio_sources.json",
    ):
        require_file(path)

    for effect_name in (
        "thresh_attack_chain",
        "thresh_attack_empowered",
        "thresh_death_sentence_chain",
        "thresh_death_sentence_hit",
        "thresh_lantern",
        "thresh_flay_sweep",
        "thresh_box",
        "thresh_soul_stack",
    ):
        require_file(ROOT / "aseprite_resources" / "effects" / f"{effect_name}#sheet.png")
        require_file(ROOT / "aseprite_resources" / "effects" / f"{effect_name}#anim.fanim")

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "thresh#anim.fanim")
    sheet_width, sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "thresh#sheet.png"
    )
    expected_counts = {
        "idle": 8,
        "run": 10,
        "attack": 8,
        "skill": 8,
        "skill2": 8,
        "ult": 6,
        "hit": 1,
        "dead": 1,
    }
    action_hashes: dict[str, list[str]] = {}
    action_bboxes: dict[str, list[tuple[int, int, int, int]]] = {}
    for action in THRESH_CORE_ACTIONS:
        frames = fanim.get("anims", {}).get(action, {}).get("frames")
        if not isinstance(frames, list) or len(frames) != expected_counts[action]:
            fail(f"Thresh {action} animation must have {expected_counts[action]} frames")
        action_hashes[action] = []
        action_bboxes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Thresh {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != THRESH_FRAME_SIZE:
                fail(f"Thresh {action} frame {index} must use the 57x54 actor frame")
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            if x < 0 or y < 0 or x + w > sheet_width or y + h > sheet_height:
                fail(f"Thresh {action} frame {index} points outside thresh#sheet.png")
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Thresh {action} frame {index} is blank")
            action_bboxes[action].append(bbox)
            action_hashes[action].append(alpha_frame_hash(sheet_alpha, sheet_width, (x, y, w, h)))
            body_height = bbox[3] - bbox[1]
            body_width = bbox[2] - bbox[0]
            bottom_safe = h - bbox[3]
            if action != "dead" and body_height > 43:
                fail(f"Thresh {action} frame {index} body height {body_height}px is too large for UI/battle labels")
            min_body_height = 38 if action == "idle" else 37 if action == "run" else 40
            if action != "dead" and body_height < min_body_height:
                fail(f"Thresh {action} frame {index} body height {body_height}px is too small for readable Chain Warden silhouette")
            if action != "dead" and body_width > THRESH_MAX_BODY_WIDTH:
                fail(f"Thresh {action} frame {index} width {body_width}px is too wide; keep hooks/flays in separate VFX")
            if bottom_safe < THRESH_MIN_BOTTOM_SAFE:
                fail(f"Thresh {action} frame {index} leaves only {bottom_safe}px bottom safety above labels")
            if action == "run" and frame.get("duration") != 0.12:
                fail("Thresh run must use calmer 0.12s walking timing")
        if action in {"attack", "skill", "skill2", "ult"} and len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Thresh {action} must have real action motion, not repeated idle frames")

    run_bboxes = action_bboxes["run"]
    run_widths = [bbox[2] - bbox[0] for bbox in run_bboxes]
    run_heights = [bbox[3] - bbox[1] for bbox in run_bboxes]
    if max(run_widths) - min(run_widths) > 16:
        fail("Thresh run width range is too unstable; remove actor-embedded hook/flay sweeps from movement frames")
    if max(run_heights) - min(run_heights) > 5:
        fail("Thresh run height range is too unstable; movement must keep one body scale class")

    for action in ("attack", "skill", "skill2", "ult", "hit"):
        if tuple(action_hashes[action][: len(action_hashes["idle"])]) == tuple(action_hashes["idle"][: len(action_hashes[action])]):
            fail(f"Thresh {action} must not be a direct copy of idle")

    thresh = load_json(ROOT / "champion" / "thresh.data_champion")
    strings = set(walk_strings(thresh))
    for required in (
        "SwitchByBuff",
        "LinearProjectile",
        "RangeEffect",
        "RangePeriodProjectile",
        "Shield",
        "Stun",
        "Knockback",
        "BlockMoveSkill",
        "Permanent",
        "test_mod_thresh_death_sentence_chain",
        "test_mod_thresh_lantern_visual",
        "test_mod_thresh_flay_sweep",
        "test_mod_thresh_box_field",
        "test_mod_thresh_soul_stack",
        "test_mod_thresh_soul_gain",
        "test_mod_thresh_ult_voice",
    ):
        if required not in strings:
            fail(f"champion/thresh.data_champion must include LoL Thresh mechanic token {required}")

    skill_effect = thresh.get("skill", {}).get("effect")
    if not isinstance(skill_effect, dict) or skill_effect.get("type") != "Combine":
        fail("Thresh Q must be a single Death Sentence combine, not a copied skill template")
    q_strings = set(walk_strings(skill_effect))
    if "RushMoveToBack" in q_strings:
        fail("Thresh Q first version must not auto-recast/dash after hook impact")
    if "MoveTo" not in q_strings:
        fail("Thresh Q must include a MoveTo hit effect so Death Sentence pulls/locks the hooked target near Thresh")
    if "test_mod_thresh_q_cast" not in q_strings or "test_mod_thresh_q_hit" not in q_strings:
        fail("Thresh Q must trigger official cast and hit sound events")
    for forbidden in THRESH_FORBIDDEN_CASTER_FOLLOW_VFX:
        if forbidden in strings:
            fail(f"Thresh must not use actor-following cast VFX {forbidden}; keep body stable and play separate projectile/field VFX")

    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in thresh.get("view_projectiles", [])}
    for name, expected in THRESH_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/thresh.data_champion projectile {name} must reference {expected}")
    projectile_repeat = {item.get("name"): item.get("repeat") for item in thresh.get("view_projectiles", [])}
    if projectile_repeat.get("test_mod_thresh_death_sentence_chain") is not True:
        fail("Thresh Death Sentence chain projectile must repeat so the hook does not vanish mid-flight")
    view_effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in thresh.get("view_effects", [])}
    view_effect_types = {item.get("name"): item.get("type") for item in thresh.get("view_effects", [])}
    for forbidden in THRESH_FORBIDDEN_CASTER_FOLLOW_VFX:
        if forbidden in view_effect_refs:
            fail(f"champion/thresh.data_champion view_effect {forbidden} is retired because it creates duplicate actor-following VFX")
    for name, expected in THRESH_VIEW_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/thresh.data_champion view_effect {name} must reference {expected}")
    for name in ("test_mod_thresh_box", "test_mod_thresh_box_field"):
        if view_effect_types.get(name) != "LoopAnimation":
            fail(f"Thresh {name} must be LoopAnimation so The Box does not vanish immediately")
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in thresh.get("view_buffs", [])}
    for name, expected in THRESH_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/thresh.data_champion buff {name} must reference {expected}")

    skill2_projectiles = find_effect_nodes(thresh.get("skill2", {}), "LineRangeProjectile")
    flay = next((node for node in skill2_projectiles if node.get("name") == "test_mod_thresh_flay_sweep"), None)
    if not isinstance(flay, dict):
        fail("Thresh skill2 must fire the Flay sweep projectile after the lantern shield")
    if flay.get("applied_target") != "EnemyWithoutTower":
        fail("Thresh Flay must target enemies only; W shield must not create duplicate actor-following hits on allies")
    knockback_nodes = find_effect_nodes(flay, "Knockback")
    if not any(int(node.get("speed", 0)) >= 2000 and int(node.get("tick", 0)) >= 12 for node in knockback_nodes):
        fail("Thresh Flay must use a visible Knockback of at least speed=2000 and tick=12 so enemies are actually pushed")

    for action, sfx_names in (
        ("skill", {"test_mod_thresh_q_cast", "test_mod_thresh_q_hit"}),
        ("skill2", {"test_mod_thresh_lantern_cast", "test_mod_thresh_lantern_shield", "test_mod_thresh_e_cast", "test_mod_thresh_e_hit"}),
        ("ult", {"test_mod_thresh_r_cast", "test_mod_thresh_r_hit", "test_mod_thresh_ult_voice"}),
    ):
        action_strings = set(walk_strings(thresh.get(action, {})))
        missing = sfx_names - action_strings
        if missing:
            fail(f"Thresh {action} must trigger sound events {sorted(missing)}")

    thresh_ult = thresh.get("ult", {})
    if thresh_ult.get("casting_type") != "Targeting" or thresh_ult.get("casting_target") != "EnemyChampion":
        fail("Thresh R must use EnemyChampion targeting so AI can actually choose The Box")
    if int(thresh_ult.get("range", 0)) < 60000:
        fail("Thresh R must expose a target range of at least 60000; range=0 makes AI skip The Box")
    if int(thresh_ult.get("cooltime", 999999)) > 3000:
        fail("Thresh R cooldown must stay at or below 3000 ticks so it appears during normal games")
    ult_range_effects = [
        node for node in find_effect_nodes(thresh_ult, "RangeEffect")
        if node.get("apply_type") == "AroundCaster" and node.get("target") == "EnemyWithoutTower"
    ]
    if not ult_range_effects:
        fail("Thresh R must still place The Box around Thresh on the ground, not as a detached target effect")

    chain_fanim = load_json(ROOT / "aseprite_resources" / "effects" / "thresh_death_sentence_chain#anim.fanim")
    chain_frames = chain_fanim.get("anims", {}).get("chain", {}).get("frames")
    if not isinstance(chain_frames, list):
        fail("Thresh Death Sentence chain fanim must expose chain frames")
    chain_total_duration = sum(float(frame.get("duration", 0)) for frame in chain_frames)
    if chain_total_duration < 0.72:
        fail("Thresh Death Sentence chain animation is too short and can disappear before the hook reaches target")
    assert_generated_vfx_volume(
        ROOT / "aseprite_resources" / "effects" / "thresh_death_sentence_chain#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "thresh_death_sentence_chain#anim.fanim",
        "chain",
        "Thresh Death Sentence hook VFX",
        min_visible=3600,
        min_color_bins=1200,
        min_height=56,
        min_fill_ratio=0.42,
        max_width=178,
    )
    chain_width, _chain_height, chain_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "effects" / "thresh_death_sentence_chain#sheet.png"
    )
    for index, frame in enumerate(chain_frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict):
            fail(f"Thresh Death Sentence chain frame {index} missing frame data")
        x = int(round(float(data.get("x", -1))))
        y = int(round(float(data.get("y", -1))))
        w = int(round(float(data.get("w", 0))))
        h = int(round(float(data.get("h", 0))))
        bbox = alpha_bbox_in_rect(chain_alpha, chain_width, (x, y, w, h))
        if bbox is None:
            fail(f"Thresh Death Sentence chain frame {index} is blank")
        left_body_pixels = alpha_visible_pixels_in_rect(chain_alpha, chain_width, (x, y, min(57, w), min(54, h)))
        if left_body_pixels > 2400:
            fail(
                f"Thresh Death Sentence chain frame {index} has {left_body_pixels} pixels in the actor-body zone; "
                "Q must stay a separate hook/soul-fire projectile, not a duplicate Thresh model"
            )
    lantern_fanim = load_json(ROOT / "aseprite_resources" / "effects" / "thresh_lantern#anim.fanim")
    lantern_frames = lantern_fanim.get("anims", {}).get("loop", {}).get("frames")
    if not isinstance(lantern_frames, list):
        fail("Thresh lantern fanim must expose loop frames")
    lantern_sheet = ROOT / "aseprite_resources" / "effects" / "thresh_lantern#sheet.png"
    lantern_width, _lantern_height, lantern_rgba = load_rgba(lantern_sheet)
    _lantern_width_alpha, _lantern_height_alpha, lantern_alpha = load_rgba_alpha(lantern_sheet)
    for index, frame in enumerate(lantern_frames):
        data = frame.get("data") if isinstance(frame, dict) else None
        if not isinstance(data, dict):
            fail(f"Thresh lantern frame {index} missing frame data")
        x = int(round(float(data.get("x", -1))))
        y = int(round(float(data.get("y", -1))))
        w = int(round(float(data.get("w", 0))))
        h = int(round(float(data.get("h", 0))))
        if (w, h) != (64, 64):
            fail(f"Thresh lantern frame {index} must stay a 64x64 lantern-only buff cell")
        left_edge_pixels = alpha_visible_pixels_in_rect(lantern_alpha, lantern_width, (x, y, 16, h))
        if left_edge_pixels > 40:
            fail(
                f"Thresh lantern frame {index} has {left_edge_pixels} pixels on the left actor edge; "
                "Dark Passage must be a lantern effect, not a second Thresh body"
            )
        dark_body_pixels = dark_actor_pixels_in_rect(lantern_rgba, lantern_width, (x, y, 32, h))
        if dark_body_pixels > 240:
            fail(
                f"Thresh lantern frame {index} has {dark_body_pixels} dark actor-like pixels; "
                "remove duplicated hood/body pixels from the lantern buff"
            )
    assert_generated_vfx_volume(
        ROOT / "aseprite_resources" / "effects" / "thresh_flay_sweep#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "thresh_flay_sweep#anim.fanim",
        "sweep",
        "Thresh Flay sweep VFX",
        min_visible=4500,
        min_color_bins=1200,
        min_height=84,
        min_fill_ratio=0.35,
        max_width=150,
    )
    box_field = next(
        (node for node in find_effect_nodes(thresh.get("ult", {}), "RangePeriodProjectile") if node.get("name") == "test_mod_thresh_box_field"),
        None,
    )
    if not isinstance(box_field, dict) or box_field.get("tick", 0) < 300:
        fail("Thresh R field must last at least 300 ticks so The Box reads as a real prison zone")

    assert_official_audio_sources(
        "thresh",
        "Thresh.wad.client",
        "thresh_base_sfx_audio.bnk",
        THRESH_SOUND_MEDIA_IDS,
        THRESH_SKILL_SOUND_EVENTS,
        THRESH_SKILL_SOUND_VOLUME_FLOOR,
    )


def check_viktor_contract(text: dict[str, Any], entries: dict[str, Any]) -> None:
    expected_display_names = {
        "en": "Viktor",
        "zh-hans": "\u7ef4\u514b\u6258",
        "zh-hant": "\u7dad\u514b\u7279",
        "ko": "Viktor",
        "ja": "Viktor",
    }
    expected_terms = {
        "en": ("Herald of the Arcane", "Glorious Evolution", "Hextech Ray", "Gravity Field", "Arcane Storm"),
        "zh-hans": ("\u5965\u672f\u5148\u9a71", "\u673a\u68b0\u5148\u9a71", "\u5149\u8363\u8fdb\u5316", "\u6d77\u514b\u65af\u5c04\u7ebf", "\u91cd\u529b\u573a", "\u5965\u672f\u98ce\u66b4"),
        "zh-hant": ("\u5967\u8853\u5148\u9a45", "\u6a5f\u68b0\u5148\u9a45", "\u5149\u69ae\u9032\u5316", "\u6d77\u514b\u65af\u5c04\u7dda", "\u91cd\u529b\u5834", "\u5967\u8853\u98a8\u66b4"),
    }
    for locale, expected_name in expected_display_names.items():
        descriptions = text.get(locale, {}).get("description")
        if not isinstance(descriptions, dict):
            fail(f"text/champion.i18n locale {locale} missing description object")
        for viktor_id in VIKTOR_IDS:
            row = descriptions.get(viktor_id)
            if not isinstance(row, dict):
                fail(f"text/champion.i18n locale {locale} missing {viktor_id}")
            name = str(row.get("name", ""))
            if name != expected_name:
                fail(f"text/champion.i18n locale {locale} {viktor_id}.name must be short display name {expected_name!r}")
            if locale in {"zh-hans", "zh-hant"} and any(alias in name for alias in ("Viktor", "\u5965\u672f", "\u5967\u8853")):
                fail(f"text/champion.i18n locale {locale} {viktor_id}.name must not include search aliases")
            for key in REQUIRED_DESCRIPTION_KEYS:
                value = str(row.get(key, ""))
                if "??" in value or "\ufffd" in value or "\u7e5d" in value:
                    fail(f"text/champion.i18n locale {locale} {viktor_id}.{key} still contains corrupted text")
            for term in expected_terms.get(locale, ()):
                if not any(term in str(row.get(key, "")) for key in ("attack", "skill", "skill2", "ult")):
                    fail(f"text/champion.i18n locale {locale} {viktor_id} missing term {term!r}")

    for viktor_id in VIKTOR_IDS:
        view = entries.get(viktor_id)
        if not isinstance(view, dict):
            fail(f"style/champion_view.champion_view missing entries.{viktor_id}")
        if view.get("face", {}).get("x") != 0 or view.get("face", {}).get("y") != -28:
            fail(f"style entry {viktor_id}.face must keep Viktor compact HUD/scoreboard portrait at x=0,y=-28")
        if view.get("center", {}).get("x") != 0 or view.get("center", {}).get("y") != -12:
            fail(f"style entry {viktor_id}.center must recenter Viktor exchange standing display to x=0,y=-12")
    assert_compact_idle_bottom_safety("viktor")

    for path in (
        ROOT / "champion" / "viktor.data_champion",
        ROOT / "aseprite_resources" / "champions" / "viktor#sheet.png",
        ROOT / "aseprite_resources" / "champions" / "viktor#anim.fanim",
        ROOT / "icons" / "viktor_skill.png",
        ROOT / "icons" / "viktor_skill2.png",
        ROOT / "icons" / "viktor_ult.png",
        ROOT / "qa" / "viktor_official_audio_sources.json",
    ):
        require_file(path)
        if path.suffix == ".png":
            require_no_green_residue(path)

    effect_tags = {
        "viktor_attack_projectile": "projectile",
        "viktor_laser": "laser",
        "viktor_laser_aftershock": "burn",
        "viktor_gravity_field": "gravity_field",
        "viktor_chaos_storm": "chaos_storm",
        "viktor_siphon_shield": "shield",
        "viktor_evolution_aura": "ray",
        "viktor_storm_impact": "impact",
    }
    for effect_name, required_tag in effect_tags.items():
        sheet = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#sheet.png"
        fanim_path = ROOT / "aseprite_resources" / "effects" / f"{effect_name}#anim.fanim"
        require_file(sheet)
        require_file(fanim_path)
        require_no_green_residue(sheet)
        fanim_effect = load_json(fanim_path)
        frames = fanim_effect.get("anims", {}).get(required_tag, {}).get("frames") if isinstance(fanim_effect, dict) else None
        if not isinstance(frames, list) or len(frames) < 4:
            fail(f"{fanim_path.relative_to(ROOT)} must expose tag {required_tag!r} with at least four readable frames")
        width, height, rgba = load_rgba(sheet)
        visible_pixels = 0
        arcane_pixels = 0
        for i in range(width * height):
            r = rgba[i * 4]
            g = rgba[i * 4 + 1]
            b = rgba[i * 4 + 2]
            a = rgba[i * 4 + 3]
            if not a:
                continue
            visible_pixels += 1
            if b > 85 and (g > 70 or r > 110):
                arcane_pixels += 1
        if visible_pixels < 24:
            fail(f"{sheet.relative_to(ROOT)} must contain a visible Viktor VFX silhouette")
        if arcane_pixels < max(8, visible_pixels // 12):
            fail(f"{sheet.relative_to(ROOT)} must keep Viktor's blue-white arcane palette readable")

    fanim = load_json(ROOT / "aseprite_resources" / "champions" / "viktor#anim.fanim")
    anims = fanim.get("anims") if isinstance(fanim, dict) else None
    if not isinstance(anims, dict):
        fail("aseprite_resources/champions/viktor#anim.fanim must contain anims")
    for retired in ("attackOld", "attackOld2", "skillOld", "skill2Old", "ultOld"):
        if retired in anims:
            fail(f"Viktor actor sheet must not keep retired action tag {retired}")

    sheet_width, _sheet_height, sheet_alpha = load_rgba_alpha(
        ROOT / "aseprite_resources" / "champions" / "viktor#sheet.png"
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
    expected_durations = {
        "idle": (0.11,) * 6,
        "run": (0.11,) * 10,
        "attack": (0.05, 0.05, 0.055, 0.055, 0.06, 0.08),
        "skill": (0.07, 0.08, 0.09, 0.11, 0.18, 0.22),
        "skill2": (0.055, 0.055, 0.06, 0.075, 0.09, 0.105, 0.11),
        "ult": (0.06, 0.06, 0.07, 0.085, 0.105, 0.13, 0.15),
        "hit": (0.1,),
        "dead": (0.2,),
    }
    action_hashes: dict[str, list[str]] = {}
    action_bboxes: dict[str, list[tuple[int, int, int, int]]] = {}
    for action in VIKTOR_CORE_ACTIONS:
        frames = anims.get(action, {}).get("frames") if isinstance(anims.get(action), dict) else None
        if not isinstance(frames, list) or len(frames) != expected_counts[action]:
            fail(f"Viktor {action} animation must have {expected_counts[action]} frames")
        action_hashes[action] = []
        action_bboxes[action] = []
        for index, frame in enumerate(frames):
            data = frame.get("data") if isinstance(frame, dict) else None
            if not isinstance(data, dict):
                fail(f"Viktor {action} frame {index} missing frame data")
            if (data.get("w"), data.get("h")) != VIKTOR_FRAME_SIZE:
                fail(f"Viktor {action} frame {index} must use the 57x54 actor frame")
            if frame.get("duration") != expected_durations[action][index]:
                fail(f"Viktor {action} frame {index} must keep duration {expected_durations[action][index]}")
            x = int(round(float(data.get("x", -1))))
            y = int(round(float(data.get("y", -1))))
            w = int(round(float(data.get("w", 0))))
            h = int(round(float(data.get("h", 0))))
            bbox = alpha_bbox_in_rect(sheet_alpha, sheet_width, (x, y, w, h))
            if bbox is None:
                fail(f"Viktor {action} frame {index} is blank")
            action_bboxes[action].append(bbox)
            action_hashes[action].append(alpha_frame_hash(sheet_alpha, sheet_width, (x, y, w, h)))
            body_height = bbox[3] - bbox[1]
            body_width = bbox[2] - bbox[0]
            bottom_safe = h - bbox[3]
            if action != "dead" and body_height > 47:
                fail(f"Viktor {action} frame {index} body height {body_height}px is too large for UI/battle labels")
            min_body_height = 40 if action == "attack" else 42
            if action != "dead" and body_height < min_body_height:
                fail(f"Viktor {action} frame {index} body height {body_height}px is too small for Herald silhouette")
            if action in {"skill", "skill2", "ult"} and body_width > VIKTOR_MAX_CLEAN_CAST_WIDTH:
                fail(f"Viktor {action} frame {index} width {body_width}px is too wide; keep laser/storm VFX outside the actor body")
            if action != "dead" and bottom_safe < VIKTOR_MIN_BOTTOM_SAFE:
                fail(f"Viktor {action} frame {index} leaves only {bottom_safe}px bottom safety above labels")
        if action in {"attack", "skill", "skill2", "ult"} and len(set(action_hashes[action])) < min(4, len(action_hashes[action])):
            fail(f"Viktor {action} must have real action motion, not repeated idle frames")

    for action in ("attack", "skill", "skill2", "ult", "hit"):
        if tuple(action_hashes[action][: len(action_hashes["idle"])]) == tuple(action_hashes["idle"][: len(action_hashes[action])]):
            fail(f"Viktor {action} must not be a direct copy of idle")

    run_frames = anims.get("run", {}).get("frames")
    assert isinstance(run_frames, list)
    run_bboxes = action_bboxes["run"]
    run_widths = [bbox[2] - bbox[0] for bbox in run_bboxes]
    run_heights = [bbox[3] - bbox[1] for bbox in run_bboxes]
    run_bottoms = [VIKTOR_FRAME_SIZE[1] - bbox[3] for bbox in run_bboxes]
    if max(run_widths) - min(run_widths) > 2:
        fail("Viktor run width range is too unstable; movement must not alternate between body scale classes")
    if max(run_heights) - min(run_heights) > 1:
        fail("Viktor run height range is too unstable; movement must not alternate between crouched/tall actors")
    if max(run_bottoms) - min(run_bottoms) > 1:
        fail("Viktor run bottom anchor is unstable and will overlap labels/health bars")
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
        for local_y in range(max(25, bbox[1] + (bbox[3] - bbox[1]) // 2), min(h, bbox[3])):
            row_start = (y + local_y) * sheet_width
            for local_x in range(bbox[0], bbox[2]):
                if 0 <= local_x < w and sheet_alpha[row_start + x + local_x] != 0:
                    lower_points.append((local_x, local_y))
        if len(lower_points) < 220:
            fail(f"Viktor run frame {index} has only {len(lower_points)} lower-body pixels; keep the full crossed walk visible")
        foot_centers.append(sum(point[0] for point in lower_points) / len(lower_points))
        lower_shapes.add(tuple(lower_points))
    if max(foot_centers) - min(foot_centers) < 0.85:
        fail("Viktor run must keep the original crossed-step rhythm, not a sliding/zombie step")
    if len(lower_shapes) < 7:
        fail("Viktor run must vary lower-body shapes across the ten-frame walk cycle")

    viktor = load_json(ROOT / "champion" / "viktor.data_champion")
    strings = set(walk_strings(viktor))
    for required in (
        "ApAttack",
        "SwitchByBuff",
        "Shield",
        "Stun",
        "BlockMoveSkill",
        "LineRangeProjectile",
        "ParabolicProjectile",
        "RangePeriodProjectile",
        "test_mod_viktor_siphon_empower",
        "test_mod_viktor_evolved_ray",
        "test_mod_viktor_evolved_field",
        "test_mod_viktor_evolved_storm",
        "test_mod_viktor_laser_aftershock",
        "test_mod_viktor_gravity_field",
        "test_mod_viktor_chaos_storm",
        "test_mod_viktor_chaos_storm_duration",
        "test_mod_viktor_storm_impact",
        "test_mod_viktor_evolution",
        "test_mod_viktor_ult_voice",
    ):
        if required not in strings:
            fail(f"champion/viktor.data_champion must include LoL Viktor mechanic token {required}")
    if "Attack" in set(walk_strings(viktor.get("attack", {}))):
        fail("Viktor basic attack must use AP Arcane Pulse, not physical Attack")
    if viktor.get("category") != "Magician":
        fail(f"champion/viktor.data_champion category must remain Magician, got {viktor.get('category')!r}")
    tags = set(viktor.get("tags", []))
    for tag in ("AP", "Range", "Magic"):
        if tag not in tags:
            fail(f"champion/viktor.data_champion tags must include {tag}")
    if "only_to_enemy" in json.dumps(viktor.get("ult", {}), ensure_ascii=False):
        fail("Viktor R must advance Glorious Evolution on cast and must not keep only_to_enemy gates")

    projectile_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in viktor.get("view_projectiles", [])}
    for name, expected in VIKTOR_EFFECT_REFS.items():
        if projectile_refs.get(name) != expected:
            fail(f"champion/viktor.data_champion projectile {name} must reference {expected}")
    projectile_repeat = {item.get("name"): item.get("repeat") for item in viktor.get("view_projectiles", [])}
    for projectile_name in ("test_mod_viktor_laser", "test_mod_viktor_laser_aftershock"):
        if projectile_repeat.get(projectile_name) is not True:
            fail(f"Viktor projectile {projectile_name} must repeat so the laser VFX stays visible for the gameplay window")
    projectile_z = {item.get("name"): item.get("z") for item in viktor.get("view_projectiles", [])}
    for projectile_name in ("test_mod_viktor_laser", "test_mod_viktor_laser_aftershock"):
        z_value = projectile_z.get(projectile_name)
        if not isinstance(z_value, (int, float)) or z_value >= 0:
            fail(f"Viktor projectile {projectile_name} must render on the ground layer with negative z, got {z_value!r}")
    laser_projectiles = [
        node
        for node in find_effect_nodes(viktor.get("skill", {}), "LineRangeProjectile")
        if node.get("name") in {
            "test_mod_viktor_laser",
            "test_mod_viktor_laser_champion_bonus",
            "test_mod_viktor_laser_aftershock",
        }
    ]
    laser_groups = {
        "test_mod_viktor_laser": [node for node in laser_projectiles if node.get("name") == "test_mod_viktor_laser"],
        "test_mod_viktor_laser_champion_bonus": [
            node for node in laser_projectiles if node.get("name") == "test_mod_viktor_laser_champion_bonus"
        ],
        "test_mod_viktor_laser_aftershock": [
            node for node in laser_projectiles if node.get("name") == "test_mod_viktor_laser_aftershock"
        ],
    }
    for projectile_name in ("test_mod_viktor_laser", "test_mod_viktor_laser_champion_bonus"):
        nodes = laser_groups[projectile_name]
        if len(nodes) != 2:
            fail(f"Viktor Hextech Ray must define two {projectile_name} projectiles, one normal and one evolved")
        for node in nodes:
            if node.get("apply", 0) < VIKTOR_LASER_MIN_APPLY:
                fail(f"Viktor {projectile_name} must persist for at least {VIKTOR_LASER_MIN_APPLY} ticks")
            if node.get("delay", 999) > 10:
                fail(f"Viktor {projectile_name} must appear promptly on the ground, got delay {node.get('delay')!r}")
            if node.get("width", 0) < 12000 or node.get("length", 0) < 90000:
                fail(f"Viktor {projectile_name} must keep a broad terrain-line footprint")
    aftershock_nodes = laser_groups["test_mod_viktor_laser_aftershock"]
    if len(aftershock_nodes) != 1:
        fail("Viktor evolved Hextech Ray must define one persistent aftershock ground projectile")
    if aftershock_nodes[0].get("apply", 0) < VIKTOR_AFTERSHOCK_MIN_APPLY:
        fail(f"Viktor laser aftershock must persist for at least {VIKTOR_AFTERSHOCK_MIN_APPLY} ticks")
    view_effect_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in viktor.get("view_effects", [])}
    view_effect_types = {item.get("name"): item.get("type") for item in viktor.get("view_effects", [])}
    for name, expected in VIKTOR_VIEW_EFFECT_REFS.items():
        if view_effect_refs.get(name) != expected:
            fail(f"champion/viktor.data_champion view_effect {name} must reference {expected}")
    for name in ("test_mod_viktor_gravity_field", "test_mod_viktor_chaos_storm"):
        if view_effect_types.get(name) != "LoopAnimation":
            fail(f"Viktor {name} must be LoopAnimation so the field/storm persists instead of flashing once and vanishing")
    if view_effect_types.get("test_mod_viktor_storm_impact") != "Animation":
        fail("Viktor storm impact must remain a one-shot Animation separate from the persistent Chaos Storm loop")
    skill2_top_level = viktor.get("skill2", {}).get("effect", {}).get("effects", [])
    if not isinstance(skill2_top_level, list):
        fail("Viktor skill2 must keep a top-level Combine.effects list")
    for node in skill2_top_level:
        if not isinstance(node, dict):
            continue
        if node.get("type") == "CasterViewEffect" and node.get("name") == "test_mod_viktor_siphon_shield":
            fail("Viktor skill2 must not double-attach the Siphon shield over the actor body")
        if node.get("type") == "ViewEffect" and node.get("name") == "test_mod_viktor_gravity_field":
            fail("Viktor Gravity Field must be spawned from a target-ground anchor, not as a caster-level ViewEffect")
    gravity_anchors = [
        node
        for node in find_effect_nodes(viktor.get("skill2", {}), "ParabolicProjectile")
        if node.get("name") == "test_mod_viktor_gravity_field_anchor"
    ]
    if len(gravity_anchors) != 2:
        fail("Viktor skill2 must use two gravity-field ground anchors, one normal and one evolved")
    for index, anchor in enumerate(gravity_anchors, start=1):
        end_effects = anchor.get("end_effects")
        if not isinstance(end_effects, list):
            fail(f"Viktor gravity anchor {index} must use end_effects for target-ground VFX")
        if not any(item.get("type") == "ViewEffect" and item.get("name") == "test_mod_viktor_gravity_field" for item in end_effects if isinstance(item, dict)):
            fail(f"Viktor gravity anchor {index} must spawn the field ViewEffect at the target point")
        field_pulses = [
            item
            for item in end_effects
            if isinstance(item, dict)
            and item.get("type") == "RangePeriodProjectile"
            and item.get("name") == "test_mod_viktor_gravity_field"
        ]
        if len(field_pulses) != 1:
            fail(f"Viktor gravity anchor {index} must own exactly one ground RangePeriodProjectile pulse")
        if field_pulses[0].get("first_delay", 0) < 15:
            fail("Viktor Gravity Field pulse must wait after the anchor's immediate slow so it does not double-pop on cast")
    storm_direct_names = {"test_mod_viktor_storm_impact", "test_mod_viktor_chaos_storm"}
    for branch_name in ("effect_none", "effect_buff"):
        branch = viktor.get("ult", {}).get("effect", {}).get(branch_name, {})
        branch_effects = branch.get("effects") if isinstance(branch, dict) else None
        if not isinstance(branch_effects, list):
            fail(f"Viktor ult {branch_name} must keep a branch effects list")
        for node in branch_effects:
            if not isinstance(node, dict):
                continue
            if node.get("type") == "ViewEffect" and node.get("name") in storm_direct_names:
                fail(f"Viktor ult {branch_name} must spawn storm VFX from the target-ground anchor, not directly on the caster")
            if node.get("type") == "RangePeriodProjectile" and node.get("name") in storm_direct_names:
                fail(f"Viktor ult {branch_name} must keep storm damage inside the target-ground anchor")
    storm_anchors = [
        node
        for node in find_effect_nodes(viktor.get("ult", {}), "ParabolicProjectile")
        if node.get("name") == "test_mod_viktor_chaos_storm_anchor"
    ]
    if len(storm_anchors) != 2:
        fail("Viktor ult must use two Chaos Storm ground anchors, one normal and one evolved")
    for index, anchor in enumerate(storm_anchors, start=1):
        end_effects = anchor.get("end_effects")
        if not isinstance(end_effects, list):
            fail(f"Viktor Chaos Storm anchor {index} must use end_effects for terrain VFX")
        end_names = {(item.get("type"), item.get("name")) for item in end_effects if isinstance(item, dict)}
        for required_view in (("ViewEffect", "test_mod_viktor_storm_impact"), ("ViewEffect", "test_mod_viktor_chaos_storm")):
            if required_view not in end_names:
                fail(f"Viktor Chaos Storm anchor {index} must spawn {required_view[1]} on the terrain")
        storm_pulses = [
            item
            for item in end_effects
            if isinstance(item, dict)
            and item.get("type") == "RangePeriodProjectile"
            and item.get("name") == "test_mod_viktor_chaos_storm"
        ]
        if len(storm_pulses) != 1:
            fail(f"Viktor Chaos Storm anchor {index} must own exactly one persistent storm pulse")
        if storm_pulses[0].get("tick", 0) < VIKTOR_STORM_MIN_TICKS[index - 1]:
            fail(
                f"Viktor Chaos Storm anchor {index} must persist on terrain for at least "
                f"{VIKTOR_STORM_MIN_TICKS[index - 1]} ticks"
            )
        if storm_pulses[0].get("first_delay") != 20:
            fail("Viktor Chaos Storm pulse must remain delayed until after the impact burst")
    assert_effect_frames_not_edge_cut(
        ROOT / "aseprite_resources" / "effects" / "viktor_gravity_field#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "viktor_gravity_field#anim.fanim",
        "gravity_field",
        "Viktor Gravity Field VFX",
    )
    assert_effect_frames_not_edge_cut(
        ROOT / "aseprite_resources" / "effects" / "viktor_storm_impact#sheet.png",
        ROOT / "aseprite_resources" / "effects" / "viktor_storm_impact#anim.fanim",
        "impact",
        "Viktor Chaos Storm impact VFX",
        max_border_pixels=4,
    )
    buff_refs = {item.get("name"): (item.get("anim"), item.get("tag")) for item in viktor.get("view_buffs", [])}
    for name, expected in VIKTOR_BUFF_REFS.items():
        if buff_refs.get(name) != expected:
            fail(f"champion/viktor.data_champion buff {name} must reference {expected}")

    for action, sfx_names in (
        ("attack", {"test_mod_viktor_attack_cast", "test_mod_viktor_attack_hit", "test_mod_viktor_siphon_empower_hit"}),
        ("skill", {"test_mod_viktor_laser_cast", "test_mod_viktor_laser_hit", "test_mod_viktor_laser_aftershock_hit", "test_mod_viktor_evolution"}),
        ("skill2", {"test_mod_viktor_siphon_cast", "test_mod_viktor_gravity_field_cast", "test_mod_viktor_gravity_field_slow", "test_mod_viktor_evolution"}),
        ("ult", {"test_mod_viktor_chaos_storm_cast", "test_mod_viktor_chaos_storm_duration", "test_mod_viktor_storm_impact", "test_mod_viktor_ult_voice", "test_mod_viktor_evolution"}),
    ):
        action_strings = set(walk_strings(viktor.get(action, {})))
        missing = sfx_names - action_strings
        if missing:
            fail(f"Viktor {action} must trigger sound events {sorted(missing)}")

    assert_official_audio_sources(
        "viktor",
        "Viktor.wad.client",
        "viktor_base_sfx_audio.bnk",
        VIKTOR_SOUND_MEDIA_IDS,
        VIKTOR_SKILL_SOUND_EVENTS,
        VIKTOR_SKILL_SOUND_VOLUME_FLOOR,
    )
    official = load_json(ROOT / "qa" / "viktor_official_audio_sources.json")
    if "Viktor.en_US.wad.client" not in str(official.get("voice_source", "")):
        fail("Viktor ult voice source must document the official Viktor.en_US.wad.client")


def check_champion_visibility() -> None:
    text = load_json(ROOT / "text" / "champion.i18n")
    style = load_json(ROOT / "style" / "champion_view.champion_view")
    entries = style.get("entries")
    if not isinstance(entries, dict):
        fail("style/champion_view.champion_view must contain an entries object")
    check_full_body_compact_portraits(entries)
    check_standard_compact_idle_bottom_safety()

    champion_files = sorted((ROOT / "champion").glob("*.data_champion"))
    stems = {path.stem for path in champion_files}
    if stems != EXPECTED_CHAMPIONS:
        fail(f"champion files mismatch: expected {sorted(EXPECTED_CHAMPIONS)}, got {sorted(stems)}")

    ids: set[str] = set()
    for path in champion_files:
        data = load_json(path)
        check_effect_shapes(path, data)
        check_view_effect_types(path, data)
        assert_no_negative_speed_fields(data, str(path.relative_to(ROOT)))
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
    if f"{MOD_ID}_darius" not in ids:
        fail("Darius encyclopedia chain is missing bo_league_champions_darius")
    if f"{MOD_ID}_kayn" not in ids:
        fail("Kayn encyclopedia chain is missing bo_league_champions_kayn")
    if f"{MOD_ID}_yasuo" not in ids:
        fail("Yasuo encyclopedia chain is missing bo_league_champions_yasuo")
    if f"{MOD_ID}_jinx" not in ids:
        fail("Jinx encyclopedia chain is missing bo_league_champions_jinx")
    if f"{MOD_ID}_thresh" not in ids:
        fail("Thresh encyclopedia chain is missing bo_league_champions_thresh")
    if f"{MOD_ID}_viktor" not in ids:
        fail("Viktor encyclopedia chain is missing bo_league_champions_viktor")
    check_encyclopedia_search_terms(text)
    check_aatrox_rework_contract(text, entries)
    check_darius_contract(text, entries)
    check_kayn_rework_contract(text, entries)
    check_yasuo_contract(text, entries)
    check_jinx_contract(text, entries)
    check_thresh_contract(text, entries)
    check_viktor_contract(text, entries)
    for champion_name in ("aatrox", "darius", "kayn", "thresh", "viktor"):
        assert_static_recall_tags(champion_name)


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
