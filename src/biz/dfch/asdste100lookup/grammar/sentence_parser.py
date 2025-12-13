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

"""SentenceParser class."""

from collections.abc import Iterable
from enum import StrEnum


class SentenceParserErrorType(StrEnum):
    """Possible `SentenceParserError` error types."""

    NESTED_QUOTES = "Nested quotes in text."
    UNCLOSED_QUOTE = "Unclosed quote in text."
    UNMATCHED_CLOSING_QUOTE = "Unmatched closing quote in text."
    MISMATCHED_CLOSING_QUOTE = "Mismatched closing quote in text."


class SentenceParserError(Exception):
    """Raised when the sentence has invalid quoting (nested or unmatched)."""


class SentenceParser:
    """
    Analyze sentences with custom rules.

    Rules for word_count:
      - Hyphenated tokens like 'pre-measure' count as 1 word.
      - Text inside configured quotes (e.g. "Big Mountain" or 'Big Mountain')
        counts as 1 word total, regardless of internal spaces.
      - Nested quotes and unmatched quotes are considered invalid and raise
        SentenceParserError.
    """

    def __init__(
        self, quote_pairs: Iterable[tuple[str, str]] | None = None
    ) -> None:
        """
        Args:
            quote_pairs: iterable of (open_quote, close_quote), optional
                Example default: [('"', '"'), ("'", "'")]
        """
        if quote_pairs is None:
            quote_pairs = [('"', '"'), ("'", "'")]

        self.quote_pairs: list[tuple[str, str]] = list(quote_pairs)
        self._open_to_close = dict(self.quote_pairs)
        self._opening_chars = set(self._open_to_close.keys())
        self._closing_chars = {close_q for _, close_q in self.quote_pairs}

    def word_count(self, text: str) -> int:
        """
        Count words in `text` using the class rules.

        Raises:
            SentenceParserError: If nested quotes or unmatched quotes are
                detected.
        """
        i = 0
        n = len(text)
        words = 0

        # Track whether we're inside a quoted segment
        in_quote = False
        active_close = None

        while i < n:
            # Skip leading whitespace
            while i < n and text[i].isspace():
                i += 1

            if i >= n:
                break

            ch = text[i]

            # Case 1: word starts with a recognized opening quote
            if ch in self._opening_chars:
                # If we're already in a quote and encounter a new opening quote,
                # that's nested quoting -> error
                if in_quote:
                    raise SentenceParserError(
                        SentenceParserErrorType.NESTED_QUOTES
                    )

                in_quote = True
                active_close = self._open_to_close[ch]
                i += 1  # move past opening quote

                # Consume until matching closing quote or end of string.
                while i < n and text[i] != active_close:
                    # If we find another opening quote of any kind inside,
                    # it is nested.

                    if text[i] in self._opening_chars:
                        raise SentenceParserError(
                            SentenceParserErrorType.NESTED_QUOTES
                        )
                    i += 1

                # If we reached end without finding the closing quote
                if i >= n:
                    raise SentenceParserError(
                        SentenceParserErrorType.UNCLOSED_QUOTE
                    )

                # We are on the closing quote now
                if text[i] != active_close:
                    # Sanity check (should not happen due to while condition)
                    raise SentenceParserError(
                        "Mismatched closing quote in text."
                    )

                # Move past the closing quote, end of this quoted word
                i += 1
                in_quote = False
                active_close = None
                words += 1

            else:
                # If we see a closing quote without a matching open quote,
                # this is an error.
                if ch in self._closing_chars:
                    raise SentenceParserError(
                        SentenceParserErrorType.UNMATCHED_CLOSING_QUOTE
                    )

                # Case 2: normal word (sequence of non-whitespace)
                while i < n and not text[i].isspace():
                    # A stray closing quote inside a normal word is also invalid
                    if text[i] in self._closing_chars:
                        raise SentenceParserError(
                            SentenceParserErrorType.UNMATCHED_CLOSING_QUOTE
                        )
                    i += 1
                words += 1

        # If we somehow exit the loop while still in a quote,
        # that should have been caught earlier.
        if in_quote:
            raise SentenceParserError(SentenceParserErrorType.UNCLOSED_QUOTE)

        return words
