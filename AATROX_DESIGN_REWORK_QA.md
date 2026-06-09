# Aatrox Design Rework QA

Date: 2026-06-09

## Scope

This pass treats the earlier `aatrox_cartoon_model` proof, the first design-book battle crop, and the muddy long-sword preview as failed. Those rejected builds made Aatrox read as a crawling red mass or a dark noisy blob in 64 px UI surfaces. This rebuild uses refined image-generated final-scale sources, with Viktor's finished walk cycle as the stability reference.

In scope:

- `aseprite_resources/champions/aatrox#sheet.png`
- `aseprite_resources/champions/aatrox#anim.fanim`
- `aseprite_resources/effects/aatrox_attack_slash#sheet.png`
- `aseprite_resources/effects/aatrox_q_impact#sheet.png`
- `aseprite_resources/effects/aatrox_infernal_chains#sheet.png`
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
- `champion/aatrox.data_champion` legacy sound event names and TFM2-compatible action slots
- existing sprite/icon/effect paths loaded by the mod

## Build

```powershell
python tools\build_aatrox_design_rework_assets.py
```

The published build produces runtime assets plus the CSV matrix only:

- asset matrix: `qa/aatrox_design_rework_asset_matrix.csv`

Temporary contact and preview sheets are treated as local diagnostics. They are not committed after the hero rebuild is complete.

## Design Checks

- Actor silhouette: compact dark-red demon warrior with readable horns, black armor, red chest mark, clear feet, and a shortened close-held sword; idle/run frames do not include flames, wings, smoke, or aura.
- Run: eight stable cross-step frames follow the Viktor reference principle: upright torso, tiny foot alternation, consistent body height, and bottom-anchor drift of no more than 1 px.
- Attack: body pose uses the refined greatsword swing, with a separate image-source red-black caster-follow slash.
- Q / `skill`: The Darkin Blade is represented as three delayed line cleaves; the third strike is heavier and knocks enemies airborne.
- W / `skill2`: Infernal Chains replaces the earlier made-up dash guard. It fires a hooked chain, slows the target, then snaps again for delayed damage and brief control.
- E / Umbral Dash: TFM2 has only three visible active skill slots, so E is folded into Aatrox's sustain identity: attacks and damaging skills heal Aatrox instead of showing a fake fourth active button.
- R / `ult`: World Ender grants attack damage, movement speed, and vamp; it briefly fears nearby enemies on cast. It no longer gives unrelated armor, magic resist, or attack-speed padding.
- R VFX: World Ender buff uses a separate image-source wing/arc aura; idle, run, hit, dead, and the encyclopedia body stay clean.
- Hit/dead/ult: these reuse the stable idle body so card, side-list, and battle HUD surfaces do not show an inflated monster pose.
- Icons: Q/W/R icons are rebuilt from the refined LoL ability image-gen source, green-key removed, dark framed, and exported at the existing 24x24 contract.

## Remaining Manual QA

- Enable the LOL mod in-game and confirm Aatrox in roster/card, side HUD, battle idle/run, Q hit, W chain, and R buff.
- In live battle, confirm run reads like a small upright cross-step and not a crawl or oversized lunge.
- In live battle, verify Q visual length matches `LineRangeProjectile` direction and does not read as an area circle.
- In live battle, verify W reads as Infernal Chains and not as a generic dash.
- Confirm R aura does not cover the health bar or make the compact portrait unreadable.
