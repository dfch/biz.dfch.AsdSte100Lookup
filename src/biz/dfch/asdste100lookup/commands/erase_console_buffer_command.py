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

"""EraseConsoleBufferCommand class."""

from abc import abstractmethod
from dataclasses import dataclass

from rich.console import Console

from biz.dfch.asdste100vocab import Word

from ..rule import Rule

from .command_base import CommandBase


@dataclass
class EraseConsoleBufferCommand(CommandBase):
    """Represents the command that erases the console export buffer."""

    @abstractmethod
    def invoke(
        self, console: Console, dictionary: list[Word], rules: list[Rule]
    ) -> None:
        """Erases the console export buffer."""

        super().invoke(console=console, dictionary=dictionary, rules=rules)

        _ = console.export_svg(clear=True)
