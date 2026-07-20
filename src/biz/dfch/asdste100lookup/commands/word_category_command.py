# Copyright (c) 2025 - 2026 Ronald Rink, http://d-fens.ch
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

from biz.dfch.asdste100vocab import Word
from biz.dfch.asdste100vocab import WordCategory

from .command_query_type import CommandQueryType
from .dictionary_command import DictionaryCommand


@dataclass
class WordCategoryCommand(DictionaryCommand):
    """Represents the category command."""

    type_: CommandQueryType

    def __init__(
        self,
        type_: CommandQueryType,
        value: str,
    ) -> None:

        super().__init__(value)

        self.type_ = type_

    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        if CommandQueryType.LIST == self.type_:
            self._list_categories(console)
            return

        words = self._match_words(dictionary)
        self._print_results(console, words)

    def _list_categories(self, console) -> None:
        descriptions = WordCategory.get_descriptions()
        lines = [f"{key}\t{WordCategory.get_description(key)}" for key in descriptions]
        console.print("\n".join(lines))

    def _match_words(self, dictionary) -> list[Word]:
        keys = None
        regex = None

        if CommandQueryType.NAME == self.type_:
            keys = WordCategory.get_matching_keys(self.value)
        elif CommandQueryType.ID == self.type_:
            regex = re.compile(self.value, re.IGNORECASE)

        matching: dict[int, Word] = {}
        try:
            for word in dictionary:
                if keys is not None and word.category in keys:
                    matching[id(word)] = word
                elif regex is not None and regex.search(word.category):
                    matching[id(word)] = word
        except re.error as ex:
            log.error("Invalid regex: '%s'", ex)

        return list(matching.values())

    def _print_results(self, console, words: list[Word]) -> None:
        result = self.show(items=words, prompt=self.value)

        if 0 == len(result.rows):
            console.print("No match.")
            return

        categories = {word.category for word in words}
        cat_descriptions = sorted(
            f"{c}: {WordCategory(c).get_description()}" for c in categories
        )
        info = "\n".join(cat_descriptions)

        console.print(info)
        console.print(result)
        print(info)
