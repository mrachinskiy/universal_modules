# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2021-2022 Mikhail Rachinskiy

bl_info = {
    "name": "Universal Modules Example",
    "author": "Mikhail Rachinskiy",
    "version": (1, 0, 0),
    "blender": (2, 93, 0),
    "location": "Add-on enable warning/Add-on Prefereces/3D View > Sidebar",
    "description": "Universal modules usage example.",
    "doc_url": "https://github.com/mrachinskiy/universal_modules#readme",
    "tracker_url": "https://github.com/mrachinskiy/universal_modules/issues",
    "category": "Object",
}


if "bpy" in locals():
    _essential.reload_recursive(var.ADDON_DIR, locals())
else:
    import bpy
    from bpy.types import AddonPreferences, Panel

    from . import mod_update, _essential, var

    _essential.check(var.CONFIG_DIR, bl_info["blender"])


class Preferences(mod_update.Preferences, AddonPreferences):
    bl_idname = __package__

    def draw(self, context):
        mod_update.prefs_ui(self, self.layout)


class VIEW3D_PT_universal_modules_update(mod_update.Sidebar, Panel):
    bl_label = "Update"
    bl_category = "Universal Modules Example"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"


classes = (
    Preferences,
    VIEW3D_PT_universal_modules_update,
    *mod_update.ops,
)

TRANSLATION_DICTIONARY = {}


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # mod_update
    # ---------------------------

    mod_update.init(
        addon_version=bl_info["version"],
        repo_url="mrachinskiy/universal_modules",
    )

    mod_update.localization_extend(TRANSLATION_DICTIONARY)

    # Translation
    # ---------------------------

    bpy.app.translations.register(__name__, TRANSLATION_DICTIONARY)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    # Translation
    # ---------------------------

    bpy.app.translations.unregister(__name__)


if __name__ == "__main__":
    register()
