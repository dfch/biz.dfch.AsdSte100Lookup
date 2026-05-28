# Copyright (c) 2024 - 2026 http://d-fens.ch
#
# ... (license header remains the same)

"""Module update copyright."""

import unittest

from .test_copyright_year import TestCopyright


class TestTestCopyrightLine(unittest.TestCase):
    """Unit tests for _update_line without file system or git dependencies."""

    sut = TestCopyright()
    sut.current_year = "2026"

    def _update(self, line: str) -> str | None:
        return self.sut.update_line(line)  # pylint: disable=W0212

    def test_single_year_with_names(self):
        """Single year, with name and company."""
        result = self._update("# Copyright 2024 abc, xyz, http://d-fens.ch")
        self.assertEqual(
            result, "# Copyright 2024 - 2026 abc, xyz, http://d-fens.ch"
        )

    def test_two_years_with_names(self):
        """Two years, with name and company."""
        result = self._update(
            "# Copyright 2024, 2025 abc, xyz, http://d-fens.ch"
        )
        self.assertEqual(
            result, "# Copyright 2024 - 2026 abc, xyz, http://d-fens.ch"
        )

    def test_three_years_with_names(self):
        """Three years, with name and company."""
        result = self._update(
            "# Copyright 2024, 2025, 2026 abc, xyz, http://d-fens.ch"
        )
        self.assertIsNone(result)

    def test_range_with_names(self):
        """Year range, with name and company."""
        result = self._update(
            "# Copyright 2024 - 2025 abc, xyz, http://d-fens.ch"
        )
        self.assertEqual(
            result, "# Copyright 2024 - 2026 abc, xyz, http://d-fens.ch"
        )

    def test_single_year_no_extra_names(self):
        """Single year, with name."""
        result = self._update("# Copyright 2024 abc, http://d-fens.ch")
        self.assertEqual(
            result, "# Copyright 2024 - 2026 abc, http://d-fens.ch"
        )

    def test_already_current_year(self):
        """Year range, with name. And current year"""
        result = self._update("# Copyright 2024 - 2026 abc, http://d-fens.ch")
        self.assertIsNone(result)

    def test_no_match(self):
        """Comment line without match."""
        result = self._update("# Some other comment")
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
