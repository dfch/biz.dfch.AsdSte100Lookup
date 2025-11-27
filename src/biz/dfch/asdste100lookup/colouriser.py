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

"""Colouriser class."""

import re


class Colouriser:
    """Creates a colourised string."""

    value: str

    def __init__(self, value: str, colour: str = "", is_bright: bool = False):

        assert value is not None and "" != value

        if colour is None or "" == colour:
            self.value = value
        else:
            if is_bright:
                colour = f"bright_{colour}"
            self.value = f"[{colour}]{value}[/{colour}]"

    def __str__(self) -> str:
        return self.value

    def __repl__(self) -> str:
        return self.__str__()

    def _colourise(self, pattern: str, value: str, is_bright: bool) -> str:

        colour = f"bright_{value}" if is_bright else value

        def replacer(match):
            word = match.group(0)
            return f"[{colour}]{word}[/{colour}]"

        # Pattern to match whole words containing the regex pattern.
        # We'll find all words (\b\w+\b) and check if pattern matches inside
        # them (case-insensitive).
        # This regex finds all words and then filters them by if pattern
        # exists inside.

        # To do this, we build a regex that matches words containing the
        # pattern:
        # (?i) - case-insensitive
        # \b\w*pattern\w*\b - words with the pattern inside

        # regex = re.compile(rf"(?i)\b\w*{pattern}\w*\b")
        # regex = re.compile(rf"(?i)\b\w*{pattern}\w*\b(?![.,;:])")
        regex = re.compile(rf"(?i)\b(\w*{pattern}\w*)\b")

        # Replace matching words with colored version
        return regex.sub(replacer, self.value)

    def to_black(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in black."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "black", is_bright)

    def to_red(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in red."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "red", is_bright)

    def to_green(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in green."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "green", is_bright)

    def to_darkergreen(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in green."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "dark_green", is_bright)

    def to_yellow(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in yellow."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "yellow", is_bright)

    def to_blue(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in blue."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "blue", is_bright)

    def to_magenta(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in mangenta."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "magenta", is_bright)

    def to_cyan(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in cyan."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "cyan", is_bright)

    def to_white(self, pattern: str, is_bright: bool = False) -> str:
        """Creates a colorized string in white."""

        assert pattern is not None and "" != pattern

        return self._colourise(pattern, "white", is_bright)
