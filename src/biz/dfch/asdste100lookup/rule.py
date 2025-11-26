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

"""Rule class."""

from dataclasses import dataclass, field

from .rule_content_base import RuleContentBase


@dataclass
class Rule:
    """Represents a ASD-STE100 rule."""

    type_: str
    id_: str
    ref: str
    section: str
    category: str
    name: str
    summary: str
    contents: list[RuleContentBase] = field(default_factory=list)
