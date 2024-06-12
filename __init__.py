# SPDX-FileCopyrightText: 2021-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later


if "bpy" in locals():
    _essential.reload_recursive(var.ADDON_DIR, locals())
else:
    from . import _essential, var

    _essential.check(var.CONFIG_DIR, var.MANIFEST["blender_version_min"])

    import bpy
    from bpy.types import AddonPreferences, Panel

    from . import mod_update


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

    mod_update.init(repo_url="mrachinskiy/universal_modules")

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
