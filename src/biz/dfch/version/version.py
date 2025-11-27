# MIT License

# Copyright (c) 2024, 2025 d-fens GmbH, http://d-fens.ch

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Module version."""

import sys


class Version:  # pylint: disable=R0903
    """Version class ensuring minimum Python interpreter version."""

    def ensure_minimum_version(self, major: int = 3, minor: int = 11) -> None:
        """Ensures the currently running Python interpreter runs at least the
        specified version.

        Args:
            major (int): The minimum major version required.
            minor (int): The minimum minor version required.

        Returns:
            None:

        Raises:
            EnvironmentError: The exception is raised, when the specified
                version is not met by the currently running Python interpreter.
        """

        if sys.version_info >= (major, minor):
            return

        raise EnvironmentError(f"'{sys.version_info}' < '{major}.{minor}'")
