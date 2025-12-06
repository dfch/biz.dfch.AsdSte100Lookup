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

"""WordType enumeration."""

from enum import StrEnum


class WordType(StrEnum):
    """ASD-STE100 Issue 9 word types; cf. page 2-0-4f."""

    UNKNOWN = "unknown"
    NOUN = "n"
    VERB = "v"
    ADJECTIVE = "adj"
    ADVERB = "adv"
    PRONOUN = "pron"
    ARTICLE = "art"
    PREPOSITION = "prep"
    CONJUNCTION = "conj"
    PREFIX = "prefix"
    TECHNICAL_NOUN = "TN"
    TECHNICAL_VERB = "TV"
