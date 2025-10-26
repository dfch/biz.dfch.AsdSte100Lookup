# from rich.console import Console
# from rich.table import Table


# class Colorizer:
#     """
#     Returns a coloured substring.
#     """

#     def __init__(self, base: str):
#         self.base = base
#         self.console = Console()

#     def _replace_with_color(self, value: str, color: str, bright: bool) -> str:
#         color_name = f"bright_{color}" if bright else color
#         colored_value = f"[{color_name}]{value}[/{color_name}]"
#         return self.base.replace(value, colored_value)

#     def to_black(self, value: str, bright: bool = False) -> str:
#         """Returns a black substring."""
#         return self._replace_with_color(value, "black", bright)

#     def to_red(self, value: str, bright: bool = False) -> str:
#         """Returns a red substring."""
#         return self._replace_with_color(value, "red", bright)

#     def to_green(self, value: str, bright: bool = False) -> str:
#         """Returns a green substring."""
#         return self._replace_with_color(value, "green", bright)

#     def to_yellow(self, value: str, bright: bool = False) -> str:
#         """Returns a yellow substring."""
#         return self._replace_with_color(value, "yellow", bright)

#     def to_blue(self, value: str, bright: bool = False) -> str:
#         """Returns a blue substring."""
#         return self._replace_with_color(value, "blue", bright)

#     def to_magenta(self, value: str, bright: bool = False) -> str:
#         """Returns a magenta substring."""
#         return self._replace_with_color(value, "magenta", bright)

#     def to_cyan(self, value: str, bright: bool = False) -> str:
#         """Returns a cyan substring."""
#         return self._replace_with_color(value, "cyan", bright)

#     def to_white(self, value: str, bright: bool = False) -> str:
#         """Returns a white substring."""
#         return self._replace_with_color(value, "white", bright)

# # Sample data — normally you'd load these from your JSON or dataclass instances
# words = [
#     {
#         "name": "WRITE",
#         "type_": "v",
#         "description": "To record data or information as words, letters, or symbols",
#         "ste": "WRITE THE TEST DATE ON THE CERTIFICATE.",
#         "nonste": ""
#     },
#     {
#         "name": "wrap",
#         "type_": "v",
#         "description": "",
#         "ste": "PUT THE PART IN OILPAPER.",
#         "nonste": "Wrap the part in oilpaper."
#     },
#     {
#         "name": "WIND",
#         "type_": "v",
#         "description": "To move around and around an object",
#         "ste": "WIND THE TAPE ON THE REEL.",
#         "nonste": ""
#     },
#     {
#         "name": "PUT",
#         "type_": "v",
#         "description": "To cause something to move or to be in a specified position or condition",
#         "ste": "PUT THE ADAPTER IN POSITION AGAINST ITS SUPPORT.",
#         "nonste": ""
#     }
# ]

# console = Console()

# # Create the table
# table = Table(title="Results")

# table.add_column("Word", no_wrap=True)
# table.add_column("Type", no_wrap=True)
# table.add_column("Description")
# table.add_column("STE Example")
# table.add_column("Non-STE Example")

# # Add rows to the table
# for word in words:
#     table.add_row(
#         Colorizer(word["name"]).to_green("WRITE", True),
#         # word["name"],
#         word["type_"],
#         word["description"] or " ",
#         word["ste"] or " ",
#         # word["nonste"] or " "
#         Colorizer(word["nonste"]).to_red("Wrap"),
#     )
#     table.add_row(" ", " ", " ", " ", " ")

# # Print the table
# console.print(table)
