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

from .constant import Constant


class Args:
    """
    Definition and handling of supported command line arguments.
    """

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
            description=f"{Constant.PROG_NAME}, "
            f"v{Constant._VERSION}"
            ". "
            "A dictionary lookup tool for ASD-STE100.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
            prog=Constant.PROG_NAME,
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
            default=Constant.DICTIONARY_FILE,
            required=False,
            help="Name of the dictionary file to read entries from "
            f"(default: {Constant.DICTIONARY_FILE}).",
        )

        dictionary_parser.add_argument(
            "--no-random-word",
            action="store_true",
            help="Prevent display of random word at startup.",
        )

        rules_parser = subparsers.add_parser(
            "rules", parents=[common], help="Shows the rules."
        )
        rules_group = rules_parser.add_mutually_exclusive_group()
        rules_group.add_argument(
            "--list",
            action="store_true",
            help="Shows all rules.")
        rules_group.add_argument(
            "--id",
            type=str,
            help="Shows rules by specified id (regex match)."
        )
        rules_group.add_argument(
            "--section",
            type=str,
            help="Shows rules by specified section (regex match).",
        )
        rules_group.add_argument(
            "--category",
            type=str,
            help="Shows rules by specified category (regex match).",
        )
        rules_parser.add_argument(
            "--summary",
            action="store_true",
            help="Shows only the summary of a rule."
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
            default=Constant.DICTIONARY_FILE,
            required=False,
            help="Name of the dictionary file to save entries to "
            f"(default: {Constant.DICTIONARY_FILE}).",
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
