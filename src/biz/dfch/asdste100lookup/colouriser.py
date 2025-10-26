# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Colorizer class."""

import re


class Colouriser:
    """Creates a colorized string."""

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
