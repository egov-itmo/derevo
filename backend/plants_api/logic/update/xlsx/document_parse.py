"""
Functions which are used in document parsing are defined here.
"""
from datetime import date
from typing import Callable

import pandas as pd

from plants_api.schemas.update.sheets_configuration import (
    GeneraCohabitationConfiguration,
    LifeformsConfiguration,
    PlantsConfiguration,
    PlantsGeneraConfiguration,
)

from .sheets_configuration import sheets_configuration as s_conf


def get_plants_from_xlsx_sheets(
    plants_sheet: pd.DataFrame,
    plant_types_sheet: pd.DataFrame,
    plants_config: PlantsConfiguration,
    lifeforms_config: LifeformsConfiguration,
) -> pd.DataFrame:
    """
    Get plants data, including plant_types (lifeforms), from document sheets.
    """
    plants = plants_sheet.copy()

    plants.iat[1, 0] = "idx"
    plants.at[1, plants_config.name_ru_column] = plants_config.name_ru_column
    plants.at[1, plants_config.name_lat_column] = plants_config.name_lat_column
    for name_in_column_name in (
        plants_config.height_column,
        plants_config.crown_diameter_column,
        plants_config.lifeform_short_column,
        plants_config.aggressiveness_column,
        plants_config.survivability_column,
        plants_config.invasiveness_column,
    ):
        plants.at[1, name_in_column_name] = name_in_column_name
    plants.columns = plants.iloc[1]
    plants = plants.rename(s_conf.names_shortings_mapping, axis=1).set_index("idx").iloc[3:]
    plants[plants_config.height_column] = plants[plants_config.height_column].apply(
        lambda x: None
        if x == "-"
        else float(x[x.index("-") + 1 :])
        if isinstance(x, str) and "-" in x
        else float(x)
        if isinstance(x, str)
        else float(f"{x.day}.{x.month}" if isinstance(x, date) else x)
    )
    plants[plants_config.crown_diameter_column] = plants[plants_config.crown_diameter_column].apply(
        lambda x: None
        if x == "-"
        else float(x)
        if isinstance(x, str)
        else float(f"{x.day}.{x.month}" if isinstance(x, date) else x)
    )
    plants = plants.dropna(subset=plants_config.name_lat_column).drop_duplicates(subset=plants_config.name_lat_column)

    # Считывание жизненных форм
    life_forms = plant_types_sheet.copy()
    life_forms[lifeforms_config.short_name_column] = life_forms[lifeforms_config.short_name_column].apply(str.lower)
    life_forms = life_forms.rename({"Расшифровка": "Тип растения"}, axis=1)
    plant_types = pd.Series(life_forms.set_index(lifeforms_config.short_name_column)[lifeforms_config.full_name_column])
    plants = plants.merge(plant_types, left_on=plants_config.lifeform_short_column, right_index=True, how="left")
    return plants


def get_plants_genera(plants_genera_sheet: pd.DataFrame, config: PlantsGeneraConfiguration) -> pd.DataFrame:
    """
    Get plants_genera dataframe from plants_genera sheet.
    """
    return plants_genera_sheet[[config.genus_column, config.plant_column]].dropna().copy()


def get_cohabitation(
    cohabitation_sheet: pd.DataFrame,
    genera: pd.DataFrame,
    log: Callable[[str], None],
    genera_config: PlantsGeneraConfiguration,
    cohabitation_config: GeneraCohabitationConfiguration,
) -> pd.DataFrame:
    """
    Get plants genera cohabitation parameters.
    """

    # Считывание родов
    cohabitation = cohabitation_sheet.copy()
    missing_genera = (
        set(cohabitation[cohabitation_config.genus_1_column].apply(str.lower))
        | set(cohabitation[cohabitation_config.genus_2_column].apply(str.lower))
    ) - set(genera[genera_config.genus_column].apply(str.lower))
    log(f"Отсутствующие рода, указанные в сочетаемости родов: {', '.join(missing_genera)}")

    log(
        "Указаны {} отношений родов, {} после удаления дубликатов".format(  # pylint: disable=consider-using-f-string
            cohabitation.shape[0],
            cohabitation.drop_duplicates(
                [cohabitation_config.genus_1_column, cohabitation_config.genus_2_column]
            ).shape[0],
        )
    )
    cohabitation = cohabitation.drop_duplicates(
        [cohabitation_config.genus_1_column, cohabitation_config.genus_2_column]
    ).dropna(subset=[cohabitation_config.genus_1_column, cohabitation_config.genus_2_column])
    return cohabitation
