# Copyright (c) 2025 - 2026 Ronald Rink, http://d-fens.ch
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

# pylint: disable=C0415
# pylint: disable=E0401
# noqa: E501

"""Application entry point as script."""

from biz.dfch.asdste100lookup.args import Args
from biz.dfch.asdste100lookup.app import App


def main():
    """main"""

    parser = Args().invoke()

    App(parser).invoke()


if __name__ == "__main__":
    main()
