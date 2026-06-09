# Aatrox Design Rework QA

Date: 2026-06-09

## Scope

This pass treats the earlier `aatrox_cartoon_model` proof, the first design-book battle crop, and the muddy long-sword preview as failed. Those rejected builds made Aatrox read as a crawling red mass or a dark noisy blob in 64 px UI surfaces. This rebuild uses refined image-generated final-scale sources, with Viktor's finished walk cycle as the stability reference.

In scope:

- `aseprite_resources/champions/aatrox#sheet.png`
- `aseprite_resources/champions/aatrox#anim.fanim`
- `aseprite_resources/effects/aatrox_attack_slash#sheet.png`
- `aseprite_resources/effects/aatrox_q1_cleave#sheet.png`
- `aseprite_resources/effects/aatrox_q2_cleave#sheet.png`
- `aseprite_resources/effects/aatrox_q3_cleave#sheet.png`
- `aseprite_resources/effects/aatrox_w_chain#sheet.png`
- `aseprite_resources/effects/aatrox_w_chain_snap#sheet.png`
- `aseprite_resources/effects/aatrox_world_ender_aura#sheet.png`
- `icons/aatrox_skill.png`
- `icons/aatrox_skill2.png`
- `icons/aatrox_ult.png`
- `qa/aatrox_design_rework_asset_matrix.csv`

Preserved:

- `bo_league_champions_aatrox` standalone champion id, with `test_mod_aatrox` retained as a text/style compatibility alias
- `bo_league_champions` mod id and `asset/bo_league_champions/...` asset namespace
- `champion/aatrox.data_champion` legacy sound event names and TFM2-compatible action slots
- existing sprite/icon paths and sound events loaded by the mod

## Published Assets

The published mod keeps only runtime assets plus the CSV matrix:

- asset matrix: `qa/aatrox_design_rework_asset_matrix.csv`

Temporary source, contact, and preview sheets are treated as local diagnostics. They are not committed after the hero rebuild is complete.
CI also fails if `source/` or `qa/` contains committed PNG/JPG/WebP process images.

## Design Checks

- Actor silhouette: compact dark-red demon warrior with readable horns, black armor, red chest mark, clear feet, and a naturally lowered greatsword; idle/run frames do not include flames, wings, smoke, or aura.
- Compact surfaces: Aatrox idle/hit/dead/ult presentation frames are repacked into the original 54x50 display slots, matching Viktor's compact UI scale class so the model sits above the hero name instead of filling the card.
- Run: eight stable cross-step frames follow the Viktor reference principle: upright torso, tiny foot alternation, consistent body height, and bottom-anchor drift of no more than 1 px.
- Attack: body pose uses the refined greatsword swing. Direct `Heal` effects were removed from attack and damaging skills because they caused a visible white flash on the actor after basic attacks.
- Q / `skill`: The Darkin Blade is represented as three delayed line cleaves; the third strike is heavier and knocks enemies airborne.
- Q VFX: the runtime now uses distinct Q1 narrow thrust, Q2 wide cleave, and Q3 heavy smash sheets instead of reusing one generic impact.
- W / `skill2`: Infernal Chains replaces the earlier made-up dash guard. It fires a hooked chain, slows the target, then snaps again for delayed damage and brief control.
- W VFX: launch and snap use separate chain sheets, so the delayed pull-back reads differently from the first projectile.
- E / Umbral Dash: TFM2 has only three visible active skill slots, so E is not presented as a fake fourth button. Aatrox's sustain identity is represented by World Ender's vamp window.
- R / `ult`: World Ender grants attack damage, movement speed, and vamp; it briefly fears nearby enemies on cast. It no longer gives unrelated armor, magic resist, or attack-speed padding.
- R VFX: World Ender buff uses a restrained 64x64 wing/rune aura rendered behind the actor; idle, run, hit, dead, and the encyclopedia body stay clean.
- Hit/dead/ult: these reuse the stable refined idle body so card, side-list, battle HUD, and exchange surfaces do not show the previous noisy red blob.
- Text: zh-hans and zh-hant Aatrox rows are readable Chinese, with CI blocking `??` corruption for both the new id and the legacy `test_mod_aatrox` alias.
- Icons: Q/W/R icons are rebuilt from the refined LoL ability image-gen source, green-key removed, dark framed, and exported at the existing 24x24 contract.

## Remaining Manual QA

- Enable the LOL mod in-game and confirm Aatrox in roster/card, side HUD, battle idle/run, Q hit, W chain, and R buff.
- In live battle, confirm run reads like a small upright cross-step and not a crawl or oversized lunge.
- In live battle, verify Q visual length matches `LineRangeProjectile` direction and does not read as an area circle.
- In live battle, verify W reads as Infernal Chains and not as a generic dash.
- Confirm R aura does not cover the health bar or make the compact portrait unreadable.
