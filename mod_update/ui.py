# SPDX-FileCopyrightText: 2019-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

import bpy
from bpy.app.translations import pgettext_iface as _

from . import operators, state


class Sidebar:
    """Only shows when new update is available"""

    @classmethod
    def poll(cls, context):
        return state.update_available

    def draw_header(self, context):
        self.layout.label(icon="INFO")

    def draw(self, context):
        sidebar_ui(self.layout)


def sidebar_ui(layout):
    row = layout.row(align=True)
    row.alignment = "CENTER"

    if state.status is state.COMPLETED:
        row.label(text="Update completed")
        row.operator(operators.WM_OT_update_whats_new.bl_idname)

        row = layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Close Blender to complete the installation", icon="ERROR")

    elif state.status is state.INSTALLING:
        row.label(text="Installing...")

    elif state.status is state.ERROR:
        row.label(text=state.error_msg)

    else:
        row.label(text=_("Update {} is available").format(state.update_version))

    col = layout.row()
    col.alignment = "CENTER"
    col.scale_y = 1.5
    col.enabled = state.status is None or state.status is state.ERROR
    col.operator(operators.WM_OT_update_download.bl_idname)


def prefs_ui(self, layout: bpy.types.UILayout):
    use_online_access = bpy.context.preferences.system.use_online_access

    col = layout.column()

    if not use_online_access:
        row = col.row()
        row.alert = True
        row.alignment = "CENTER"
        row.label(text="Allow online access for auto update check")

    col = col.column()
    col.active = use_online_access
    col.prop(self, "mod_update_autocheck")
    col.prop(self, "mod_update_prerelease")
    sub = col.column()
    sub.active = self.mod_update_autocheck
    sub.prop(self, "mod_update_interval")

    layout.separator()

    row = layout.row(align=True)
    row.alignment = "CENTER"

    if state.status is state.COMPLETED:
        row.label(text="Update completed")
        row.operator(operators.WM_OT_update_whats_new.bl_idname)

        row = layout.row(align=True)
        row.alignment = "CENTER"
        row.label(text="Close Blender to complete the installation", icon="ERROR")

    elif state.status is state.CHECKING:
        row.label(text="Checking...")

    elif state.status is state.INSTALLING:
        row.label(text="Installing...")

    elif state.status is state.ERROR:
        row.label(text=state.error_msg)

    elif state.update_available:
        row.label(text=_("Update {} is available").format(state.update_version))

    else:
        if state.days_passed is None:
            msg_date = _("never")
        elif state.days_passed == 0:
            msg_date = _("today")
        elif state.days_passed == 1:
            msg_date = _("yesterday")
        else:
            msg_date = "{} {}".format(state.days_passed, _("days ago"))

        row.label(text="{} {}".format(_("Last checked"), msg_date))

    col = layout.row()
    col.alignment = "CENTER"
    col.scale_y = 1.5
    col.enabled = state.status is None or state.status is state.ERROR

    if state.update_available:
        col.operator(operators.WM_OT_update_download.bl_idname)
    else:
        col.operator(operators.WM_OT_update_check.bl_idname)
