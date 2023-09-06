# pylint: disable=redefined-outer-name
"""Negative cohabitation plants should be in a different compositions"""

from uuid import uuid4

import pytest

from derevo import Plant, Territory
from derevo import enumerations as d_enum
from derevo import get_compositions


def get_plant_for_humidity_type(humidity_type: d_enum.HumidityType, tolerance_type: d_enum.ToleranceType) -> Plant:
    """Plants with all combitations of light types."""
    idx = uuid4()
    return Plant(
        name_ru=f"plant_{idx}",
        name_latin=f"plant_{idx}",
        genus="genus",
        life_form="life_form",
        limitation_factors_resistances={},
        humidity_preferences={humidity_type: tolerance_type},
        soil_acidity_preferences={d_enum.AcidityType.NEUTRAL: d_enum.ToleranceType.POSITIVE},
        soil_fertility_preferences={d_enum.FertilityType.FERTIL: d_enum.ToleranceType.POSITIVE},
        soil_type_preferences={d_enum.SoilType.HEAVY: d_enum.ToleranceType.POSITIVE},
        light_preferences={d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE},
        usda_zone_preferences={d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE},
    )


@pytest.fixture
def territory_info() -> Territory:
    """Default territory for the test"""
    return Territory(
        limitation_factors=[],
        humidity_types=[],
        soil_acidity_types=[d_enum.AcidityType.NEUTRAL],
        soil_fertility_types=[d_enum.FertilityType.FERTIL],
        soil_types=[d_enum.SoilType.HEAVY],
        light_types=[d_enum.LightType.LIGHT],
        usda_zone=d_enum.UsdaZone.USDA5,
    )


@pytest.mark.xfail(reason="Fixing")
def test_no_plants_unacceptable_humidity_type(territory_info: Territory):
    """Test that no plant type without positive tolerance to the given light type is used in composition."""

    plants = {
        value: get_plant_for_humidity_type(value, d_enum.ToleranceType.POSITIVE) for value in list(d_enum.HumidityType)
    }
    plants_list = list(plants.values())

    print("Plants:", ", ".join(f"{p.name_ru}: {next(iter(p.light_preferences.keys()))}" for p in plants_list))
    for humidity_type in list(d_enum.HumidityType):
        territory_info.humidity_types = [humidity_type]
        print("Territory humidity type:", territory_info.humidity_types)
        compositions = get_compositions(
            plants_available=plants_list,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1, "There should be only one composition"
        assert compositions[0][0] == plants[humidity_type]


@pytest.mark.xfail(reason="Fixing")
def test_no_plants_unacceptable_humidity_type_neutral(territory_info: Territory):
    """Test that no plant type without positive tolerance to the given light type is used in composition."""

    plants = {
        value: get_plant_for_humidity_type(value, d_enum.ToleranceType.NEUTRAL) for value in list(d_enum.HumidityType)
    }
    plants_list = list(plants.values())

    print("Plants:", ", ".join(f"{p.name_ru}: {next(iter(p.light_preferences.keys()))}" for p in plants_list))
    for humidity_type in list(d_enum.HumidityType):
        territory_info.humidity_types = [humidity_type]
        print("Territory humidity types:", territory_info.humidity_types)
        compositions = get_compositions(
            plants_available=plants_list,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1, "There should be only one composition"
        assert compositions[0][0] == plants[humidity_type]


@pytest.mark.xfail(reason="Fixing")
def test_no_plants_denying_humidity_type(territory_info: Territory):
    """Test every combination of light types to block out plants."""

    plants_positive = {
        value: get_plant_for_humidity_type(value, d_enum.ToleranceType.POSITIVE) for value in list(d_enum.HumidityType)
    }
    plants_negative = {
        value: get_plant_for_humidity_type(value, d_enum.ToleranceType.NEGATIVE) for value in list(d_enum.HumidityType)
    }
    plants_list = list(plants_positive.values()) + list(plants_negative.values())

    print("Plants:", ", ".join(f"{p.name_ru}: {next(iter(p.light_preferences.keys()))}" for p in plants_list))
    for humidity_type in list(d_enum.HumidityType):
        territory_info.humidity_types = [humidity_type]
        print("Territory humidity type:", territory_info.humidity_types)
        compositions = get_compositions(
            plants_available=plants_list,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert len(compositions) == 1, "There should be only one composition"
        assert plants_negative[humidity_type] not in compositions[0]
