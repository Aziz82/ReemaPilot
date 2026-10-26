# ReemaPilot

Personal build of [FrogPilot](https://github.com/FrogAi/FrogPilot) (release of 4 Jul 2026), tuned for calm driving on Saudi roads in a Toyota/Lexus.

## What's different from FrogPilot

| Area | Setting | FrogPilot | ReemaPilot |
|---|---|---|---|
| Calm driving | Acceleration profile | Sport | Standard |
| | Deceleration profile (no car ahead) | Standard | Eco – coasts more |
| | Following distance – Aggressive / Standard / Relaxed | 1.25 / 1.45 / 1.75 s | 1.00 / 1.15 / 1.35 s (Aggressive = FrogPilot minimum) |
| | Driving-mode button on the driving screen | off | on – tap to switch Aggressive / Standard / Relaxed |
| Steering / cruise | Steering only (no cruise) | cruise main button on, no SET | same – kept on |
| | Cruise only (no steering) | – | long-press distance button to pause/resume steering |
| | Distance button short press | driving mode | driving mode (unchanged) |
| Saudi roads | Units | mph | km/h |
| | Speed-limit offset (all speeds) | +5 / +10 | 0 – drives at the posted limit |
| | Offline speed-limit maps | none | Saudi Arabia |
| | U.S. holiday themes | on | off |
| Look | Colours / steering-wheel icon / boot logo | Frog | ReemaPilot (teal + gold) |
| | Icons, sounds, turn signals | Frog | Stock openpilot |
| | Start-up message | Frog | "ReemaPilot is ready" |

All of these are normal FrogPilot settings and can still be changed on the device under Settings.

The preset is applied **once** on first boot (marker: `/data/reemapilot_preset_version`). Later changes made on the device are kept.

**Not changed:** steering/acceleration safety limits, driver monitoring, or the panda safety code.

**Known limit:** the word "FrogPilot" in the settings menu is part of the pre-compiled screen software and still shows.

## Files touched
- `frogpilot/common/reemapilot.py` – the preset, the theme installer and the one-time apply
- `frogpilot/common/frogpilot_variables.py` – uses the ReemaPilot defaults; `ReemaPilot` counts as a release branch
- `system/manager/manager.py` – applies the preset once at boot
- `frogpilot/assets/theme_manager.py` – installs the ReemaPilot theme
- `frogpilot/common/frogpilot_functions.py` – ReemaPilot boot logo
- `system/version.py` – `ReemaPilot` added to the release branches
- `frogpilot/assets/reemapilot_theme/`, `frogpilot/assets/other_images/reemapilot_boot_logo.png` – artwork
