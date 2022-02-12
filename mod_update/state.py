# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright 2019-2022 Mikhail Rachinskiy

CHECKING = 0
INSTALLING = 1
COMPLETED = 2
ERROR = 3

status: int = None
days_passed: int = None
update_version: str = None
download_url: str = None
changelog_url: str = None
error_msg: str = None

update_available: bool = False
