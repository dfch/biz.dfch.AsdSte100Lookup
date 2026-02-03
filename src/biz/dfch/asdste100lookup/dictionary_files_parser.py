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

"""DictionaryFilesParser class."""

from dataclasses import asdict
import json
from pathlib import Path

from biz.dfch.logging import log

from .constant import Constant
from .dictionary_info import DictionaryInfo
from .line_info import LineInfo
from .line_info_type import LineInfoType
from .utils import get_value_or_default
from .word import Word
from .word_info import WordInfo
from .word_meaning import WordMeaning
from .word_note import WordNote
from .word_source import WordSource
from .word_state import WordState
from .word_status import WordStatus


class DictionaryFilesParser:
    """Methods related to parsing dictionary files."""

    def _process_lines(self, lines: list[str]) -> list[LineInfo]:

        result: list[LineInfo] = []

        for line in lines:
            line_info = LineInfo()
            line_info.line = line.strip("\ufeff")
            line_info.tokens = line_info.line.split("\t")
            line_info.tokens_count = len(line_info.tokens)
            if not line_info.tokens:
                continue

            token = line_info.tokens[0]
            if DictionaryInfo.is_word(token):
                line_info.is_start_of_word = True

            log.debug(
                "[%s] [%s] %s",
                line_info.tokens_count,
                line_info.is_start_of_word,
                line_info.line,
            )

            for index, token in enumerate(line_info.tokens):
                log.debug("[%s/%s] '%s'", index, line_info.tokens_count, token)

            result.append(line_info)

        return result

    def process_file(self, file: Path) -> tuple[list[LineInfo], list[WordInfo]]:
        """Parses a single OCR dictionary file."""

        assert file is not None and isinstance(file, Path)

        log.debug("Processing file '%s' ...", file.name)

        lines: list[str] = []
        with open(file, "r", encoding="utf-8") as f:

            for line in f:
                if not line:
                    continue

                lines.append(line)

        line_infos: list[LineInfo] = []
        word_infos: list[WordInfo] = []
        result: tuple[list[LineInfo], list[WordInfo]] = (line_infos, word_infos)

        if not lines:
            log.warning(
                "Processing file '%s' FAILED. "
                "File does not contain text. "
                "Skipping file.",
                file.name,
            )
            return result

        line_infos.extend(self._process_lines(lines))

        word_info: WordInfo = WordInfo(file.name)
        for index, line_info in enumerate(line_infos):
            log.debug(
                "[%s] [%s] '%s'", word_info.filename, index, line_info.line
            )
            if 0 == index:
                assert line_info.is_start_of_word

            if line_info.is_start_of_word:
                word_info = WordInfo(file.name)
                word = DictionaryInfo.get_word(line_info.tokens[0])
                assert word is not None
                assert WordStatus.UNKNOWN != word.status

                word_info.word = word
                word_infos.append(word_info)

            word_info.line_infos.append(line_info)

        for word_info in word_infos:
            log.debug("%s", word_info.line_infos[0].tokens[0])
            log.debug(
                "'%s' [%s] %s [#%s]",
                word_info.word.name,
                word_info.word.type_,
                word_info.word.status,
                len(word_info.line_infos),
            )

        log.info("Processing file '%s' SUCCEEDED.", file.name)

        return result

    def process_wordinfo(self, item: WordInfo) -> Word | None:
        """Processes a WordInfo."""

        assert item is not None

        # Process first line_info.
        current_state = WordState.INITIAL
        assert 0 < len(item.line_infos)
        line_info = item.line_infos[0]
        next_state = self.get_next_state(current_state, line_info)
        log.debug(
            "[%s] [%s --> %s] @ %s: %s",
            item.filename,
            current_state.name,
            next_state.name,
            line_info.get_type().name,
            line_info.line,
        )
        assert WordState.ERROR != next_state
        previous_state = current_state
        current_state = next_state

        name = line_info.get_name()
        assert name
        description = line_info.get_description()
        assert description
        ste = line_info.get_ste()
        non_ste = line_info.get_nonste()
        spellings = DictionaryInfo.get_spellings(name)

        match current_state:
            case WordState.WORD_MEANING:
                meaning = WordMeaning(
                    value=description,
                    ste_example=get_value_or_default(ste),
                    nonste_example=get_value_or_default(non_ste),
                )
                result = Word(
                    status=item.word.status,
                    name=item.word.name,
                    type_=item.word.type_,
                    source=WordSource.STE100_9,
                    meanings=[meaning],
                    spellings=spellings,
                    alternatives=[],
                    note=WordNote(value=""),
                )
            case WordState.WORD_ALTERNATIVE:
                alt_word = DictionaryInfo.get_single_word(description)
                assert alt_word
                alternative = Word(
                    status=alt_word.status,
                    name=alt_word.name,
                    type_=alt_word.type_,
                    source=WordSource.STE100_9,
                    meanings=[],
                    spellings=[],
                    alternatives=[],
                    ste_example=[],
                    nonste_example=[],
                )
                if ste:
                    alternative.ste_example.append(ste)
                if non_ste:
                    alternative.nonste_example.append(non_ste)
                result = Word(
                    status=item.word.status,
                    name=item.word.name,
                    type_=item.word.type_,
                    source=WordSource.STE100_9,
                    meanings=[],
                    spellings=spellings,
                    alternatives=[alternative],
                    note=WordNote(value=""),
                )
            case WordState.WORD_NOTE:
                result = Word(
                    status=item.word.status,
                    name=item.word.name,
                    type_=item.word.type_,
                    source=WordSource.STE100_9,
                    meanings=[],
                    spellings=spellings,
                    alternatives=[],
                    note=WordNote(
                        value=DictionaryInfo.get_note(description),
                        ste_example=get_value_or_default(ste),
                        nonste_example=get_value_or_default(non_ste),
                    ),
                )
            case _:
                raise ValueError(
                    f"[{previous_state}] --> [{current_state}] "
                    f"@ {line_info.get_type().name}: '{line_info}'"
                )
        assert result

        for line_info in item.line_infos[1:]:
            next_state = self.get_next_state(current_state, line_info)
            log.debug(
                "[%s] [%s --> %s] @ %s: %s",
                item.filename,
                current_state.name,
                next_state.name,
                line_info.get_type().name,
                line_info.line,
            )
            assert (
                WordState.ERROR != next_state
            ), f"current_state: {current_state} [{line_info}]."
            previous_state = current_state
            current_state = next_state

            description = line_info.get_description()
            ste = line_info.get_ste()
            non_ste = line_info.get_nonste()
            match current_state:
                case WordState.NOTE:
                    assert description
                    assert result.note
                    result.note.value = DictionaryInfo.get_note(description)
                    result.note.ste_example = get_value_or_default(ste)
                    result.note.nonste_example = get_value_or_default(non_ste)
                case WordState.MEANING:
                    meaning = WordMeaning(
                        value=get_value_or_default(description),
                        ste_example=get_value_or_default(ste),
                        nonste_example=get_value_or_default(non_ste),
                    )
                    result.meanings.append(meaning)
                case WordState.MEANING_EXAMPLE:
                    meaning = WordMeaning(
                        value=description or Constant.BLOCKING_WHITE_SPACE,
                        ste_example=get_value_or_default(ste),
                        nonste_example=get_value_or_default(non_ste),
                    )
                    result.meanings.append(meaning)
                case WordState.ALTERNATIVE:
                    assert description
                    alt_word = DictionaryInfo.get_single_word(description)
                    assert alt_word
                    alternative = Word(
                        status=alt_word.status,
                        name=alt_word.name,
                        type_=alt_word.type_,
                        source=WordSource.STE100_9,
                        meanings=[],
                        spellings=[],
                        alternatives=[],
                        ste_example=[],
                        nonste_example=[],
                    )
                    if ste:
                        alternative.ste_example.append(ste)
                    if non_ste:
                        alternative.nonste_example.append(non_ste)

                    result.alternatives.append(alternative)
                case WordState.ALTERNATIVE_EXAMPLE:
                    log.warning(
                        "[%s] ALTERNATIVE_EXAMPLE '%s (%s)': "
                        "alternative '%s' has multiple examples.",
                        item.filename,
                        item.word.name,
                        item.word.type_,
                        result.alternatives[-1].name,
                    )
                    if ste:
                        result.alternatives[-1].ste_example.append(ste)
                    if non_ste:
                        result.alternatives[-1].nonste_example.append(non_ste)
                case WordState.NOTE_ALTERNATIVE:
                    assert description
                    assert result.note
                    assert description
                    alt_word = DictionaryInfo.get_single_word(description)
                    assert alt_word
                    alternative = Word(
                        status=alt_word.status,
                        name=alt_word.name,
                        type_=alt_word.type_,
                        source=WordSource.STE100_9,
                        meanings=[],
                        spellings=[],
                        alternatives=[],
                        ste_example=[],
                        nonste_example=[],
                    )
                    if ste:
                        alternative.ste_example.append(ste)
                    if non_ste:
                        alternative.nonste_example.append(non_ste)
                    result.note.words.append(alternative)
                case WordState.NOTE_ALTERNATIVE_EXAMPLE:
                    assert result.note
                    log.warning(
                        "[%s] NOTE_ALTERNATIVE_EXAMPLE '%s (%s)': "
                        "alternative '%s' has multiple examples.",
                        item.filename,
                        item.word.name,
                        item.word.type_,
                        result.note.words[-1].name,
                    )
                case _:
                    raise ValueError(
                        f"[{previous_state}] --> [{current_state}] "
                        f"@ {line_info.get_type().name}: '{line_info}'"
                    )

        return result

    def invoke(
        self, path: Path, prefix: str, extension: str, dictionary_file_name: str
    ) -> None:
        """Parse OCR dictionary files."""

        assert path is not None and isinstance(path, Path)
        assert prefix is not None and "" != prefix
        assert extension is not None and "" != extension
        assert dictionary_file_name is not None and "" != dictionary_file_name

        log.debug("Parsing files in '%s' ...", path)

        files = [
            f
            for f in path.iterdir()
            if (
                f.is_file()
                and f.name.startswith(prefix)
                and f.suffix == extension
            )
        ]

        word_infos: list[WordInfo] = []
        for file in files:

            _, info = self.process_file(file)
            word_infos.extend(info)

        words: list[Word] = []
        for word_info in word_infos:

            word = self.process_wordinfo(word_info)
            if word is None:
                continue
            words.append(word)
            log.debug("word: [%s]", word)

        current_folder = Path(__file__).parent
        parsed_words_dicts = [asdict(entry) for entry in words]
        with open(
            file=(current_folder / dictionary_file_name),
            mode="w",
            encoding="utf-8",
            newline="\n",
        ) as f:
            json.dump(parsed_words_dicts, f, indent=2)

    def get_next_state(
        self, current_state: WordState, line_info: LineInfo
    ) -> WordState:
        """Returns the next state based on the current state and line_info."""

        assert line_info is not None

        next_state: WordState = WordState.ERROR
        line_info_type = line_info.get_type()

        if WordState.INITIAL == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.WORD_MEANING
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.WORD_ALTERNATIVE
            if LineInfoType.NOTE == line_info_type:
                return WordState.WORD_NOTE

        if WordState.WORD_MEANING == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.MEANING
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.MEANING_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.WORD_ALTERNATIVE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.ALTERNATIVE_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.WORD_NOTE == current_state:
            return WordState.ERROR

        if WordState.MEANING == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.MEANING
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.MEANING_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.MEANING_EXAMPLE == current_state:
            if LineInfoType.MEANING == line_info_type:
                return WordState.MEANING
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.MEANING_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.ALTERNATIVE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.ALTERNATIVE_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE
        if WordState.ALTERNATIVE_EXAMPLE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.ALTERNATIVE_EXAMPLE
            if LineInfoType.NOTE == line_info_type:
                return WordState.NOTE

        if WordState.NOTE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.NOTE_ALTERNATIVE
        if WordState.NOTE_ALTERNATIVE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.NOTE_ALTERNATIVE
            if LineInfoType.EXAMPLE == line_info_type:
                return WordState.NOTE_ALTERNATIVE_EXAMPLE
        if WordState.NOTE_ALTERNATIVE_EXAMPLE == current_state:
            if LineInfoType.ALTERNATIVE == line_info_type:
                return WordState.NOTE_ALTERNATIVE

        return next_state
