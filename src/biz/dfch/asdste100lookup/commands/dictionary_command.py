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

"""DictionaryCommand class."""

from dataclasses import dataclass
from itertools import zip_longest
from typing import cast

from rich.table import Table

from biz.dfch.logging import log  # pylint: disable=E0401

from ..colouriser import Colouriser
from ..constant import Constant
from ..table_row import TableRow
from ..utils import get_value_or_default
from ..word import Word
from ..word_category import WordCategory
from ..word_note import WordNote
from ..word_status import WordStatus

from .erase_console_buffer_command import EraseConsoleBufferCommand


@dataclass
class DictionaryCommand(EraseConsoleBufferCommand):
    """Shows dictionary words on the console."""

    def to_colour(self, text: str, value: str, status: str) -> str:
        """Colourises value in specified text green or red based on status."""

        assert isinstance(status, str) and "" != status

        if WordStatus.APPROVED == status:
            return Colouriser(text).to_green(value)

        return Colouriser(text).to_red(value)

    def to_word_colour(
        self, text: str, value: str, status: str, category: str
    ) -> str:
        """Colourises value in specified text green or red based on status."""

        assert isinstance(status, str) and "" != status
        assert isinstance(category, str) and "" != category

        if status in (WordStatus.REJECTED, WordStatus.UNKNOWN):
            return Colouriser(text).to_red(value)

        if WordCategory.DEFAULT == category:
            return Colouriser(text).to_green(value)

        return Colouriser(text).to_darkergreen(value)

    def _get_first_or_item(self, item: str | list[str] | None) -> str | None:
        """
        Retrieves the first `item` of a list or the `item` itself.
        If `item` is `None` or the list is empty, `None` is returned.

        Args:
            item (str | list[str] | None): A list of strings or a string.

        Returns:
            (str | None): - The first `item` in the list, if it is a list
                - The `item`, if it is not a list
                - None, if `item` or the list is empty.
        """

        if item is None:
            return None

        if isinstance(item, list):
            return item[0] if item else None

        return item

    def _process_note_value(
        self,
        word: Word,
        note: WordNote,
    ) -> list[TableRow]:

        assert isinstance(word, Word)
        assert isinstance(note, WordNote)

        result: list[TableRow] = []

        row = TableRow()
        row.description = str(Colouriser(note.value, "yellow"))
        if note.ste_example:
            row.ste_example = self.to_colour(
                note.ste_example, word.name, WordStatus.APPROVED
            )
        if note.nonste_example:
            row.nonste_example = self.to_colour(
                note.nonste_example, word.name, WordStatus.REJECTED
            )
        result.append(row)

        return result

    def _process_note_words(
        self, note: WordNote, row: TableRow
    ) -> list[TableRow]:

        assert isinstance(note, WordNote)
        assert isinstance(row, TableRow)

        result: list[TableRow] = []

        nwords = note.words

        if row.description or row.ste_example or row.nonste_example:

            row = TableRow()
            result.append(row)

        row.description = str(Colouriser(note.value, "yellow"))

        for nword in nwords:
            result.extend(self._process_nword(nword))

        return result

    def _process_nword(self, word: Word) -> list[TableRow]:

        assert isinstance(word, Word)

        result: list[TableRow] = []

        row = TableRow()
        result.append(row)
        row.description = self.to_colour(
            f"{word.name} ({word.type_})",
            word.name,
            word.status,
        )
        if self._get_first_or_item(word.ste_example):
            row.ste_example = self.to_colour(
                cast(str, self._get_first_or_item(word.ste_example)),
                word.name,
                WordStatus.APPROVED,
            )
        if self._get_first_or_item(word.nonste_example):
            row.nonste_example = self.to_colour(
                cast(
                    str,
                    self._get_first_or_item(word.nonste_example),
                ),
                word.name,
                WordStatus.REJECTED,
            )

        return result

    def _process_note(self, word: Word, row: TableRow) -> list[TableRow]:

        assert isinstance(word, Word)
        assert isinstance(row, TableRow)
        assert isinstance(word.note, WordNote)
        assert word.note

        result: list[TableRow] = []

        note = word.note

        if note.words:
            result.extend(self._process_note_words(word.note, row))

        elif note.value:
            result.extend(self._process_note_value(word, note))

        return result

    def _process_alternatives(
        self, word: Word, row: TableRow
    ) -> list[TableRow]:

        assert isinstance(word, Word)
        assert isinstance(row, TableRow)
        assert word.alternatives

        result: list[TableRow] = []

        alternatives = word.alternatives
        for alt in alternatives:
            if row.description:
                row = TableRow()
                result.append(row)

            row.description = self.to_colour(
                f"{alt.name.upper()} ({alt.type_})", alt.name, alt.status
            )

            # Process examples pairwise.
            if isinstance(alt.ste_example, list):
                ste_list = alt.ste_example
            elif alt.ste_example is None:
                ste_list = []
            else:
                ste_list = [alt.ste_example]

            if isinstance(alt.nonste_example, list):
                nonste_list = alt.nonste_example
            elif alt.nonste_example is None:
                nonste_list = []
            else:
                nonste_list = [alt.nonste_example]

            for i, (ste, nonste) in enumerate(
                zip_longest(ste_list, nonste_list, fillvalue=" ")
            ):

                if 0 == i:
                    row.ste_example = self.to_colour(ste, alt.name, alt.status)
                    row.nonste_example = self.to_colour(
                        nonste, word.name, WordStatus.REJECTED
                    )
                    continue

                row = TableRow()
                result.append(row)

                row.ste_example = self.to_colour(ste, alt.name, alt.status)
                row.nonste_example = self.to_colour(
                    nonste, word.name, WordStatus.REJECTED
                )

        return result

    def show(self, items: list[Word], prompt: str) -> Table:
        """Creates a table of the specified words."""

        assert isinstance(items, list)
        assert isinstance(prompt, str)

        # Create the table
        result = Table()
        result.add_column("Word", no_wrap=True, min_width=16)
        result.add_column("Meaning/ALTERNATIVE", min_width=16)
        result.add_column("STE Example")
        result.add_column("Non-STE Example")

        rows: list[TableRow] = []
        for word in items:

            row = TableRow()
            rows.append(row)

            if WordStatus.APPROVED == word.status:
                if word.name:
                    row.word = self.to_word_colour(
                        f"{word.name.upper()} ({word.type_})",
                        word.name,
                        word.status,
                        word.category,
                    )
                if self._get_first_or_item(word.ste_example):
                    row.ste_example = self.to_colour(
                        cast(str, self._get_first_or_item(word.ste_example)),
                        prompt,
                        word.status,
                    )
            elif WordStatus.REJECTED == word.status:
                if word.name:
                    row.word = self.to_word_colour(
                        f"{word.name.lower()} ({word.type_})",
                        word.name,
                        word.status,
                        word.category,
                    )
                if self._get_first_or_item(word.nonste_example):
                    row.nonste_example = self.to_colour(
                        cast(str, self._get_first_or_item(word.nonste_example)),
                        prompt,
                        word.status,
                    )
            else:
                log.error(
                    "Word '%s' with status '%s' found.", word.name, word.status
                )
                continue

            if word.spellings:
                colourised_spellings: list[str] = [
                    str(Colouriser(x, "blue")) for x in word.spellings
                ]

                spellings = "\n".join(colourised_spellings)
                row.word = f"{row.word}\n{spellings}"

            if word.meanings:
                meanings = word.meanings
                for meaning in meanings:
                    if row.ste_example or row.nonste_example:
                        row = TableRow()
                        rows.append(row)
                    row.description = meaning.value
                    if meaning.ste_example:
                        row.ste_example = self.to_colour(
                            meaning.ste_example, word.name, word.status
                        )
                    if meaning.nonste_example:
                        row.nonste_example = self.to_colour(
                            meaning.nonste_example,
                            word.name,
                            WordStatus.REJECTED,
                        )

            if word.alternatives:
                rows.extend(self._process_alternatives(word, row))

            if word.note:
                rows.extend(self._process_note(word, row))

            rows.append(TableRow())

        for row in rows:
            if row.description:
                row.description = row.description.replace(
                    Constant.BLOCKING_WHITE_SPACE, ""
                )
            log.debug(
                "'%s', '%s', '%s', '%s'",
                row.word,
                row.description,
                row.ste_example,
                row.nonste_example,
            )
            result.add_row(
                get_value_or_default(row.word),
                get_value_or_default(row.description),
                get_value_or_default(row.ste_example),
                get_value_or_default(row.nonste_example),
            )

        return result
