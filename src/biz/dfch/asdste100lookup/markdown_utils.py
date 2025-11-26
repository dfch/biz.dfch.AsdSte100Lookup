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

"""MarkDownUtils class."""

from io import StringIO
from typing import cast

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel


class MarkDownUtils:
    """Support class for working with `MarkDown()`."""

    @staticmethod
    def get_max_width(value: str) -> int:
        """
        Returns the maximum width of a specified markdown text.

        Args:
            value (str): The markdown text.

        Returns:
            (str): The maximum character width of a text rendered
                with `MarkDown()`.
         """

        if not value or "" == value:
            return 0

        md = Markdown(value)
        console = Console(file=StringIO())
        console.print(md)
        io: StringIO = cast(StringIO, console.file)
        rendered = io.getvalue()  # pylint: disable=E1101
        lines = rendered.splitlines()

        result = max((len(line.rstrip()) for line in lines), default=0)

        return result

    @staticmethod
    def to_panel(
        value: str = "",
        title: str = "",
        style: str = "green"
    ) -> Panel:
        """Converts a markdown to text to a `Panel`."""

        if value is None:
            value = ""

        assert style is not None and "" != style

        md = Markdown(value)

        max_length = MarkDownUtils.get_max_width(value)

        padding_height = 0
        padding_width = 1
        border_width = 1
        width = max_length + 2 * padding_width + 2 * border_width + 2

        result = Panel(
            md,
            title=title,
            width=width,
            title_align="left",
            border_style=style,
            expand=False,
            padding=(padding_height, padding_width),
        )

        return result
