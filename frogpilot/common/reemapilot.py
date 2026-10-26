#!/usr/bin/env python3
"""ReemaPilot: personal preset layered on top of FrogPilot.

Three things live here:
  1. REEMAPILOT_DEFAULTS - the settings ReemaPilot ships with (calm driving,
     Saudi roads, ReemaPilot look). frogpilot_variables.py uses these as the
     defaults, so a fresh install starts with them.
  2. apply_reemapilot_preset() - writes those settings ONCE on a device that
     already has FrogPilot settings, so an existing install picks them up.
     After that the driver can change anything in Settings and it sticks.
  3. install_reemapilot_theme() - copies the ReemaPilot colours and steering
     wheel into the folders FrogPilot's theme manager reads from.

Nothing here touches steering/acceleration safety limits (panda safety,
car controller limits); only user-facing FrogPilot options are set.
"""
import json
import shutil

from pathlib import Path

# Bump this when the preset changes and should be re-applied once on devices.
PRESET_VERSION = 1
PRESET_MARKER = Path("/data/reemapilot_preset_version")

THEME_NAME = "reema"
THEME_SOURCE_PATH = Path(__file__).parents[1] / "assets/reemapilot_theme"

SAUDI_MAPS = json.dumps({"nations": ["SA"], "states": []})

REEMAPILOT_DEFAULTS: dict[str, str] = {
  # --- Smoother, calmer driving -------------------------------------------
  "AccelerationProfile": "0",        # Standard (FrogPilot ships "Sport")
  "DecelerationProfile": "1",        # Eco: coast more when slowing for set speed/curves (full braking still available behind a lead)
  # Following gaps kept tight for Saudi traffic (big gaps invite cut-ins). FrogPilot allows 1.0-3.0 s.
  "AggressiveFollow": "1.00",        # seconds behind lead in "Aggressive" - FrogPilot's minimum (FrogPilot default: 1.25)
  "StandardFollow": "1.15",          # seconds behind lead in "Standard" (FrogPilot: 1.45)
  "RelaxedFollow": "1.35",           # seconds behind lead in "Relaxed" (FrogPilot: 1.75)
  "IncreasedStoppedDistance": "0",   # no extra gap when stopped in traffic
  "OnroadDistanceButton": "1",       # on-screen button to switch Aggressive / Standard / Relaxed while driving

  # --- Steering and cruise as separate functions ---------------------------
  #   Steering only : cruise ON/OFF (main) button on, don't press SET  -> "Always On Lateral"
  #   Both          : main on + SET
  #   Cruise only   : while engaged, long-press the distance button    -> steering paused (long-press again to resume)
  "AlwaysOnLateral": "1",            # steering works without cruise set (needs a reboot to take effect)
  "AlwaysOnLateralMain": "1",        # ...switched on by the cruise main button
  "PauseAOLOnBrake": "0",            # keep steering while braking in steering-only mode
  "LongDistanceButtonControl": "3",  # distance button long press = pause/resume steering (was: Experimental Mode)
  "DistanceButtonControl": "1",      # distance button short press = cycle driving mode (Aggressive/Standard/Relaxed)

  # --- Saudi roads & speed limits -----------------------------------------
  "IsMetric": "1",                   # km/h everywhere
  "Fahrenheit": "0",
  "Offset1": "0",                    # 0-29 km/h   -> drive at the posted limit
  "Offset2": "0",                    # 30-49 km/h
  "Offset3": "0",                    # 50-59 km/h
  "Offset4": "0",                    # 60-79 km/h
  "Offset5": "0",                    # 80-99 km/h
  "Offset6": "0",                    # 100-119 km/h
  "Offset7": "0",                    # 120-140 km/h
  "SpeedLimitController": "1",
  "SLCFallback": "2",                # keep the previous limit when none is found
  "MapsSelected": SAUDI_MAPS,        # offline speed-limit maps: Saudi Arabia
  "HolidayThemes": "0",              # FrogPilot's themes follow U.S. holidays

  # --- ReemaPilot look & name ---------------------------------------------
  "CustomColors": THEME_NAME,
  "CustomDistanceIcons": "stock",
  "CustomIcons": "stock",
  "CustomSignals": "stock",
  "CustomSounds": "stock",
  "WheelIcon": THEME_NAME,
  "RandomThemes": "0",
  "StartupMessageTop": "ReemaPilot is ready",
  "StartupMessageBottom": "Hands on the wheel, eyes on the road",
}


def install_reemapilot_theme(theme_save_path: Path) -> None:
  """Copy ReemaPilot colours + steering wheel where the theme manager looks."""
  colors_source = THEME_SOURCE_PATH / "colors"
  colors_destination = theme_save_path / "theme_packs" / THEME_NAME / "colors"
  colors_destination.mkdir(parents=True, exist_ok=True)
  shutil.copytree(colors_source, colors_destination, dirs_exist_ok=True)

  wheel_source = THEME_SOURCE_PATH / "steering_wheel" / f"{THEME_NAME}.png"
  wheel_destination = theme_save_path / "steering_wheels" / f"{THEME_NAME}.png"
  wheel_destination.parent.mkdir(parents=True, exist_ok=True)
  shutil.copy2(wheel_source, wheel_destination)


def apply_reemapilot_preset(params, params_cache=None, marker: Path = PRESET_MARKER) -> bool:
  """Write REEMAPILOT_DEFAULTS once per PRESET_VERSION. Returns True if applied."""
  try:
    applied_version = int(marker.read_text().strip())
  except (FileNotFoundError, ValueError):
    applied_version = 0

  if applied_version >= PRESET_VERSION:
    return False

  for key, value in REEMAPILOT_DEFAULTS.items():
    params.put(key, value)
    if params_cache is not None:
      params_cache.put(key, value)

  marker.parent.mkdir(parents=True, exist_ok=True)
  marker.write_text(str(PRESET_VERSION))
  print(f"ReemaPilot preset v{PRESET_VERSION} applied")
  return True
