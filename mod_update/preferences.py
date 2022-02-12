# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2019-2022 Mikhail Rachinskiy

from bpy.props import BoolProperty, EnumProperty


class Preferences:
    mod_update_autocheck: BoolProperty(
        name="Automatically check for updates",
        description="Automatically check for updates with specified interval",
        default=True,
    )
    mod_update_prerelease: BoolProperty(
        name="Update to pre-release",
        description="Update add-on to pre-release version if available",
    )
    mod_update_interval: EnumProperty(
        name="Auto-check interval",
        description="Auto-check interval",
        items=(
            ("1", "Once a day", ""),
            ("7", "Once a week", ""),
            ("30", "Once a month", ""),
        ),
        default="7",
    )
