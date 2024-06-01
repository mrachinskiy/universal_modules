# SPDX-FileCopyrightText: 2019-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from bpy.types import Operator

from .. import var
from . import state, updatelib


class WM_OT_update_check(Operator):
    bl_label = "Check for Updates"
    bl_description = "Check for new add-on release"
    bl_idname = f"wm.{var.ADDON_ID}_update_check"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        if state.status in {state.CHECKING, state.INSTALLING, state.COMPLETED}:
            return {"CANCELLED"}
        updatelib.update_init_check(use_force_check=True)
        return {"FINISHED"}


class WM_OT_update_download(Operator):
    bl_label = "Install Update"
    bl_description = "Download and install new version of the add-on"
    bl_idname = f"wm.{var.ADDON_ID}_update_download"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        if state.status in {state.CHECKING, state.INSTALLING, state.COMPLETED}:
            return {"CANCELLED"}
        updatelib.update_init_download()
        return {"FINISHED"}


class WM_OT_update_whats_new(Operator):
    bl_label = "See What's New"
    bl_description = "Open release notes in web browser"
    bl_idname = f"wm.{var.ADDON_ID}_update_whats_new"
    bl_options = {"INTERNAL"}

    def execute(self, context):
        import webbrowser
        webbrowser.open(state.changelog_url)
        return {"FINISHED"}
