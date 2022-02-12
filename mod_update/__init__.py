# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2019-2022 Mikhail Rachinskiy

# v1.0.0

from . import operators, state
from .preferences import Preferences
from .ui import Sidebar, sidebar_ui, prefs_ui
from .updatelib import init


ops = (
    operators.WM_OT_update_check,
    operators.WM_OT_update_download,
    operators.WM_OT_update_whats_new,
)


def localization_extend(d: dict[str, dict[tuple[str, str], str]]) -> None:
    from . import localization
    localization.extend(d)
