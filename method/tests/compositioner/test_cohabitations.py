# pylint: disable=redefined-outer-name
"""Negative cohabitation plants should be in a different compositions"""

import pytest

from derevo import Plant, Territory
from derevo import enumerations as d_enum
from derevo import get_compositions
from derevo.models.cohabitation import CohabitationType, GeneraCohabitation


@pytest.fixture
def oaks() -> list[Plant]:
    """List of 6 oak trees."""
    return [
        Plant(
            name_ru=name_ru,
            name_latin=name_latin,
            genus="Дуб",
            life_form="Дерево",
            humidity_preferences={
                d_enum.HumidityType.NORMAL: d_enum.ToleranceType.POSITIVE,
            },
            light_preferences={
                d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE,
            },
            usda_zone_preferences={
                d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE,
            },
        )
        for name_ru, name_latin in (
            ("Дуб болотный", "Quercus palustris Münchh."),
            ("Дуб зубчатый", "Quercus dentata Thunb."),
            ("Дуб изменчивый", "Quercus variabilis Blume"),
            ("Дуб красный", "Quercus rubra"),
            ("Дуб монгольский", "Quercus mongolica Fisch. ex Ledeb."),
            ("Дуб черешчатый", "Quercus robur L."),
        )
    ]


@pytest.fixture
def apple_trees() -> list[Plant]:
    """List of one apple tree."""
    return [
        Plant(
            name_ru="Яблоня домашняя",
            name_latin="Malus domestica (Suckow) Borkh.",
            genus="Яблоня",
            life_form="Дерево",
            humidity_preferences={
                d_enum.HumidityType.NORMAL: d_enum.ToleranceType.POSITIVE,
            },
            light_preferences={
                d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE,
            },
            usda_zone_preferences={
                d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE,
            },
        )
    ]


@pytest.fixture
def kalinas() -> list[Plant]:
    """List of one 3 kalina trees."""
    return [
        Plant(
            name_ru=name_ru,
            name_latin=name_latin,
            genus="Калина",
            life_form="Дерево",
            light_preferences={
                d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE,
            },
            usda_zone_preferences={
                d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE,
            },
        )
        for name_ru, name_latin in (
            ("Калина съедобная", "Viburnum edule (Michx.) Raf."),
            ("Калина буль-де-неж", "Viburnum opulus f. roseum (L.) Hegi"),
            ("Калина гордовина", "Viburnum lantana L."),
        )
    ]


@pytest.fixture
def cohabitation_attributes() -> list[GeneraCohabitation]:
    """Cohabitation attributes for oak, apple tree and kalina"""
    return [
        GeneraCohabitation("Дуб", "Калина", CohabitationType.NEGATIVE),
        GeneraCohabitation("Яблоня", "Дуб", CohabitationType.POSITIVE),
        GeneraCohabitation("Яблоня", "Калина", CohabitationType.NEGATIVE),
    ]


@pytest.fixture
def cohabitation_attributes_all_positive() -> list[GeneraCohabitation]:
    """Cohabitation attributes for oak, apple tree and kalina"""
    return [
        GeneraCohabitation("Дуб", "Калина", CohabitationType.POSITIVE),
        GeneraCohabitation("Яблоня", "Дуб", CohabitationType.POSITIVE),
        GeneraCohabitation("Яблоня", "Калина", CohabitationType.POSITIVE),
    ]


@pytest.fixture
def territory_info() -> Territory:
    """Default territory for the test"""
    return Territory(
        usda_zone=d_enum.UsdaZone.USDA5,
        limitation_factors=[],
        humidity_types=[d_enum.HumidityType.NORMAL],
        light_types=[d_enum.LightType.LIGHT],
        soil_acidity_types=[d_enum.AcidityType.NEUTRAL],
        soil_fertility_types=[d_enum.FertilityType.FERTIL],
        soil_types=[d_enum.SoilType.ROCKY],
    )


def test_oak_kalina(
    oaks: list[Plant],
    kalinas: list[Plant],
    cohabitation_attributes: list[GeneraCohabitation],
    territory_info: Territory,
):
    """Дуб vs Калина"""
    plants_list: list[Plant] = oaks + kalinas

    compositions = get_compositions(
        plants_available=plants_list,
        cohabitation_attributes=cohabitation_attributes,
        territory=territory_info,
    )

    assert len(compositions) > 1, "There must be 2 compositions"
    assert all(
        (all(plant.genus == "Дуб" for plant in plants) or all(plant.genus == "Калина" for plant in plants))
        for plants in compositions
    )


def test_oak_apple_tree_kalina(
    oaks: list[Plant],
    kalinas: list[Plant],
    apple_trees: list[Plant],
    cohabitation_attributes: list[GeneraCohabitation],
    territory_info: Territory,
):
    """Дуб + Яблоня vs Калина"""
    plants_list: list[Plant] = oaks + apple_trees + kalinas

    compositions = get_compositions(
        plants_available=plants_list,
        cohabitation_attributes=cohabitation_attributes,
        territory=territory_info,
    )

    assert len(compositions) > 1, "There must be 2 compositions"
    for i, plants in enumerate(compositions):
        print(f"Composition #{i}:", ", ".join(plant.genus for plant in plants))
    assert all(
        (all(plant.genus in ("Дуб", "Яблоня") for plant in plants) or all(plant.genus == "Калина" for plant in plants))
        for plants in compositions
    )


def test_unset_cohabitation(
    oaks: list[Plant],
    kalinas: list[Plant],
    apple_trees: list[Plant],
    territory_info: Territory,
):
    """Дуб + Яблоня + Калина without cohabitation attributes."""
    plants_list: list[Plant] = oaks + apple_trees + kalinas

    compositions = get_compositions(
        plants_available=plants_list,
        cohabitation_attributes=[],
        territory=territory_info,
    )

    for i, plants in enumerate(compositions):
        print(f"Composition #{i}:", ", ".join(plant.genus for plant in plants))
    assert len(compositions) == 1, "There must be one composition"
    assert len(compositions[0]) == len(plants_list)


def test_positive_cohabitation(
    kalinas: list[Plant],
    apple_trees: list[Plant],
    cohabitation_attributes_all_positive: list[GeneraCohabitation],
    territory_info: Territory,
):
    """Дуб + Яблоня + Калина without cohabitation attributes."""
    plants_list: list[Plant] = apple_trees + kalinas

    compositions = get_compositions(
        plants_available=plants_list,
        cohabitation_attributes=cohabitation_attributes_all_positive,
        territory=territory_info,
    )

    for i, plants in enumerate(compositions):
        print(f"Composition #{i}:", ", ".join(plant.genus for plant in plants))
    assert len(compositions) == 1, "There must be one composition"
    assert len(compositions[0]) == len(plants_list)
