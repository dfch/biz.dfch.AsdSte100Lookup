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


"""TestUnittestFramework class."""

import unittest


class TestUnittestFramework(unittest.TestCase):
    """This test class makes sure, that `unittest` operates correctly."""

    def test_unittest_succeeds(self):
        """Make sure, that `unittest` operates correctly."""

        self.assertIsNotNone(unittest)
