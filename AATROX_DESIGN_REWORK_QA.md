# Aatrox Design Rework QA

Date: 2026-06-09

## Scope

This pass treats the earlier `aatrox_cartoon_model` proof and the first design-book battle crop as failed. The rejected battle crop made Aatrox read as a crawling red mass with oversized fire/body motion. This rebuild uses a new stable cross-step source, with Viktor's finished walk cycle as the stability reference.

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
- final motion contact: `qa/aatrox_post_stable_motion_contact.png`
- Viktor reference contact: `qa/viktor_motion_contact.png`

## Design Checks

- Actor silhouette: compact dark-red demon warrior with readable horns, black armor, red cuts, and a shortened close-held sword; idle/run frames do not include flames, wings, smoke, or aura.
- Run: eight stable cross-step frames follow the Viktor reference principle: upright torso, tiny foot alternation, consistent body height, and bottom-anchor drift of no more than 1 px.
- Attack: body pose uses the generated greatsword swing, with a separate compact red-black caster-follow slash.
- Q: `aatrox_q_impact` is a six-frame forward ground-crack cleave generated as a readable line effect, not a round explosion.
- E: `skill2` uses upright cross-step body frames plus a low-opacity red-black dash trail; the actor body does not stretch into a horizontal crawl pose.
- R: World Ender buff uses a separate low-opacity wing/arc aura; idle, run, hit, dead, and the encyclopedia body stay clean.
- Hit/dead/ult: these reuse the stable idle body so card, side-list, and battle HUD surfaces do not show an inflated monster pose.
- Icons: Q/E/R icons are rebuilt from new image-gen source, green-key removed, dark framed, and exported at the existing 24x24 contract.

## Remaining Manual QA

- Enable the LOL mod in-game and confirm Aatrox in roster/card, side HUD, battle idle/run, Q hit, E dash, and R buff.
- In live battle, confirm run reads like a small upright cross-step and not a crawl or oversized lunge.
- In live battle, verify Q visual length matches `LineRangeProjectile` direction and does not read as an area circle.
- Confirm R aura does not cover the health bar or make the compact portrait unreadable.
