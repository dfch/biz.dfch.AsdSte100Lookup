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

"""RuleTechnicalWordsParser class."""

import re

from .rule import Rule
from .rule_content_type import RuleContentType
from .technical_word_category import TechnicalWordCategory
from .word import Word
from .word_note import WordNote
from .word_source import WordSource
from .word_status import WordStatus
from .word_type import WordType


class RuleTechnicalWordsParser:
    """Parser for technical nouns and verbs from rule file."""

    def get_technical_words(
        self, rules: list[Rule], rule_id: str, prefix: str, type_: WordType
    ) -> list[Word]:
        """Returns all technical nouns from rule R1.5."""

        assert isinstance(rules, list)
        for rule in rules:
            assert isinstance(rule, Rule)

        result: list[Word] = []

        rule = next((r for r in rules if r.id_ == rule_id))
        assert isinstance(rule, Rule)

        current_category: str = ""
        contents = [d for d in rule.contents if d.type_ in ("text", "good")]
        for content in contents:
            if RuleContentType.TEXT == content.type_:
                match = re.match(r"^(?P<category>\d+)\.", content.data.strip())
                if not match:
                    continue
                current_category = f"{prefix}{match.group('category')}"
                continue

            category_word_list = content.data.split(", ")
            for category_word in category_word_list:
                note = WordNote(
                    value=f"See '{WordSource.STE100_9}' ({current_category})."
                )
                word = Word(
                    status=WordStatus.CUSTOM,
                    source=WordSource.STE100_9,
                    category=TechnicalWordCategory(current_category),
                    name=category_word.strip(),
                    type_=type_,
                    meanings=[],
                    spellings=[],
                    alternatives=[],
                    ste_example=[],
                    nonste_example=[],
                    note=note,
                )
                result.append(word)

        return result

    def invoke(self, rules: list[Rule]) -> list[Word]:
        """Returns all technical nouns and verbs from rules R1.5 and R1.12."""

        assert isinstance(rules, list)

        result: list[Word] = []

        result = self.get_technical_words(
            rules,
            rule_id="R1.5",
            prefix="TN",
            type_=WordType.TECHNICAL_NOUN
        )

        result.extend(
            self.get_technical_words(
                rules,
                rule_id="R1.12",
                prefix="TV",
                type_=WordType.TECHNICAL_VERB
            )
        )

        return result
