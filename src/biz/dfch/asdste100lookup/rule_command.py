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

"""RuleCommand class."""

from dataclasses import dataclass
import re

from .rule_renderer import RuleRenderer
from .command_base import CommandBase
from .rule import Rule


@dataclass
class RuleCommand(CommandBase):
    """Represents the rule command."""

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        selected_rules: list[Rule] = []
        for rule in rules:
            if re.search(self.value, rule.id_, re.IGNORECASE):
                selected_rules.append(rule)
                continue

        RuleRenderer().show(
            console=console,
            rules=selected_rules,  # pylint: disable=R0801
            is_summary_only=False)
