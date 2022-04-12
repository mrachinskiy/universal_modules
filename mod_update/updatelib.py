# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2019-2022 Mikhail Rachinskiy

import threading
from typing import Union

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


def _parse_tag(tag: str) -> tuple[tuple[int, int, int], tuple[int, int, int]]:
    import re

    vers = tuple(
        tuple(int(x) for x in re.findall(r"\d+", y))
        for y in tag.split("-")
    )

    if len(vers) == 1:
        return vers[0], (0, 0, 0)

    return vers


def _save_state_serialize() -> None:
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


def _save_state_deserialize() -> dict[str, Union[bool, int]]:
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

    return data


def _update_check(use_force_check: bool) -> None:
    import re
    import urllib.request
    import urllib.error
    import json
    import ssl

    prefs = bpy.context.preferences.addons[var.ADDON_ID].preferences
    save_state = _save_state_deserialize()

    if not use_force_check and not prefs.mod_update_autocheck:
        return

    if save_state["update_available"]:
        use_force_check = True

    if not use_force_check and (
        state.days_passed is not None and
        state.days_passed < int(prefs.mod_update_interval)
    ):
        return

    _runtime_state_set(state.CHECKING)
    ssl_context = ssl.SSLContext()

    try:

        with urllib.request.urlopen(RELEASES_URL, context=ssl_context) as response:
            data = json.load(response)

            for release in data:

                if not prefs.mod_update_prerelease and release["prerelease"]:
                    continue

                if not release["draft"]:
                    update_version, required_blender = _parse_tag(release["tag_name"])

                    if update_version > ADDON_VERSION:
                        if required_blender <= bpy.app.version:
                            break
                        else:
                            continue
                    else:
                        _save_state_serialize()
                        _runtime_state_set(None)
                        return

            with urllib.request.urlopen(release["assets_url"], context=ssl_context) as response:
                data = json.load(response)

                for asset in data:
                    if re.match(r".+\d+.\d+.\d+.+", asset["name"]):
                        break

                prerelease_note = " (pre-release)" if release["prerelease"] else ""

                state.update_available = True
                state.update_version = ".".join(str(x) for x in update_version) + prerelease_note
                state.download_url = asset["browser_download_url"]
                state.changelog_url = release["html_url"]

        _save_state_serialize()
        _runtime_state_set(None)

    except (urllib.error.HTTPError, urllib.error.URLError) as e:

        state.error_msg = str(e)

        _save_state_serialize()
        _runtime_state_set(state.ERROR)


def _update_download() -> None:
    import io
    import zipfile
    import urllib.request
    import urllib.error
    import shutil
    import ssl
    from pathlib import Path

    _runtime_state_set(state.INSTALLING)
    ssl_context = ssl.SSLContext()

    try:

        with urllib.request.urlopen(state.download_url, context=ssl_context) as response:
            with zipfile.ZipFile(io.BytesIO(response.read())) as zfile:
                addons_dir = var.ADDON_DIR.parent
                extract_relpath = Path(zfile.namelist()[0])
                extract_dir = addons_dir / extract_relpath.parts[0]

                shutil.rmtree(var.ADDON_DIR)
                zfile.extractall(addons_dir)
                extract_dir.rename(var.ADDON_DIR)

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
