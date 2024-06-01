# SPDX-FileCopyrightText: 2019-2024 Mikhail Rachinskiy
# SPDX-License-Identifier: GPL-3.0-or-later

from collections.abc import Iterator
from pathlib import Path


def _po_parse(text: str) -> dict[tuple[str, str], str]:
    import re
    concat_multiline = text.replace('"\n"', "")
    entries = re.findall(r'(?:msgctxt\s*"(.+)")?\s*msgid\s*"(.+)"\s*msgstr\s*"(.*)"', concat_multiline)

    return {
        (ctxt or "*", key.replace("\\n", "\n")): msg.replace("\\n", "\n")
        for ctxt, key, msg in entries
        if msg
    }


def _walk() -> Iterator[tuple[str, dict[tuple[str, str], str]]]:
    for child in Path(__file__).parent.iterdir():
        if child.is_file() and child.suffix == ".po":
            with open(child, "r", encoding="utf-8") as file:
                yield child.stem, _po_parse(file.read())


def extend(d: dict[str, dict[tuple[str, str], str]]) -> None:
    for k, v in _walk():
        if k in d:
            d[k] |= v
