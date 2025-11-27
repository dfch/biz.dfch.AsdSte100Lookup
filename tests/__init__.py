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


"""tests module."""

import sys
import os

# Adjust path, to include src tree.
sys.path.insert(0, os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "src")))


# Only import after adjusting the path.
from biz.dfch.i18n import I18n  # pylint: disable=C0413  # noqa: E402
I18n.Factory.create()


# run from project root with either
# $ python -m unittest discover
# or
# $ python -m unittest discover tests -t .
# or
# $ python -m unittest discover tests/<specific_package> -t .
# or
# $ python -m unittest discover -s tests -t . -p test_*.py
