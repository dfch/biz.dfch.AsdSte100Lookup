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

"""TechnicalWordCategory enum."""

# pylint: disable=line-too-long

from __future__ import annotations
from enum import StrEnum
import re

from biz.dfch.logging import log


class TechnicalWordCategory(StrEnum):
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
    def get_descriptions() -> dict[TechnicalWordCategory, str]:
        """Returns a map of all word category descriptions."""

        result: dict[TechnicalWordCategory, str] = {
            TechnicalWordCategory.DEFAULT: "Not a technical noun or verb",

            TechnicalWordCategory.OFFICIAL_PARTS: "Official parts information",
            TechnicalWordCategory.VEHICLES_MACHINES: "Vehicles and machines, and locations on them",  # noqa: disable:E0501
            TechnicalWordCategory.TOOLS_EQUIPMENT: "Tools and support equipment, their parts, and locations on them",  # noqa: disable:E0501
            TechnicalWordCategory.MATERIALS: "Materials, consumables, and unwanted material",  # noqa: disable:E0501
            TechnicalWordCategory.FACILITIES_INFRASTRUCTURE: "Facilities, infrastructure, and logistic procedures",  # noqa: disable:E0501
            TechnicalWordCategory.SYSTEMS_COMPONENTS: "Systems, components and circuits, their functions, configurations, and parts",  # noqa: disable:E0501
            TechnicalWordCategory.MATHEMATICAL_SCIENCE: "Mathematical, scientific, engineering terms, and formulas",  # noqa: disable:E0501
            TechnicalWordCategory.NAVIGATION: "Navigation and geographic terms",
            TechnicalWordCategory.NUMBERS_UNITS: "Numbers, units of measurement and time (and their symbols)",  # noqa: disable:E0501
            TechnicalWordCategory.QUOTED_TEXT: "Quoted text",
            TechnicalWordCategory.ROLES_GROUPS: "Professional roles, individuals, groups, organizations, and geopolitical entities",  # noqa: disable:E0501
            TechnicalWordCategory.BODY_TERMS: "Parts of the body",
            TechnicalWordCategory.EFFECTS_FOOD_BEVERAGE: "Common personal effects, food, and beverages",  # noqa: disable:E0501
            TechnicalWordCategory.MEDICAL_TERMS: "Medical terms",
            TechnicalWordCategory.DOCUMENTATION: "Official documents, parts of documentation, standards, and guidelines",  # noqa: disable:E0501
            TechnicalWordCategory.ENVIRONMENTAL_TERMS: "Environmental and operational conditions",  # noqa: disable:E0501
            TechnicalWordCategory.COLOURS: "Colors",
            TechnicalWordCategory.DAMAGE_TERMS: "Damage terms",
            TechnicalWordCategory.ICT_TERMS: "Computer science, information and communication technology",  # noqa: disable:E0501
            TechnicalWordCategory.CIVIL_MILITARY_TERMS: "Civil and military operations",  # noqa: disable:E0501
            TechnicalWordCategory.LAW_REGULATIONS: "Law and regulations",
            TechnicalWordCategory.ANIMALS_PLANTS: "Animals, plants, and other life forms",  # noqa: disable:E0501

            TechnicalWordCategory.TV_MANUFACTURING_PROCESSES: "Manufacturing processes",  # noqa: disable=E0501
            TechnicalWordCategory.TV_COMPUTER_PROCESSES: "Computer processes and applications",  # noqa: disable=E0501
            TechnicalWordCategory.TV_INSTRUCTIONS_INFORMATION: "Instructions and information for applicable subject fields",  # noqa: disable=E0501
            TechnicalWordCategory.TV_LAW_REGULATIONS: "Law and regulations",
        }

        return result

    @staticmethod
    def get_matching_keys(pattern: str) -> list[TechnicalWordCategory]:
        """pass"""

        assert isinstance(pattern, str) and "" != pattern.strip()

        try:
            regex = re.compile(pattern, re.IGNORECASE)
        except re.error as ex:
            log.error("Invalid regex: '%s'", ex)

            return []

        result = [key for key, value in
                  TechnicalWordCategory.get_descriptions().items()
                  if regex.search(value)]

        return result

    def get_description(self) -> str:
        """Returns the descriptive text of the category."""

        descriptions = TechnicalWordCategory.get_descriptions()

        return descriptions[self]
