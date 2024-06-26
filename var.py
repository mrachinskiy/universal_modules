# SPDX-FileCopyrightText: 2021-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

import tomllib
from pathlib import Path


ADDON_ID = __package__
ADDON_DIR = Path(__file__).parent
CONFIG_DIR = ADDON_DIR / ".config"


with open(ADDON_DIR / "blender_manifest.toml", "rb") as f:
    MANIFEST = tomllib.load(f)
