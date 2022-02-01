# ##### BEGIN GPL LICENSE BLOCK #####
#
#  mod_update automatic add-on updates.
#  Copyright (C) 2019-2022  Mikhail Rachinskiy
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####


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
