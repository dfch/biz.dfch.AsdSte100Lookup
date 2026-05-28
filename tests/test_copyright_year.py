# Copyright (c) 2024 - 2025 d-fens GmbH, http://d-fens.ch
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

# pylint: disable=C0114
# pylint: disable=C0115
# pylint: disable=C0116
# pylint: disable=C0301

"""Module update copyright."""

from pathlib import Path
import os
import re
import subprocess
import unittest


@unittest.skipIf(
    os.getenv('GITHUB_ACTIONS') == 'true',
    "This 'test' does change source files. Do only start it locally.")
class TestCopyright(unittest.TestCase):
    """Change copyright year to include specified year."""

    CURRENT_YEAR = "2026"  # or str(datetime.now().year)

    _pattern = re.compile(
        r"^(# Copyright \(c\) )(.+?)(http://d-fens\.ch)$"
    )

    def _update_line(self, value: str) -> str | None:
        m = self._pattern.match(value)
        if not m:
            return None
        prefix, years_part, suffix = m.groups()
        years = re.findall(r"\d{4}", years_part)
        if not years:
            return None

        min_year = min(years)
        max_year = max(years)
        if self.CURRENT_YEAR == max_year:
            return None
        updated_years = f"{min_year} - {self.CURRENT_YEAR}"

        return f"{prefix}{updated_years}{suffix}"

    def _update_file(self, path: Path, *, dry_run: bool = False) -> bool:
        assert path.exists(), path
        lines = path.read_text(encoding="utf-8").splitlines()
        if not lines:
            return False

        updated = self._update_line(lines[0])
        if not updated:
            return False

        if dry_run:
            lines[0] = updated
            path.write_text(  # NOSONAR python:S2083
                "\n".join(lines) + "\n",
                encoding="utf-8"
            )
        return True

    def _get_files(self, path: Path) -> list[Path]:

        result: list[Path] = []

        # git log --since="2026-01-01" --name-only --pretty=format:
        cmd = [
            "git.exe",
            "log",
            f'--since="{self.CURRENT_YEAR}-01-01"',
            "--name-only",
            "--pretty=format:",
        ]
        git_result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        file_names = sorted({
            e.strip() for e
            in git_result.stdout.splitlines()
            if e.strip().lower().endswith(".py")
        })
        for file_name in file_names:
            full_name = path / file_name
            if not Path.exists(full_name):
                continue
            result.append(full_name)

        return result

    def test_update_copyright_year(self):

        project_dir = Path(__file__).resolve().parent.parent

        files = self._get_files(project_dir)

        for file in files:
            print(f"{file}")
            self._update_file(file, dry_run=False)

    def test_needs_update_copyright_year(self):

        project_dir = Path(__file__).resolve().parent.parent

        files = self._get_files(project_dir)

        for file in files:
            print(f"{file}")
            result = self._update_file(file, dry_run=True)

            self.assertFalse(result, file)


if __name__ == "__main__":
    unittest.main()
