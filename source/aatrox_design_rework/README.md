# Aatrox Design Rework Source

This folder contains the fresh image-gen source route for the design-book Aatrox rebuild.

Inputs:

- `imagegen_actor_design_source.png`: 5x2 pose sheet for idle, run, attack, Q cleave, E dash, ult, hit, and dead.
- `imagegen_vfx_design_source.png`: Q ground-crack cleave, E dash trail, and R aura source rows.
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
