# Copyright (c) 2025 Ronald Rink, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

"""Constant class."""

from dataclasses import dataclass


@dataclass
class Constant:
    """System-wide constants."""

    # Note: also adjust in pyproject.toml.
    _VERSION = "1.9.0"
    PROG_NAME = "AsdSte100Lookup"

    BLOCKING_WHITE_SPACE = "\u200b"

    DICTIONARY_FILE = "dictionary.json"
    RULES_FILE = "rules.json"
