# pylint: disable=redefined-outer-name
"""Negative cohabitation plants should be in a different compositions"""

import pytest

from derevo import Plant, Territory
from derevo import enumerations as d_enum
from derevo import get_compositions


@pytest.fixture
def plants_with_all_negative_usda_zones() -> list[Plant]:
    """Plants with all combitations of limitation factors."""
    plants: list[Plant] = []
    for i, usda_zone in enumerate(d_enum.UsdaZone):
        plants.append(
            Plant(
                name_ru=f"plant_{i}",
                name_latin=f"plant_{i}",
                genus="genus",
                life_form="life_form",
                limitation_factors_resistances={},
                humidity_preferences={d_enum.HumidityType.NORMAL: d_enum.ToleranceType.POSITIVE},
                soil_acidity_preferences={d_enum.AcidityType.NEUTRAL: d_enum.ToleranceType.POSITIVE},
                soil_fertility_preferences={d_enum.FertilityType.FERTIL: d_enum.ToleranceType.POSITIVE},
                soil_type_preferences={d_enum.SoilType.HEAVY: d_enum.ToleranceType.POSITIVE},
                light_preferences={d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE},
                usda_zone_preferences={usda_zone: d_enum.ToleranceType.NEGATIVE},
            )
        )
    return plants


@pytest.fixture
def territory_info() -> Territory:
    """Default territory for the test"""
    return Territory(
        limitation_factors=[],
        humidity_types=[d_enum.HumidityType.NORMAL],
        soil_acidity_types=[d_enum.AcidityType.NEUTRAL],
        soil_fertility_types=[d_enum.FertilityType.FERTIL],
        soil_types=[d_enum.SoilType.HEAVY],
        light_types=[d_enum.LightType.LIGHT],
        usda_zone=d_enum.UsdaZone.USDA5,
    )


def test_error_no_plants(plants_with_all_negative_usda_zones: list[Plant], territory_info: Territory):
    """USDA zones blocks one plant from being included in composition for each zone."""

    for usda_zone in iter(d_enum.UsdaZone):
        territory_info.usda_zone = usda_zone
        compositions = get_compositions(
            plants_available=plants_with_all_negative_usda_zones,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1 and len(compositions[0]) == len(list(d_enum.UsdaZone)) - 1


def test_no_plants_unacceptable_usda_zones(plants_with_all_negative_usda_zones: list[Plant], territory_info: Territory):
    """Test combinations of USDA zones to block out plants."""

    for usda_zone in list(d_enum.UsdaZone):
        territory_info.usda_zone = usda_zone
        compositions = get_compositions(
            plants_available=plants_with_all_negative_usda_zones,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert (
            len(compositions) == 1 or len(territory_info.limitation_factors) == 6
        ), "There should be only one composition"
        if len(compositions) != 0:
            for plant in compositions[0]:
                try:
                    assert (
                        not plant.usda_zone_preferences.get(usda_zone, d_enum.ToleranceType.NEUTRAL)
                        == d_enum.ToleranceType.NEGATIVE
                    ), "No plants with negative tolerance to the esda zone should be in result"
                except AssertionError:
                    print(", ".join(str(plant.usda_zone_preferences) for plant in compositions[0]))
                    raise
