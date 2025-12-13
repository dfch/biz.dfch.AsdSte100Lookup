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

"""RuleGrouper class."""

from collections import defaultdict

from .rule import Rule


class RuleGrouper:  # pylint: disable=R0903
    """Groups rules by section and category."""

    rules: list[Rule]

    def __init__(self, rules: list[Rule]):
        assert isinstance(rules, list)

        self.rules = rules

    def invoke(
        self,
    ) -> dict[str, dict[str, list[Rule]]]:
        """
        Group rules by section, then by category.

        Returns:
            {
            section: {
                category: [Rule, Rule, ...],
                ...
            },
            ...
            }
        """
        grouped: dict[str, dict[str, list[Rule]]] = defaultdict(
            lambda: defaultdict(list)
        )

        for rule in self.rules:
            grouped[rule.section][rule.category].append(rule)

        return {
            section: dict(categories) for section, categories in grouped.items()
        }
