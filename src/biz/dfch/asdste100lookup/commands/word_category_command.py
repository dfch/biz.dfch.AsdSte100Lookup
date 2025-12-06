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

"""WordCategoryCommand class."""

from dataclasses import dataclass
import re

from biz.dfch.logging import log  # pylint: disable=E0401

from ..word_category import WordCategory
from ..word import Word

from .command_query_type import CommandQueryType
from .dictionary_command import DictionaryCommand


@dataclass
class WordCategoryCommand(DictionaryCommand):
    """Represents the category command."""

    type_: CommandQueryType

    def __init__(self, type_: CommandQueryType, value: str) -> None:
        super().__init__(value)

        self.type_ = type_

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        if CommandQueryType.NAME == self.type_:
            keys = WordCategory.get_matching_keys(self.value)

        if CommandQueryType.ID == self.type_:
            regex = re.compile(self.value, re.IGNORECASE)

        matching_words: dict[int, Word] = {}
        try:
            for word in dictionary:
                if CommandQueryType.NAME == self.type_:
                    if word.category in keys:
                        matching_words[id(word)] = word
                    continue

                if CommandQueryType.ID == self.type_:
                    if regex.search(word.category):
                        matching_words[id(word)] = word
                    continue

        except re.error as ex:
            log.error("Invalid regex: '%s'", ex)

        words = list(matching_words.values())
        result = self.show(items=words, prompt=self.value)

        if 0 == len(result.rows):
            console.print("No match.")
            return

        categories = {word.category for word in words}
        cat_descriptions: list[str] = []
        for c in categories:
            cat_descriptions.append(f"{c}: {WordCategory(c).get_description()}")
        cat_descriptions = sorted(cat_descriptions)
        info = "\n".join(cat_descriptions)

        console.print(info)
        console.print(result)
        print(info)
