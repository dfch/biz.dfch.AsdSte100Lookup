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

"""commands package."""

from .command_base import CommandBase
from .dictionary_command import DictionaryCommand
from .empty_command import EmptyCommand
from .erase_console_buffer_command import EraseConsoleBufferCommand
from .exit_command import ExitCommand
from .help_command import HelpCommand
from .rule_command import RuleCommand
from .save_command import SaveCommand
from .unknown_command import UnknownCommand
from .word_category_command import WordCategoryCommand

__all__ = [
    "CommandBase",
    "DictionaryCommand",
    "EmptyCommand",
    "EraseConsoleBufferCommand",
    "ExitCommand",
    "HelpCommand",
    "RuleCommand",
    "SaveCommand",
    "UnknownCommand",
    "WordCategoryCommand",
]
