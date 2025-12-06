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

"""WordInfo class."""

from dataclasses import dataclass, field

from .dictionary_word import DictionaryWord
from .line_info import LineInfo


@dataclass
class WordInfo:
    """Contains information about a word in the dictionary."""

    filename: str
    word: DictionaryWord = field(default_factory=DictionaryWord)
    line_infos: list[LineInfo] = field(default_factory=list)
