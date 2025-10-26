# MIT License

# Copyright (c) 2025 d-fens GmbH, http://d-fens.ch

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

"""Module i18n."""

from __future__ import annotations
import os
from pathlib import Path
import sys
from threading import Lock
from typing import ClassVar

from .language_code import LanguageCode


class I18n:
    """Internationalisation module."""

    _RES_PATH = "res"

    _path: str

    def __init__(self, value: str):

        if not I18n.Factory._sync_root.locked():
            raise RuntimeError("Private ctor. Use Factory instead.")

        assert value is not None and isinstance(value, str)

        self._path = value

    class Factory:  # pylint: disable=R0903
        """Factory class for creating `I18n` instances."""

        __instance: ClassVar[I18n | None] = None
        _sync_root: ClassVar[Lock] = Lock()

        @staticmethod
        def _reset(value: str | None = None) -> None:
            """Internal: Reset the initial value of the path."""

            assert I18n.Factory.__instance

            if not value:
                value = ""

            with I18n.Factory._sync_root:
                I18n._path = value  # pylint: disable=W0212

        @staticmethod
        def create(value: str | None = None) -> I18n:
            """Creates the `I18n` singleton instance.

            Args:
                value (str | None): A relative path, "" or None. Default is
                    `None`.

            Returns:
                I18: An instance of the object.

            Raises:
                AssertionError: If the instance has already been created.
            """

            assert not I18n.Factory.__instance

            if not value:
                value = ""

            with I18n.Factory._sync_root:
                assert not I18n.Factory.__instance

                I18n.Factory.__instance = I18n(value)

            return I18n.Factory.__instance

        @staticmethod
        def get() -> I18n:
            """Returns the `I18n` singleton instance.

            Returns:
                I18: An instance of the object.

            Raises:
                AssertionError: If the instance has not been created.
            """

            assert I18n.Factory.__instance

            return I18n.Factory.__instance

    def get_runtime_path(self, relative_path: str) -> str:
        """Resolves a relative path to the runtime path.

        Args:
            relative_path (str): The relative (to __main__.py) path to
                translate.

        Returns:
            str: The runtime path depending on the environment (frozen or
                source).

        Raises:
            AssertionError: If relative_path is None or "".
        """

        assert relative_path and relative_path.strip()

        if getattr(sys, "frozen", False):
            # Determine whether we run as binary "onefile".
            base_path = getattr(sys, "_MEIPASS", None)
            assert base_path
        else:
            base_path = os.path.join(os.getcwd(), self._path)

        return os.path.normpath(os.path.join(base_path, relative_path))

    def get_resource_path(
            self,
            item: str,
            code: LanguageCode | None = None
    ) -> str:
        """Returns the normalised resource path for an item.

        Args:
            item (str): The item to join with the _RES_PATH.
            code (LanguageCode | None): If specified, the language code will be
                infixed as a sub directory under _RES_PATH

        Returns:
            str: The normalised path (without resolving links).

        Raises:
            AssertionError: If item is None or "".
        """

        assert item and item.strip()

        path = Path(item)

        if code is not None:
            if code is LanguageCode.DEFAULT:
                code = LanguageCode.EN
            result = os.path.join(I18n._RES_PATH, code.name, path)
        else:
            result = os.path.join(I18n._RES_PATH, path)

        return self.get_runtime_path(result)
