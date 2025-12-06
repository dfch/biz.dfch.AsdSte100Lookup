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

"""FilterCommand class."""

from dataclasses import dataclass
from typing import ClassVar


from .command_base import CommandBase
from .word_filter_type import WordFilterType


@dataclass
class FilterCommand(CommandBase):
    """Represents an empty command."""

    _filter: ClassVar[dict] = {
        WordFilterType.TYPE: "",
        WordFilterType.STATUS: "",
        WordFilterType.SOURCE: "",
        WordFilterType.CATEGORY: "",
        WordFilterType.NOTE: "",
    }

    def __init__(self, type_: WordFilterType, value: str) -> None:
        super().__init__(value)

        match type_:
            case WordFilterType.RESET:
                self._filter[WordFilterType.TYPE] = ""
                self._filter[WordFilterType.STATUS] = ""
                self._filter[WordFilterType.SOURCE] = ""
                self._filter[WordFilterType.CATEGORY] = ""
                self._filter[WordFilterType.NOTE] = ""

                return

            case WordFilterType.LIST:
                for key, value in self._filter.items():
                    if isinstance(value, bool):
                        print(key, value)
                    elif isinstance(value, str) and "" != value.strip():
                        print(key, value)
                return

            case (
                WordFilterType.TYPE
                | WordFilterType.STATUS
                | WordFilterType.SOURCE
                | WordFilterType.CATEGORY
                | WordFilterType.NOTE
            ):
                assert isinstance(value, str) and "" != value.strip()

                self._filter[type_] = self.value
                return

            case _:
                raise ValueError(
                    f"Invalid {WordFilterType.__name__}: '{type_}'."
                )

    # pylint: disable=W0246
    def invoke(self, console, dictionary, rules) -> None:
        super().invoke(console, dictionary, rules)

        # We must implement abstract `invoke()`.

    @staticmethod
    def get_filter() -> dict:
        """Returns the currenty filter definition."""

        return FilterCommand._filter
