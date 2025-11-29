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

"""CategoryCommand class."""

import re
from dataclasses import dataclass

from biz.dfch.logging import log  # pylint: disable=E0401

from .dictionary_command import DictionaryCommand
from .technical_word_category import TechnicalWordCategory
from .word import Word


@dataclass
class CategoryCommand(DictionaryCommand):
    """Represents the category command."""

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        matching_words: dict[int, Word] = {}
        try:
            for word in dictionary:
                if re.search(self.value, word.category, re.IGNORECASE):
                    matching_words[id(word)] = word
                    continue

        except re.error as ex:
            log.error("Invalid regex: '%s'", ex)

        words = list(matching_words.values())
        result = self.show(
            items=words, prompt=self.value)

        if 0 == len(result.rows):
            console.print("No match.")
            return

        categories = {word.category for word in words}
        cat_descriptions: list[str] = []
        for c in categories:
            cat_descriptions.append(
                f"{c}: {TechnicalWordCategory(c).get_description()}")
        cat_descriptions = sorted(cat_descriptions)
        info = '\n'.join(cat_descriptions)

        console.print(info)
        console.print(result)
        print(info)
