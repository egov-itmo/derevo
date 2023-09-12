# pylint: disable=redefined-outer-name
"""Negative cohabitation plants should be in a different compositions"""

from uuid import uuid4

import pytest

from derevo import Plant, Territory
from derevo import enumerations as d_enum
from derevo import get_compositions


def get_plant_for_light_type(light_type: d_enum.LightType, tolerance_type: d_enum.ToleranceType) -> Plant:
    """Plants with all combitations of light types."""
    idx = uuid4()
    return Plant(
        name_ru=f"plant_{idx}",
        name_latin=f"plant_{idx}",
        genus="genus",
        life_form="life_form",
        limitation_factors_resistances={},
        humidity_preferences={d_enum.HumidityType.NORMAL: d_enum.ToleranceType.POSITIVE},
        soil_acidity_preferences={d_enum.AcidityType.NEUTRAL: d_enum.ToleranceType.POSITIVE},
        soil_fertility_preferences={d_enum.FertilityType.FERTIL: d_enum.ToleranceType.POSITIVE},
        soil_type_preferences={d_enum.SoilType.HEAVY: d_enum.ToleranceType.POSITIVE},
        light_preferences={light_type: tolerance_type},
        usda_zone_preferences={d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE},
    )


@pytest.fixture
def territory_info() -> Territory:
    """Default territory for the test"""
    return Territory(
        limitation_factors=[],
        humidity_types=[d_enum.HumidityType.NORMAL],
        soil_acidity_types=[d_enum.AcidityType.NEUTRAL],
        soil_fertility_types=[d_enum.FertilityType.FERTIL],
        soil_types=[d_enum.SoilType.HEAVY],
        light_types=[],
        usda_zone=d_enum.UsdaZone.USDA5,
    )


def test_no_plants_unacceptable_light_type(territory_info: Territory):
    """Test that no plant type with negative tolerance to the given light type is used in composition."""

    plants = {value: get_plant_for_light_type(value, d_enum.ToleranceType.NEGATIVE) for value in list(d_enum.LightType)}
    plants_list = list(plants.values())

    print("Plants:", ", ".join(f"{p.name_ru}: {next(iter(p.light_preferences.keys()))}" for p in plants_list))
    for light_type in list(d_enum.LightType):
        territory_info.light_types = [light_type]
        print("Territory light type:", territory_info.light_types)
        compositions = get_compositions(
            plants_available=plants_list,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1, "There should be only one composition"
        assert plants[light_type] not in compositions[0]


def test_no_plants_unacceptable_light_type_neutral(territory_info: Territory):
    """Test that all neutral light types tolerance to the given light type is used in composition."""

    plants = {value: get_plant_for_light_type(value, d_enum.ToleranceType.NEUTRAL) for value in list(d_enum.LightType)}
    plants_list = list(plants.values())

    print("Plants:", ", ".join(f"{p.name_ru}: {next(iter(p.light_preferences.keys()))}" for p in plants_list))
    for light_type in list(d_enum.LightType):
        territory_info.light_types = [light_type]
        print("Territory light type:", territory_info.light_types)
        compositions = get_compositions(
            plants_available=plants_list,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1, "There should be only one composition"
        assert len(compositions[0]) == len(plants), "All plants with neutral tolerance should be used"


def test_no_plants_denying_light_type(territory_info: Territory):
    """Test every combination of light types to block out plants."""

    plants_positive = {
        value: get_plant_for_light_type(value, d_enum.ToleranceType.POSITIVE) for value in list(d_enum.LightType)
    }
    plants_negative = {
        value: get_plant_for_light_type(value, d_enum.ToleranceType.NEGATIVE) for value in list(d_enum.LightType)
    }
    plants_list = list(plants_positive.values()) + list(plants_negative.values())

    print("Plants:", ", ".join(f"{p.name_ru}: {next(iter(p.light_preferences.keys()))}" for p in plants_list))
    for light_type in list(d_enum.LightType):
        territory_info.light_types = [light_type]
        print("Territory light type:", territory_info.light_types)
        compositions = get_compositions(
            plants_available=plants_list,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1, "There should be only one composition"
        assert plants_negative[light_type] not in compositions[0]
