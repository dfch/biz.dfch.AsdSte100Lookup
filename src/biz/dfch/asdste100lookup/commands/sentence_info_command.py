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

"""SentenceInfoCommand class."""

from dataclasses import dataclass

from .erase_console_buffer_command import EraseConsoleBufferCommand

from ..grammar.sentence_parser import SentenceParser
# from ..grammar.sentence_parser import SentenceParserError
# from ..grammar.sentence_parser import SentenceParserErrorType


@dataclass
class SentenceInfoCommand(EraseConsoleBufferCommand):
    """Represents the sentence info command."""

    def invoke(self, console, dictionary, rules):
        super().invoke(console, dictionary, rules)

        parser = SentenceParser()
        result = parser.word_count(self.value)
        console.print(f"[{result}] {self.value}")
