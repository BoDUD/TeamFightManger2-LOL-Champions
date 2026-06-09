# Aatrox Design Rework QA

Date: 2026-06-09

## Scope

This pass treats the earlier `aatrox_cartoon_model` proof as failed and rebuilds Aatrox from fresh design-book image-gen source assets.

In scope:

- `aseprite_resources/champions/aatrox#sheet.png`
- `aseprite_resources/champions/aatrox#anim.fanim`
- `aseprite_resources/effects/aatrox_attack_slash#sheet.png`
- `aseprite_resources/effects/aatrox_q_impact#sheet.png`
- `aseprite_resources/effects/aatrox_ult_aura#sheet.png`
- `icons/aatrox_skill.png`
- `icons/aatrox_skill2.png`
- `icons/aatrox_ult.png`
- `source/aatrox_design_rework/`
- `tools/build_aatrox_design_rework_assets.py`
- `qa/aatrox_design_rework_asset_matrix.csv`

Preserved:

- `bo_league_champions_aatrox` standalone champion id, with `test_mod_aatrox` retained as a text/style compatibility alias
- `bo_league_champions` mod id and `asset/bo_league_champions/...` asset namespace
- `champion/aatrox.data_champion` gameplay timings, damage, ranges, cooldowns, legacy sound/VFX event names, and skill logic
- existing sprite/icon/effect paths loaded by the mod
- existing `style/champion_view.champion_view` offsets

## Build

```powershell
python tools\build_aatrox_design_rework_assets.py
```

The build produced:

- actor contact: `source/aatrox_design_rework/aatrox_design_actor_contact.png`
- icon contact: `source/aatrox_design_rework/aatrox_design_icon_contact.png`
- VFX contact: `source/aatrox_design_rework/aatrox_design_vfx_contact.png`
- asset matrix: `qa/aatrox_design_rework_asset_matrix.csv`

## Design Checks

- Actor silhouette: compact dark-red demon warrior with readable horns, black armor, glowing red cuts, and oversized sword.
- Run: `run_a` / `run_b` source poses are used with stronger offsets so the walk/run reads at TFM2 scale without changing frame count.
- Attack: body pose uses the generated greatsword swing, with a separate compact red-black caster-follow slash.
- Q: `aatrox_q_impact` is a six-frame forward ground-crack cleave, not a round explosion.
- E: red-black dash trail is composited into the existing `skill2` body frames without changing `champion/aatrox.data_champion`.
- R: World Ender buff uses a lower-opacity ring/wing aura to show transformation while reducing face/body obstruction.
- Hit/dead/ult: these now use generated hit, dead, and ult source poses rather than reusing idle.
- Icons: Q/E/R icons are rebuilt from new image-gen source, green-key removed, dark framed, and exported at the existing 24x24 contract.

## Remaining Manual QA

- Enable the LOL mod in-game and confirm Aatrox in roster/card, side HUD, battle idle/run, Q hit, E dash, and R buff.
- In live battle, verify Q visual length matches `LineRangeProjectile` direction and does not read as an area circle.
- Confirm R aura does not cover the health bar or make the compact portrait unreadable.
