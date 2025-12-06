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

"""DictionaryWord class."""

from dataclasses import dataclass

from .word_status import WordStatus
from .word_type import WordType


@dataclass
class DictionaryWord:
    """Represents a word from the dictionary."""

    name: str = ""
    type_: WordType = WordType.UNKNOWN
    status: WordStatus = WordStatus.UNKNOWN
