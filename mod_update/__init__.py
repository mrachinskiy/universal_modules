# SPDX-FileCopyrightText: 2019-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

# v1.2.1

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
