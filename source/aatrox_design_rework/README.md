# Aatrox Design Rework Source

This folder contains the image-gen source route for the design-book Aatrox rebuild.

Inputs:

- `imagegen_actor_design_source.png`: rejected 5x2 source retained as provenance; it produced an oversized crawling battle read.
- `imagegen_actor_stable_cross_step_source.png`: accepted 4x3 stable source with clean idle, Viktor-style cross-step walk/run poses, and separate attack/cleave/dash poses.
- `imagegen_vfx_design_source.png`: rejected as the active VFX source; current Q/R/E visual effects are intentionally simpler procedural frames for readability.
- `imagegen_icons_design_source.png`: three icon source panels for Q, E, and R.

Generated review sheets:

- `aatrox_design_actor_contact.png`
- `aatrox_design_icon_contact.png`
- `aatrox_design_vfx_contact.png`

Build:

```powershell
python tools\build_aatrox_design_rework_assets.py
```

This route intentionally supersedes the earlier `aatrox_cartoon_model` proof, which is treated as a failed prior attempt.
