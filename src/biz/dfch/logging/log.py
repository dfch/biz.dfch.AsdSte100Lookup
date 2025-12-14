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

"""Module log"""

import logging
import logging.config

from biz.dfch.i18n import I18n

_LOGGER_NAME = "biz.dfch.asdste100lookup"
# Note: When using `pyinstaller --onefile` make sure this file is available.
_LOGGER_FILE = "logging.conf"


try:
    logging.config.fileConfig(I18n.Factory.get().get_runtime_path(_LOGGER_FILE))
    log = logging.getLogger(_LOGGER_NAME)

except Exception as ex:

    print(f"{_LOGGER_NAME}: An error occurred while trying to load "
          f"'{_LOGGER_FILE}': '{ex}'")

    raise
