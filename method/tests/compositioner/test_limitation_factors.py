# pylint: disable=redefined-outer-name
"""Negative cohabitation plants should be in a different compositions"""

from itertools import chain

import pytest

from derevo import Plant, Territory
from derevo import enumerations as d_enum
from derevo import get_compositions


@pytest.fixture
def binary_combinations6() -> list[list[bool]]:
    """Return list of lists of 6 boolean values covering all the available combinations."""
    options = list(chain.from_iterable([[[False] + val, [True] + val] for val in [[False], [True]]]))
    options = list(chain.from_iterable([[[False] + val, [True] + val] for val in options]))
    options = list(chain.from_iterable([[[False] + val, [True] + val] for val in options]))
    options = list(chain.from_iterable([[[False] + val, [True] + val] for val in options]))
    options = list(chain.from_iterable([[[False] + val, [True] + val] for val in options]))
    return options


@pytest.fixture
def plants_with_all_limitation_factors(binary_combinations6: list[list[bool]]) -> list[Plant]:
    """Plants with all combitations of limitation factors."""
    plants: list[Plant] = []
    for i, positives in enumerate(binary_combinations6):
        plants.append(
            Plant(
                name_ru=f"plant_{i}",
                name_latin=f"plant_{i}",
                genus="genus",
                life_form="life_form",
                limitation_factors_resistances={
                    factor: d_enum.ToleranceType.POSITIVE if positives[j] else d_enum.ToleranceType.NEGATIVE
                    for j, factor in enumerate(d_enum.LimitationFactor)
                },
                humidity_preferences={d_enum.HumidityType.NORMAL: d_enum.ToleranceType.POSITIVE},
                soil_acidity_preferences={d_enum.AcidityType.NEUTRAL: d_enum.ToleranceType.POSITIVE},
                soil_fertility_preferences={d_enum.FertilityType.FERTIL: d_enum.ToleranceType.POSITIVE},
                soil_type_preferences={d_enum.SoilType.HEAVY: d_enum.ToleranceType.POSITIVE},
                light_preferences={d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE},
                usda_zone_preferences={d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE},
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


def test_error_no_plants(plants_with_all_limitation_factors: list[Plant], territory_info: Territory):
    """Limitation factors blocks each plant from being planted, so no compositions are available."""

    territory_info.limitation_factors = list(d_enum.LimitationFactor)
    compositions = get_compositions(
        plants_available=plants_with_all_limitation_factors[:-1],
        cohabitation_attributes=[],
        territory=territory_info,
    )
    assert len(compositions) == 0


@pytest.mark.xfail(reason="Fixing")
def test_no_plants_unacceptable_limitation_factors(
    plants_with_all_limitation_factors: list[Plant], territory_info: Territory, binary_combinations6: list[list[bool]]
):
    """Test every combination of limitation factors to block out plants."""

    for positives in binary_combinations6:
        print(f"Positives = {positives}")
        if not any(p for p in positives):
            continue
        territory_info.limitation_factors = [
            limitation_factor
            for is_positive, limitation_factor in zip(positives, list(d_enum.LimitationFactor))
            if is_positive
        ]
        compositions = get_compositions(
            plants_available=plants_with_all_limitation_factors,
            cohabitation_attributes=[],
            territory=territory_info,
        )
        assert (
            len(compositions) == 1 or len(territory_info.limitation_factors) == 6
        ), "There should be only one composition"
        if len(compositions) != 0:
            for plant in compositions[0]:
                try:
                    assert not any(
                        plant.limitation_factors_resistances[lf] == d_enum.ToleranceType.NEGATIVE
                        for lf in territory_info.limitation_factors
                    ), "No plants with negative tolerance to the territory limitation factors should be in result"
                except AssertionError:
                    print(", ".join(str(plant.limitation_factors_resistances) for plant in compositions[0]))
                    raise
