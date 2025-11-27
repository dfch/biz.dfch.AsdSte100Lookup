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

"""UnknownCommand class."""

import re
from dataclasses import dataclass
from typing import cast

from biz.dfch.logging import log  # pylint: disable=E0401

from .dictionary_command import DictionaryCommand
from .word import Word


@dataclass
class UnknownCommand(DictionaryCommand):
    """Represents an unknown command."""

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        matching_words: dict[int, Word] = {}
        try:
            for word in dictionary:
                if re.search(self.value, word.name, re.IGNORECASE):
                    matching_words[id(word)] = word
                    continue

                for spelling in word.spellings:
                    if re.search(self.value, spelling, re.IGNORECASE):
                        matching_words[id(word)] = word
                        continue

                if self._get_first_or_item(word.ste_example) and re.search(
                    self.value,
                    cast(str, self._get_first_or_item(word.ste_example)),
                    re.IGNORECASE,
                ):
                    matching_words[id(word)] = word
                    continue

                if self._get_first_or_item(word.nonste_example) and re.search(
                    self.value,
                    cast(str, self._get_first_or_item(word.nonste_example)),
                    re.IGNORECASE,
                ):
                    matching_words[id(word)] = word
                    continue

        except re.error as ex:
            log.error("Invalid regex: '%s'", ex)

        result = self.show(
            items=list(matching_words.values()), prompt=self.value)

        # Clear recording buffer before next output.
        _ = console.export_svg(clear=True)

        if 0 == len(result.rows):
            console.print("No match.")
        else:
            console.print(result)
