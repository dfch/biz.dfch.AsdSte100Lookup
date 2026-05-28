# Copyright (C) 2026 Ronald Rink, d-fens GmbH, http://d-fens.ch
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: AGPL-3.0-or-later

"""BuiltInRules enumeration."""

from enum import Enum
from importlib import resources
from pathlib import Path


class BuiltInRules(Enum):
    """ASD STE100 builtin rules."""

    DATA_DIR = "data"
    STE100_RULES = Path(
        str(
            resources.files(__package__).joinpath(
                "data", "asdste100_issue9_rules.jsonl"
            )
        )
    )
