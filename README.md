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

Aatrox's accepted runtime assets are committed directly: refined idle display frames, stabilized run frames, approved attack frames, separate Q1/Q2/Q3 cleaves, separate Infernal Chains launch/snap sheets, World Ender aura, and localized text. Process/source PNGs are local-only and should not be committed after a rebuild. Review notes are in `AATROX_DESIGN_REWORK_QA.md`.

## Local Runtime Check

GitHub CI checks the repository visibility chain:

```powershell
python tools\ci_encyclopedia_visibility_check.py
```

Before judging the in-game encyclopedia on this machine, also run:

```powershell
python tools\local_runtime_encyclopedia_check.py
```

This local check verifies that `mods/bo_league_champions` matches the repository, only `bo_league_champions` is enabled, and a stale AppData `custom_database.tfm2db` is not enabled while missing `bo_league_champions_aatrox`.

Roster visibility coverage is tracked in `qa/roster_visibility_coverage.json`. Native Teamfight Manager 2 heroes must either be covered by a League replacement or remain in the staged retirement queue until a verified hide/disable path is proven.
