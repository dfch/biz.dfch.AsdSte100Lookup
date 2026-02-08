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

"""CommandBase class."""

from abc import ABC, abstractmethod
from dataclasses import dataclass

from rich.console import Console

from biz.dfch.asdste100vocab import Word

from ..rule import Rule


@dataclass
class CommandBase(ABC):
    """Represents a base command with a single parameter."""

    value: str

    def __init__(self, value: str):
        self.value = value

    @abstractmethod
    def invoke(
        self, console: Console, dictionary: list[Word], rules: list[Rule]
    ) -> None:
        """Invokes the command."""

        assert isinstance(console, Console)
        assert isinstance(dictionary, list)
        for word in dictionary:
            assert isinstance(word, Word)
        assert isinstance(rules, list)
        for rule in rules:
            assert isinstance(rule, Rule)
