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

"""TestSentenceParser test class."""

import unittest

from biz.dfch.asdste100lookup.grammar.sentence_parser import SentenceParser
from biz.dfch.asdste100lookup.grammar.sentence_parser import SentenceParserError


class TestSentenceParser(unittest.TestCase):
    """
    Tests for the SentenceParser word counting and quote validation logic.
    """

    sut: SentenceParser

    def setUp(self) -> None:
        """Create a default SentenceParser instance for each test."""

        self.sut = SentenceParser()  # default quote pairs: "..." and '...'

    def test_simple_words(self) -> None:
        """Simple space-separated words are counted individually."""

        self.assertEqual(self.sut.word_count("This is a test"), 4)

    def test_hyphenated_word(self) -> None:
        """Hyphenated tokens should be counted as a single word."""

        self.assertEqual(self.sut.word_count("pre-measure"), 1)
        self.assertEqual(self.sut.word_count("pre-measure test"), 2)

    def test_double_quoted_phrase(self) -> None:
        """A phrase in double quotes counts as a single word."""

        text = 'He said "Big Mountain" today'
        # ["He", "said", "Big Mountain", "today"]
        self.assertEqual(self.sut.word_count(text), 4)

    def test_single_quoted_phrase(self) -> None:
        """A phrase in single quotes counts as a single word."""

        text = "He said 'Big Mountain' today"
        # ["He", "said", "Big Mountain", "today"]
        self.assertEqual(self.sut.word_count(text), 4)

    def test_multiple_quoted_phrases(self) -> None:
        """Multiple quoted phrases each count as one word."""

        text = '"Big Mountain" "Small Hill"'
        # ["Big Mountain", "Small Hill"]
        self.assertEqual(self.sut.word_count(text), 2)

    def test_whitespace_and_newlines(self) -> None:
        """Extra whitespace, newlines, and tabs do not affect word semantics."""

        text = "  This   is\n\n  spaced\tout  "
        # ["This", "is", "spaced", "out"]
        self.assertEqual(self.sut.word_count(text), 4)

    # ---------- Error conditions ----------

    def test_nested_quotes_error_double_in_double(self) -> None:
        """
        Nested quotes (double inside double) should raise SentenceParserError.
        """

        text = "He said \"Big 'Mountain'\" today"
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_nested_quotes_error_single_in_single(self) -> None:
        """
        Nested quotes (single inside single) should raise SentenceParserError.
        """

        text = "He said 'Big \"Mountain\"' today"
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_nested_quotes_error_multiple_open(self) -> None:
        """
        Multiple openings before a close constitute nested quotes and error.
        """

        text = '"Big "Mountain""'
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_unmatched_open_quote_error_double(self) -> None:
        """
        An unmatched double quote at the end should raise SentenceParserError.
        """

        text = 'He said "Big Mountain today'
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_unmatched_open_quote_error_single(self) -> None:
        """
        An unmatched single quote at the end should raise SentenceParserError.
        """

        text = "He said 'Big Mountain today"
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_orphan_closing_quote_error(self) -> None:
        """A closing quote without a prior opener should raise
        SentenceParserError.
        """

        text = 'He said Big Mountain" today'
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_orphan_closing_quote_in_word_error(self) -> None:
        """
        A stray closing quote inside a normal word should raise
        SentenceParserError.
        """

        text = 'He said Big"Mountain today'
        with self.assertRaises(SentenceParserError):
            self.sut.word_count(text)

    def test_custom_quote_pairs_ok(self) -> None:
        """
        Custom quote pairs should be honored for grouping words.
        """

        parser = SentenceParser(quote_pairs=[("«", "»")])
        text = "He said «Big Mountain» today"
        self.assertEqual(parser.word_count(text), 4)

    def test_custom_quote_pairs_nested_error(self) -> None:
        """
        Nested custom quote pairs should raise SentenceParserError.
        """

        parser = SentenceParser(quote_pairs=[("«", "»"), ("[", "]")])
        text = "He said «Big [Mountain]» today"
        with self.assertRaises(SentenceParserError):
            parser.word_count(text)

    def test_empty_string(self) -> None:
        """
        An empty string should have a word count of 0.
        """

        self.assertEqual(self.sut.word_count(""), 0)

    def test_only_whitespace(self) -> None:
        """
        A string with only whitespace characters should have a word count of 0.
        """

        self.assertEqual(self.sut.word_count("   \n\t  "), 0)

    def test_quoted_empty_string(self) -> None:
        """
        An empty quoted string should be treated as a single word.
        """

        text = '""'
        self.assertEqual(self.sut.word_count(text), 1)

    def test_multiple_hyphens(self) -> None:
        """
        A token with multiple hyphens still counts as a single word.
        """

        text = "pre-post-measure test"
        self.assertEqual(self.sut.word_count(text), 2)


if __name__ == "__main__":
    unittest.main()
