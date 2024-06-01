# SPDX-FileCopyrightText: 2019-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

import threading

import bpy

from .. import var
from . import state


ADDON_VERSION: tuple[int, int, int] = None
RELEASES_URL: str = None
SAVE_STATE_FILEPATH = var.CONFIG_DIR / "update_state.json"


def _runtime_state_set(status: int) -> None:
    state.status = status

    for window in bpy.context.window_manager.windows:
        for area in window.screen.areas:
            area.tag_redraw()


def _save_state_serialize(runtime_state: int = None) -> None:
    import datetime
    import json

    state.days_passed = 0
    data = {
        "update_available": state.update_available,
        "last_check": int(datetime.datetime.now().timestamp()),
    }

    if not var.CONFIG_DIR.exists():
        var.CONFIG_DIR.mkdir(parents=True)

    with open(SAVE_STATE_FILEPATH, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

    _runtime_state_set(runtime_state)


def _save_state_deserialize() -> None:
    import datetime
    import json

    data = {
        "update_available": False,
        "last_check": 0,
    }

    if SAVE_STATE_FILEPATH.exists():
        with open(SAVE_STATE_FILEPATH, "r", encoding="utf-8") as file:
            data.update(json.load(file))
            last_check = datetime.date.fromtimestamp(data["last_check"])
            delta = datetime.date.today() - last_check
            state.days_passed = delta.days
            state.update_available = data["update_available"]


def _parse_tag(tag: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    import re

    vers = tuple(
        tuple(int(x) for x in re.findall(r"\d+", y))
        for y in tag.split("-")
    )

    if len(vers) == 1:
        return vers[0], (0, 0, 0)

    return vers


def _is_autocheck() -> bool:
    prefs = bpy.context.preferences.addons[var.ADDON_ID].preferences

    if not prefs.mod_update_autocheck:
        return False

    if state.days_passed is None:
        return True

    return state.update_available or (state.days_passed >= int(prefs.mod_update_interval))


def _update_check(use_force_check: bool) -> None:
    _save_state_deserialize()

    if not use_force_check and not _is_autocheck():
        state.update_available = False
        return

    import json
    import re
    import ssl
    import urllib.error
    import urllib.request

    _runtime_state_set(state.CHECKING)
    ssl_context = ssl.SSLContext()

    try:

        with urllib.request.urlopen(RELEASES_URL, context=ssl_context) as response:
            prefs = bpy.context.preferences.addons[var.ADDON_ID].preferences

            for release in json.load(response):
                if (not prefs.mod_update_prerelease and release["prerelease"]) or release["draft"]:
                    continue

                update_ver, blender_ver = _parse_tag(release["tag_name"])

                if update_ver > ADDON_VERSION and blender_ver <= bpy.app.version:
                    break
            else:
                state.update_available = False
                _save_state_serialize()
                return

        with urllib.request.urlopen(release["assets_url"], context=ssl_context) as response:
            for asset in json.load(response):
                if re.match(r".+\d+.\d+.\d+.+", asset["name"]):
                    break
            else:
                state.error_msg = "Unable to find installation file"
                _save_state_serialize(state.ERROR)
                return

            state.update_available = True
            state.update_version = ".".join(str(x) for x in update_ver)
            state.download_url = asset["browser_download_url"]
            state.changelog_url = release["html_url"]
            if release["prerelease"]:
                state.update_version += " (pre-release)"

        _save_state_serialize()

    except (urllib.error.HTTPError, urllib.error.URLError) as e:

        state.error_msg = str(e)
        _save_state_serialize(state.ERROR)


def _update_download() -> None:
    import io
    import shutil
    import ssl
    import urllib.error
    import urllib.request
    import zipfile
    from pathlib import Path

    _runtime_state_set(state.INSTALLING)
    ssl_context = ssl.SSLContext()

    try:

        with urllib.request.urlopen(state.download_url, context=ssl_context) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as zfile:
                addons_dir = var.ADDON_DIR.parent
                extract_dir = addons_dir / f"{var.ADDON_DIR.name} update {state.update_version.replace('.', '')}"
                update_dir = extract_dir / Path(zfile.namelist()[0]).parts[0]

                shutil.rmtree(var.ADDON_DIR)
                zfile.extractall(extract_dir)
                update_dir.rename(var.ADDON_DIR)
                extract_dir.rmdir()

        _runtime_state_set(state.COMPLETED)

    except (urllib.error.HTTPError, urllib.error.URLError) as e:

        state.error_msg = str(e)
        _runtime_state_set(state.ERROR)


def update_init_check(use_force_check: bool = False) -> None:
    threading.Thread(target=_update_check, args=(use_force_check,)).start()


def update_init_download() -> None:
    threading.Thread(target=_update_download).start()


def init(addon_version: tuple[int, int, int], repo_url: str) -> None:
    global ADDON_VERSION
    global RELEASES_URL

    ADDON_VERSION = addon_version
    RELEASES_URL = f"https://api.github.com/repos/{repo_url}/releases?per_page=10"

    update_init_check()
