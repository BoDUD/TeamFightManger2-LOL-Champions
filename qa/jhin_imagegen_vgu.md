# Jhin Imagegen VGU QA

Date: 2026-06-12

## Source Policy

Jhin was rebuilt from image-generated actor source and image-generated VFX source. The source/process PNGs are local-only and are not committed after rebuild, matching the repository policy for generated champion resources.

Local source hashes used for this rebuild:

- image-generated actor source: `96f39fbd5ea7852334bd6901d6eb9d4fb42643aaaa5df69608d03cda90db60b5`
- actor alpha intermediate: `291b03cee3a52d7c4c7d540eca8d1e991e6bb89fe7387fa6ba45a8ab27008730`
- image-generated VFX source: `c7a1a2b1f164a1b739600e28e214570548cbed58ada5735d1d721300442228c4`
- VFX alpha intermediate: `cc87f9af80432f0ce2302f35f0c1ab52d7734b321a6b72ab34b76a019ef1a5b6`

## Runtime Assets

- Actor: `aseprite_resources/champions/jhin#sheet.png` and `jhin#anim.fanim`
- Icons: `icons/jhin_skill.png`, `icons/jhin_skill2.png`, `icons/jhin_ult.png`
- Projectiles and effects: generated Whisper bullets, fourth-shot bloom, grenade, Deadly Flourish beam, trap bloom, Curtain Call stage, Curtain Call shots, hit bloom, finale bloom, and reload/fourth-shot loops.

## Review Notes

- The actor keeps the existing Jhin action contract: `idle 7`, `run 10`, `attack 15`, `skill 5`, `skill2 3`, `ult 3`, `hit 1`, `dead 1`, all in 64x64 cells.
- The first idle frame keeps the full mask, gun, legs, and feet inside compact display bounds so card/list/HUD portraits do not crop the lower body.
- W/E and R VFX use generated red-gold lotus and theater-stage art. The script only crops, scales, and packs generated source art into runtime sheets; it does not create geometry-line placeholder art.
- `champion/jhin.data_champion` removes the old base arrow projectile and wires generated projectile, buff, and view-effect assets for all active skills.
