# Skill VFX Runtime Audit

Date: 2026-06-14

## Scope

This audit checks the active League champion data files for battle-visible skill feedback. It separates three cases that look similar in game:

- `missing visual node`: the skill slot has damage, movement, buff, or sound logic but no ViewEffect/projectile/buff visual node.
- `low-visibility visual`: a visual node exists, but it is low z, behind the actor/map, follows a unit that may be hidden, or fires at the wrong timing.
- `engine limitation`: the public data surface supports three active slots (`skill`, `skill2`, `ult`) and passive/attack hooks. A real fourth active League skill is not available without deeper code-mod UI/runtime work.

## Findings

- Kayn R was not a missing asset problem. `kayn_r_entry` and `kayn_r_exit` sheets are populated, and the action plays sound. The live failure was data-chain timing/anchoring: the entry row was following a unit during the hidden/stasis segment, while the exit burst was a top-level cast-start ViewEffect instead of being tied to the rush release. The fix makes entry target-ground/non-following and moves the exit ViewEffect into the direct `RushMoveToBack` hit branch.
- True active skill slots with no dedicated visual node in the current data are Fizz Q, Fizz E, Vayne Q, Vayne W/passive slot, Vayne R, and Ezreal E. Their cause is data design, not missing PNG files: they currently use rush, teleport, invisible, passive, or buff logic plus SFX without spawning a registered ViewEffect/projectile/buff visual.
- Ezreal Q and R do have projectile visuals through `LinearProjectile`; they were false positives in a first rough scan that did not count `LinearProjectile` as a visible projectile type.
- Low-visibility but not absent examples include Fizz R (`z=-1` fish/shark rows), Azir soldier and wall rows (`z=-1` by design), Jhin R channel/stage (`z=-1` / following), Yasuo R burst (caster-following), and several low-z basic/projectile accents. These are candidates for later readability passes, but they are not the same class as "no visual node".
- This is not a blanket original-game incompatibility. The engine accepts `Animation` / `LoopAnimation` rows in `view_effects`, animated projectiles in `view_projectiles`, and `Animated` rows in `view_buffs`. The known incompatible shape is putting `Animated` directly in `view_effects`; existing CI already blocks that. The practical risk is choosing the wrong anchor/timing/z for a valid visual row.

## Current Action Matrix

| Champion | Missing dedicated active-slot VFX | Main low-visibility risks |
| --- | --- | --- |
| Aatrox | None for Q/W/R slots | Q/W projectile and cast rows are low z/following, but present. |
| Azir | None | Soldier zones and wall visuals intentionally use low z floor placement. |
| Blitzcrank | None | No current sound-only active slot found. |
| Darius | None | Some bleed/might helper visuals are low z/following; R target chop is direct and visible. |
| Ezreal | E / Arcane Shift | Q and R have `LinearProjectile` visuals; E is `DirTeleport` plus SFX only. |
| Fiddlesticks | None | Crowstorm/drain have lower-z/following rows but registered visuals. |
| Fizz | Q / Urchin Strike, E / Playful-Trickster | R fish/shark rows exist but are `z=-1`. |
| Jhin | None | R channel/stage is low z/following; shot impacts are visible. |
| Jinx | None | Rocket explosion is target-following but present. |
| Kayn | None after this fix | R entry/exit are now target-ground/release-anchored. |
| Thresh | None | Q hit, W lantern, E sweep, and R box all have generated visuals. |
| Vayne | Q / Tumble, W/passive slot, R / Final Hour | Vayne has attack bolt and silver-bolt visuals, but active self-buff/dash slots are sound/buff only. |
| Veigar | None | Cage is low z but present. |
| Viktor | None | Evolution/shield helper buffs are behind actor by design; W/R ground visuals are direct. |
| Yasuo | None | R burst is caster-following and may need a later target-ground pass if live evidence shows it disappears. |

## Follow-Up Queue

- Add generated visible dash/arrival VFX for Ezreal E, Fizz Q/E, and Vayne Q/R before calling their active kits visually complete.
- Raise or retune Fizz R fish/shark z if live battle crops show the shark under terrain or units.
- Revisit Yasuo R only if live evidence shows the current caster-follow Last Breath burst disappears; it is present in data, unlike Kayn's old mistimed release burst.
