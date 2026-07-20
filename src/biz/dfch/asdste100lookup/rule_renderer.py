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

"""RuleRenderer class."""

from rich import box
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.padding import Padding

from .markdown_utils import MarkDownUtils
from .rule import Rule
from .rule_content_type import RuleContentType
from .rule_grouper import RuleGrouper
from .rule_render_type import RuleRenderType


class RuleRenderer:  # pylint: disable=R0903
    """Shows STE100 rules on the console."""

    def show(
        self,
        console: Console,
        rules: list[Rule],
        type_: RuleRenderType = RuleRenderType.DEFAULT,
    ) -> None:
        """Shows rules on the console."""

        assert isinstance(console, Console)
        assert isinstance(rules, list)

        if RuleRenderType.LIST == type_:
            self._show_list(console, rules)
            return

        for rule in rules:
            self._show_rule_header(console, rule)
            if RuleRenderType.BRIEF != type_:
                self._show_contents(console, rule)

    def _show_list(self, console: Console, rules: list[Rule]) -> None:
        current_section = ""
        current_category = ""
        grouped = RuleGrouper(rules).invoke()
        for section, categories in grouped.items():
            if current_section != section:
                current_section = section
                console.print(Markdown(f"**{current_section}**"))
            for category, rules_cat in categories.items():
                if current_category != category:
                    current_category = category
                    console.print(
                        Padding(Markdown(f"*{current_category}*"), (0, 0, 0, 2))
                    )
                for rule in rules_cat:
                    console.print(
                        Padding(Markdown(f"**{rule.id_}**: {rule.name}"), (0, 0, 0, 4))
                    )

    def _show_rule_header(self, console: Console, rule: Rule) -> None:
        p = Panel(
            Markdown(rule.name),
            title=f"{rule.type_.capitalize()} {rule.id_}",
            title_align="left",
            subtitle=f"{rule.section}, {rule.category}, {rule.ref}",
            subtitle_align="left",
            border_style="bright_yellow",
            padding=(1, 1),
            box=box.HEAVY_EDGE,
        )
        console.print(p)
        console.print("")
        console.print(Markdown(f"**{rule.summary}**"))
        console.print("")

    def _show_contents(self, console: Console, rule: Rule) -> None:
        for content in rule.contents:
            self._show_content(console, content)

    def _show_content(self, console: Console, content) -> None:
        match content.type_:
            case RuleContentType.TEXT:
                console.print(Markdown(content.data))
            case RuleContentType.EXAMPLE:
                console.print(
                    Panel(
                        f"[green]{content.data}[/green]",
                        title="STE",
                        title_align="left",
                        expand=False,
                    )
                )
            case RuleContentType.STE:
                console.print(
                    MarkDownUtils.to_panel(content.data, title="STE", style="green")
                )
            case RuleContentType.NONSTE:
                console.print(
                    MarkDownUtils.to_panel(content.data, title="Non-STE", style="red")
                )
            case RuleContentType.NOT_RECOMMENDED:
                console.print(
                    MarkDownUtils.to_panel(
                        content.data, title="Not recommended", style="red"
                    )
                )
            case RuleContentType.NOTE:
                console.print(
                    Panel(
                        Markdown(content.data),
                        title="💡",
                        title_align="left",
                        border_style="yellow",
                        expand=False,
                    )
                )
            case RuleContentType.GOOD:
                console.print(
                    MarkDownUtils.to_panel(content.data, title="Example", style="green")
                )
            case RuleContentType.GENERAL:
                console.print(
                    MarkDownUtils.to_panel(content.data, title="Example", style="blue")
                )
            case RuleContentType.COMMENT:
                console.print(Markdown(f"_{content.data}_"))
            case _:
                console.print("default")
                console.print(Markdown(content.data))
        console.print("")
