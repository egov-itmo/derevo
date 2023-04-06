"""
Functions which are used in document parsing are defined here.
"""
from datetime import date
from typing import Callable

import pandas as pd

from .sheets_configuration import sheets_configuration as s_conf


def get_plants_from_xlsx_sheets(plants_sheet: pd.DataFrame, plant_types_sheet: pd.DataFrame) -> pd.DataFrame:
    """
    Get plants data, including plant_types (lifeforms), from document sheets.
    """
    plants = plants_sheet.copy()

    plants.iat[1, 0] = "idx"
    plants.iat[1, 1] = "Название"
    plants.iat[1, 2] = "Латинское название"
    for name_in_column_name in (
        "Высота",
        "Размер кроны",
        "Жизненная форма",
        "Агресс-ть развития",
        "Живучесть",
        "Инвазивный вид",
        "Период цветения",
        "Назначение, хар-р использ-я",
    ):
        plants.at[1, name_in_column_name] = name_in_column_name
    plants.columns = plants.iloc[1]
    plants = plants.rename(s_conf.names_shortings_mapping, axis=1).set_index("idx").iloc[3:]
    plants["Высота"] = plants["Высота"].apply(
        lambda x: None
        if x == "-"
        else float(x[x.index("-") + 1 :])
        if isinstance(x, str) and "-" in x
        else float(x)
        if isinstance(x, str)
        else float(f"{x.day}.{x.month}" if isinstance(x, date) else x)
    )
    plants["Размер кроны"] = plants["Размер кроны"].apply(
        lambda x: None
        if x == "-"
        else float(x)
        if isinstance(x, str)
        else float(f"{x.day}.{x.month}" if isinstance(x, date) else x)
    )
    plants = plants.dropna(subset="Латинское название").drop_duplicates(subset="Латинское название")

    # Считывание жизненных форм
    life_forms = plant_types_sheet.copy()
    life_forms["Сокращение"] = life_forms["Сокращение"].apply(str.lower)
    life_forms = life_forms.rename({"Расшифровка": "Тип растения"}, axis=1)
    plant_types = pd.Series(life_forms.set_index("Сокращение")["Тип растения"])
    plants = plants.merge(plant_types, left_on="Жизненная форма", right_index=True, how="left")
    return plants


def get_plants_genera(plants_genera_sheet: pd.DataFrame) -> pd.DataFrame:
    """
    Get plants_genera dataframe from plants_genera sheet.
    """
    return plants_genera_sheet[["Род", "Вид"]].dropna().copy()


def get_cohabitation(
    cohabitation_sheet: pd.DataFrame, genera: pd.DataFrame, log: Callable[[str], None]
) -> pd.DataFrame:
    """
    Get plants genera cohabitation parameters.
    """

    # Считывание родов
    cohabitation = cohabitation_sheet.copy()
    missing_genera = (set(cohabitation["Род"].apply(str.lower)) | set(cohabitation["Род.1"].apply(str.lower))) - set(
        genera["Род"].apply(str.lower)
    )
    log(f"Отсутствующие рода, указанные в сочетаемости родов: {', '.join(missing_genera)}")

    log(
        f"Указаны {cohabitation.shape[0]} сочетаемостей родов,"
        f" {cohabitation.drop_duplicates(['Род', 'Род.1']).shape[0]} после удаления дубликатов"
    )
    cohabitation = cohabitation.drop_duplicates(["Род", "Род.1"]).dropna(subset=["Род", "Род.1"])
    return cohabitation
