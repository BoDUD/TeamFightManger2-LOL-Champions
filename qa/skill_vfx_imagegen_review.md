# Skill VFX Imagegen Review

Date: 2026-06-11

## Scope

- Replaced Thresh `Flay` with image-generated chain-and-soul push frames.
- Replaced Darius `Noxian Guillotine` cast and hit VFX with image-generated execution chop frames.
- Replaced Kayn `Umbral Trespass` entry and exit VFX with image-generated shadow dive and burst frames.
- Restored the user-selected stronger Aatrox actor sheet with black armor, large horns, and oversized greatsword action frames, then updated the model contract to match that final sheet.
- Rebuilt Viktor's actor sheet and all active VFX families with fuller Hextech/Arcane visuals instead of mostly line-based placeholders.
- Verified Aatrox, Darius, Thresh, Kayn, and Viktor all have attack SFX, skill SFX, and champion/ultimate voice clips wired through `sound_info` with existing WAV clips.
- Removed obsolete source/process model resources from the active repository tree.

## Findings

- Thresh: the clean `origin/main` actor already uses the LoL-style green soul face, lantern, chain, and hook silhouette. The older black-hood screenshot came from an out-of-date dirty/runtime folder and should be corrected by syncing the merged mod folder. Flay's VFX was still too crescent-like, so it now uses a chain-backed horizontal shove wave that reads as E pushing enemies away.
- Darius: the previous ultimate cast read as a falling axe/icon. The new cast is a close-range Darius execution chop, and the hit sheet is a ground-impact shockwave instead of a vertical marker.
- Kayn: Q/W slash sheets are acceptable and read as scythe arcs. R entry/exit had the most symbol-like feel, so only those sheets were replaced with shadow-body entry and red-purple exit burst frames.
- Aatrox: the current mainline actor sheet was too uniformly red and muddy. This pass restores the requested earlier Darkin model with readable horns, black armor, giant sword, and larger attack/skill poses. The basic attack remains model-driven and does not trigger the oversized skill slash VFX, while Q/W/R keep their existing Darkin Blade, dash, and World Ender VFX/SFX wiring.
- Viktor: the previous mainline/dirty VFX were too line-based. This pass replaces the tiny attack projectile and rebuilds laser, laser aftershock, shield, Gravity Field, Chaos Storm, storm impact, and evolution aura sheets with fuller image-generated Hextech machinery and energy. The rebuilt actor was enlarged inside its `57x54` frame cells and given small attack/skill/run silhouette accents so actions read as active model animation instead of static idle frames.
- Audio: `sound/sfx` contains matching `.sound_info` and `.wav` clips for Aatrox, Darius, Thresh, Kayn, and Viktor attack casts/hits, skill casts/hits, and ult/skill voice lines. Champion data references were checked for the relevant attack, skill, skill2, and ult actions.
- Cleanup: `source/aatrox_design_rework/README.md`, local image-generation source PNGs, alpha intermediates, and contact-sheet review PNGs were removed so the active mod tree only carries runtime assets and lightweight QA metadata.

## Validation

- Preserved runtime frame counts and durations for the edited effect sheets; frame boxes were only changed where the replacement actor/effect sheet required matching cells.
- Aatrox intentionally restores the matching actor sheet and animation table together, because the requested model uses wider action cells than the compact mainline sheet.
- Generated contact sheets were used locally for review and then deleted from the active tree before commit.
- Ran `python tools/ci_encyclopedia_visibility_check.py` after the model/VFX/audio checks; it passed.
