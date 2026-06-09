# Aatrox Design Rework Source

This folder contains the accepted image-gen source route for the design-book Aatrox rebuild.

Local-only inputs:

- `imagegen_actor_refined_front_sword_source.png`: accepted 4x3 final-scale actor source with a compact upright body, readable feet, and a close-held sword.
- `imagegen_vfx_lol_abilities_source.png`: accepted LoL ability source for Deathbringer slash, Q / The Darkin Blade, W / Infernal Chains, R / World Ender, and Q/W/R icons.

These source PNGs are not committed after the rebuild is complete. Keep them only as local scratch inputs when regenerating the runtime assets.

Build:

```powershell
python tools\build_aatrox_design_rework_assets.py
```

This route intentionally supersedes the earlier `aatrox_cartoon_model` proof, which is treated as a failed prior attempt.
Older actor/icon/VFX generations were removed from the active source route after review because they produced crawling silhouettes, muddy compact portraits, or code-drawn placeholder effects.
Temporary contact and preview sheets are local-only diagnostics. Set `AATROX_DEBUG_CONTACTS=1` while rebuilding if a quick visual sheet is needed, then delete it before publishing.
