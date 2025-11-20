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

"""Arg parsing module."""

from __future__ import annotations

import argparse


class Args:
    """
    Definition and handling of supported command line arguments.
    """

    # Note: also adjust in pyproject.toml
    _VERSION = "1.2.0"
    _PROG_NAME = "AsdSte100Lookup"

    _parser: argparse.ArgumentParser

    LOG_LEVEL_CHOICES = [
        "CRITICAL",
        "FATAL",
        "ERROR",
        "WARNING",
        "WARN",
        "INFO",
        "DEBUG",
        "NOTSET",
    ]
    _DEFAULT_LOG_LEVEL = "ERROR"

    _DICTIONARY_FILE = "dictionary.json"

    def __init__(self):

        common = argparse.ArgumentParser(add_help=False)
        common.add_argument(
            "--log-level",
            "-l",
            dest="log_level",
            choices=self.LOG_LEVEL_CHOICES,
            # default=self._DEFAULT_LOG_LEVEL,
            help=f"Logging level (default: {self._DEFAULT_LOG_LEVEL}).",
        )
        common.add_argument(
            "-v",
            action="count",
            default=0,
            help="Increase verbosity (-v = WARNING, -vv = INFO, -vvv = DEBUG).",
        )

        self._parser = argparse.ArgumentParser(
            description=f"{self._PROG_NAME}, "
            f"v{self._VERSION}"
            ". "
            "A dictionary lookup tool for ASD-STE100.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=self._PROG_NAME,
            epilog="Copyright 2025 Ronald Rink, "
            "https://github.com/dfch/biz.dfch.AsdSte100Lookup"
            ". "
            "Licensed under GPLv3."
            "\n\n"
            "ASD-STE100 Simplified Technical English "
            "(Standard for Technical Documentation), Issue 9"
            "\n"
            "Copyright 2025 Aerospace, Security and Defence "
            "Industries Association of Europe (ASD)"
            ", "
            "https://www.asd-europe.org"
            ".",
        )

        subparsers = self._parser.add_subparsers(
            dest="command", help="Available commands."
        )

        dictionary_parser = subparsers.add_parser(
            "dictionary", parents=[common], help="Queries the dictionary."
        )

        dictionary_parser.add_argument(
            "-i",
            "--input",
            default=self._DICTIONARY_FILE,
            required=False,
            help="Name of the dictionary file to read entries from "
            f"(default: {self._DICTIONARY_FILE}).",
        )

        parse_parser = subparsers.add_parser(
            "parse", parents=[common], help="Parses input dictionary files."
        )

        parse_path_default = "ASD-STE100/v3/txt"
        parse_parser.add_argument(
            "-p",
            "--path",
            default=parse_path_default,
            required=False,
            help="Path with dictionary files "
            f"(default: '{parse_path_default}').",
        )

        parse_prefix_default = "ASD-STE100 - "
        parse_parser.add_argument(
            "--prefix",
            default=parse_prefix_default,
            required=False,
            help="Prefix of files in path "
            f"(default: '{parse_prefix_default}').",
        )
        parse_extension_default = ".txt"
        parse_parser.add_argument(
            "-ext",
            "--extension",
            default=parse_extension_default,
            required=False,
            help="Extension of files in path "
            f"(default: '{parse_extension_default}').",
        )

        parse_parser.add_argument(
            "-o",
            "--output",
            default=self._DICTIONARY_FILE,
            required=False,
            help="Name of the dictionary file to save entries to "
            f"(default: {self._DICTIONARY_FILE}).",
        )

    @staticmethod
    def get_effective_log_level_name(args) -> str:
        """Returns the effective log level name."""

        result = Args._DEFAULT_LOG_LEVEL

        # Explicit specification of --log-level takes precedence.
        if hasattr(args, "log_level") and args.log_level:
            result = args.log_level.upper()
            return result

        # Return default log level if no "-v" is specified.
        if not hasattr(args, "v"):
            return result

        # Otherwise map verbosity count to log level.
        if args.v >= 3:
            result = "DEBUG"
            return result

        if args.v == 2:
            result = "INFO"
            return result

        if args.v == 1:
            result = "WARNING"
            return result

        return result

    def invoke(self) -> argparse.ArgumentParser:
        """
        Initialise supported command line arguments.
        """

        return self._parser
