# TeamFightManger2-LOL-Champions

Standalone Teamfight Manager 2 mod package based on the SilverBear League Champions workshop snapshot:

- Original Workshop item: `3735969373`
- Mod id: `bo_league_champions`
- Mod name: `BO-League Champions`
- Author: `silverbear`
- Version: `0.7.8`
- Last updated: `2026-06-09`
- Base dependency: `base >=0.4.9`

This repository uses its own mod id and asset namespace, so it can be copied into `mods/bo_league_champions` and enabled independently from the original Workshop subscription. Core files are `mod.mod_info`, `mod.override_info`, `champion/`, `aseprite_resources/`, `icons/`, `sound/`, `style/`, and `text/`.

Workshop description and changelog snapshots are kept in `WORKSHOP_DESCRIPTION_0.7.7.txt` and `WORKSHOP_CHANGE_NOTE_0.7.7.txt`.

## Aatrox Design Rework

This branch rebuilds Aatrox's visual assets from the design-book direction. Champion ids now use the `bo_league_champions_*` namespace for standalone registration, while legacy `test_mod_*` sound and VFX event names are preserved so battle logic and audio references remain stable. Asset paths use `asset/bo_league_champions/...`.

Rebuild the Aatrox visual assets with:

```powershell
python tools\build_aatrox_design_rework_assets.py
```

The build refreshes the Aatrox actor sheet, Q ground-crack impact, World Ender aura, E dash body read, and Q/E/R icons. Review notes are in `AATROX_DESIGN_REWORK_QA.md`.
