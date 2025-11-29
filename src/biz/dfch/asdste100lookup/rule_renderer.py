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

from .markdown_utils import MarkDownUtils
from .rule import Rule
from .rule_content_type import RuleContentType


class RuleRenderer:  # pylint: disable=R0903
    """Shows STE100 rules on the console."""

    def show(
        self, console: Console, rules: list[Rule], is_summary_only: bool = False
    ) -> None:
        """Shows rules on the console."""

        assert isinstance(console, Console)
        assert isinstance(rules, list)

        for rule in rules:

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
            md = Markdown(f"**{rule.summary}**")
            console.print("")
            console.print(md)
            console.print("")

            if is_summary_only:
                continue

            for content in rule.contents:
                match content.type_:
                    case RuleContentType.TEXT:
                        md = Markdown(content.data)
                        console.print(md)
                        console.print("")
                    case RuleContentType.EXAMPLE:
                        txt = f"[green]{content.data}[/green]"
                        console.print(
                            Panel(txt,
                                  title="STE",
                                  title_align="left",
                                  expand=False)
                        )
                        console.print("")
                    case RuleContentType.STE:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="STE", style="green"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.NONSTE:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Non-STE", style="red"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.NOT_RECOMMENDED:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Not recommended", style="red"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.NOTE:
                        md = Markdown(content.data)
                        console.print(
                            Panel(
                                md,
                                title="💡",
                                title_align="left",
                                border_style="yellow",
                                expand=False,
                            )
                        )
                        console.print("")
                    case RuleContentType.GOOD:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Example", style="green"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.GENERAL:
                        panel = MarkDownUtils.to_panel(
                            content.data, title="Example", style="blue"
                        )
                        console.print(panel)
                        console.print("")
                    case RuleContentType.COMMENT:
                        md = Markdown(f"_{content.data}_")
                        console.print(md)
                        console.print("")
                    case _:
                        console.print("default")
                        md = Markdown(content.data)
                        console.print(md)
                        console.print("")
