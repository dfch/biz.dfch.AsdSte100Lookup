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

"""WordCategory enum."""

# pylint: disable=line-too-long

from __future__ import annotations
from enum import StrEnum
import re

from biz.dfch.logging import log


class WordCategory(StrEnum):
    """Represents ASD-STE100 technical word categories."""

    DEFAULT = "0"
    OFFICIAL_PARTS = "TN1"
    VEHICLES_MACHINES = "TN2"
    TOOLS_EQUIPMENT = "TN3"
    MATERIALS = "TN4"
    FACILITIES_INFRASTRUCTURE = "TN5"
    SYSTEMS_COMPONENTS = "TN6"
    MATHEMATICAL_SCIENCE = "TN7"
    NAVIGATION = "TN8"
    NUMBERS_UNITS = "TN9"
    QUOTED_TEXT = "TN10"
    ROLES_GROUPS = "TN11"
    BODY_TERMS = "TN12"
    EFFECTS_FOOD_BEVERAGE = "TN13"
    MEDICAL_TERMS = "TN14"
    DOCUMENTATION = "TN15"
    ENVIRONMENTAL_TERMS = "TN16"
    COLOURS = "TN17"
    DAMAGE_TERMS = "TN18"
    ICT_TERMS = "TN19"
    CIVIL_MILITARY_TERMS = "TN20"
    LAW_REGULATIONS = "TN21"
    ANIMALS_PLANTS = "TN22"

    TV_MANUFACTURING_PROCESSES = "TV1"
    TV_COMPUTER_PROCESSES = "TV2"
    TV_INSTRUCTIONS_INFORMATION = "TV3"
    TV_LAW_REGULATIONS = "TV4"

    @staticmethod
    def get_descriptions() -> dict[WordCategory, str]:
        """Returns a map of all word category descriptions."""

        result: dict[WordCategory, str] = {
            WordCategory.DEFAULT: "Not a technical noun or verb",
            WordCategory.OFFICIAL_PARTS: "Official parts information",
            WordCategory.VEHICLES_MACHINES: "Vehicles and machines, and locations on them",  # noqa: disable:E0501
            WordCategory.TOOLS_EQUIPMENT: "Tools and support equipment, their parts, and locations on them",  # noqa: disable:E0501
            WordCategory.MATERIALS: "Materials, consumables, and unwanted material",  # noqa: disable:E0501
            WordCategory.FACILITIES_INFRASTRUCTURE: "Facilities, infrastructure, and logistic procedures",  # noqa: disable:E0501
            WordCategory.SYSTEMS_COMPONENTS: "Systems, components and circuits, their functions, configurations, and parts",  # noqa: disable:E0501
            WordCategory.MATHEMATICAL_SCIENCE: "Mathematical, scientific, engineering terms, and formulas",  # noqa: disable:E0501
            WordCategory.NAVIGATION: "Navigation and geographic terms",
            WordCategory.NUMBERS_UNITS: "Numbers, units of measurement and time (and their symbols)",  # noqa: disable:E0501
            WordCategory.QUOTED_TEXT: "Quoted text",
            WordCategory.ROLES_GROUPS: "Professional roles, individuals, groups, organizations, and geopolitical entities",  # noqa: disable:E0501
            WordCategory.BODY_TERMS: "Parts of the body",
            WordCategory.EFFECTS_FOOD_BEVERAGE: "Common personal effects, food, and beverages",  # noqa: disable:E0501
            WordCategory.MEDICAL_TERMS: "Medical terms",
            WordCategory.DOCUMENTATION: "Official documents, parts of documentation, standards, and guidelines",  # noqa: disable:E0501
            WordCategory.ENVIRONMENTAL_TERMS: "Environmental and operational conditions",  # noqa: disable:E0501
            WordCategory.COLOURS: "Colors",
            WordCategory.DAMAGE_TERMS: "Damage terms",
            WordCategory.ICT_TERMS: "Computer science, information and communication technology",  # noqa: disable:E0501
            WordCategory.CIVIL_MILITARY_TERMS: "Civil and military operations",  # noqa: disable:E0501
            WordCategory.LAW_REGULATIONS: "Law and regulations",
            WordCategory.ANIMALS_PLANTS: "Animals, plants, and other life forms",  # noqa: disable:E0501
            WordCategory.TV_MANUFACTURING_PROCESSES: "Manufacturing processes",  # noqa: disable=E0501
            WordCategory.TV_COMPUTER_PROCESSES: "Computer processes and applications",  # noqa: disable=E0501
            WordCategory.TV_INSTRUCTIONS_INFORMATION: "Instructions and information for applicable subject fields",  # noqa: disable=E0501
            WordCategory.TV_LAW_REGULATIONS: "Law and regulations",
        }

        return result

    @staticmethod
    def get_matching_keys(pattern: str) -> list[WordCategory]:
        """
        Returns all word categories where `pattern` matchs the text from
        the description.
        """

        assert isinstance(pattern, str) and "" != pattern.strip()

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as ex:
            log.error("Invalid regex: '%s'", ex)

            return []

        result = [
            key
            for key, value in WordCategory.get_descriptions().items()
            if regex.search(value)
        ]

        return result

    def get_description(self) -> str:
        """Returns the descriptive text of the category."""

        descriptions = WordCategory.get_descriptions()

        return descriptions[self]
