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

from ..rule import Rule
from ..rule_renderer import RuleRenderer
from ..rule_renderer import RuleRenderType

from .command_query_type import CommandQueryType
from .erase_console_buffer_command import EraseConsoleBufferCommand


@dataclass
class RuleCommand(EraseConsoleBufferCommand):
    """Represents the rule command."""

    _type_: CommandQueryType
    _show_heading_only: bool
    _display_type: RuleRenderType

    def __init__(
        self,
        type_: CommandQueryType,
        value: str,
        display_type: RuleRenderType = RuleRenderType.DEFAULT,
    ) -> None:

        super().__init__(value)

        self._type_ = type_
        self._display_type = display_type

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        regex = re.compile(self.value, re.IGNORECASE)

        selected_rules: list[Rule] = []
        for rule in rules:
            match self._type_:
                # With `ALL` we select all rules regardless of `value`.
                case CommandQueryType.ALL:
                    selected_rules.append(rule)
                    continue

                case CommandQueryType.ID:
                    value = rule.id_
                case CommandQueryType.NAME:
                    value = rule.name
                case CommandQueryType.SECTION:
                    value = rule.section
                case CommandQueryType.CATEGORY:
                    value = rule.category
                case CommandQueryType.SUMMARY:
                    value = rule.summary
                case CommandQueryType.TEXT:
                    value = ' '.join([item.data for item in rule.contents])
                case _:
                    raise ValueError(
                        f"Invalid {CommandQueryType.__name__}: "
                        f"'{self._type_}'."
                    )
            if regex.search(value):
                selected_rules.append(rule)

        RuleRenderer().show(
            console=console,
            rules=selected_rules,
            type_=self._display_type,
        )
