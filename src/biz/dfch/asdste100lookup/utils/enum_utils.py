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

"""enum_utils."""


def enum_key_from_value(enum_cls, value: str):
    """Returns an Enum key based on case-insenstivie value."""

    value_comparison = value.casefold()
    for m in enum_cls:
        if m.value.casefold() == value_comparison:
            return m.name

    raise KeyError(f"Invalid value for '{enum_cls.__name__}': '{value!r}'.")
