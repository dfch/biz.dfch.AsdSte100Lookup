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

"""SaveCommand class."""

from dataclasses import dataclass
import tempfile
from pathlib import Path

from .command_base import CommandBase


@dataclass
class SaveCommand(CommandBase):
    """Represents the save command."""

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        file_name = Path(self.value).resolve()
        try:
            console.save_svg(str(file_name), title="ASD-STE100")
        except Exception as ex:  # pylint: disable=W0718
            console.print(f"File cannot be saved: '{file_name}'")
            console.print(f"[red]{ex}[/red]")

        text = (
            f"[link={file_name.as_uri()}]"
            "Console output saved: "
            f"'{file_name}'.[/link]"
        )
        console.print(text)
