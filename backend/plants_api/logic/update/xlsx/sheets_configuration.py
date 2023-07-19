"""
Document sheet configuration is defined here.
"""
from dataclasses import dataclass
from typing import Literal


@dataclass
class SheetsConfiguration:
    """
    Configuration class for excel sheets defining some of the parsing rules.

    Content:
    - `park_sheets` contains a list of sheet names with parks plants data.
    - `plants_naming_exceptions` is a dictionary with a normalized plant name_ru as (key) which
        can be used in the document, but is stored in the database with (value) name_ru.
    - `names_shortings_mapping` is a column names mapping from short names used in the document to their
        full versions from the database.
    - `plants_columns_mapping` is a mappnig of column names to the listing database tables.
    - `additional_columns` is a set of columns which are used after parsing, but are not listing ones.
    """

    plants_naming_exceptions: dict[str, str]
    names_shortings_mapping: dict[str, str]
    plants_columns_mapping: dict[
        str,
        Literal[
            "limitation_factors",
            "soil_acidity_types",
            "soil_fertility_types",
            "soil_types",
            "light_types",
            "humidity_types",
        ],
    ]
    additional_columns: set[str]


sheets_configuration = SheetsConfiguration(
    plants_naming_exceptions={
        "Клен сахаристый": "Клён сахарный",
        "Шиповник колючейший Шиповник": "Шиповник колючейший",
    },
    names_shortings_mapping={
        "Уст. к пересыханию": "Устойчивость к пересыханию",
        "Уст. к подтоплению": "Устойчивость к подтоплению",
        "Агресс-ть развития": "Агрессивность развития",
        "Назначение, хар-р использ-я": "Назначение, характер использования",
        "Ксерофит": "Мало воды",
        "Мезофит": "Средняя",
        "Гигрофит": "Много воды",
        "Средне плодородные": "Средне плодородная",
        "Бедные почвы": "Бедная почва",
    },
    plants_columns_mapping=(
        {
            name: "limitation_factors"
            for name in (
                "Устойчивость к переуплотнению",
                "Устойчивость к засолению",
                "Устойчивость к пересыханию",
                "Устойчивость к подтоплению",
                "Газостойкость",
                "Ветроустойчивость",
            )
        }
        | {
            name: "soil_acidity_types"
            for name in (
                "Сильнокислые (4)",
                "Кислые (5)",
                "Слабокислые (6)",
                "Нейтральные (7)",
                "Слабощелочные (8)",
                "Щелочные (9)",
                "Сильнощелочные (10)",
            )
        }
        | {name: "soil_fertility_types" for name in ("Плодородная", "Средне плодородные", "Бедные почвы")}
        | {
            name: "soil_types"
            for name in (
                "Песчаная",
                "Супесчаная",
                "Суглинистая",
                "Глинистая",
                "Каменистые",
                "Щебнистые",
                "Тяжёлая",
                "Хорошо дренированная",
            )
        }
        | {name: "light_types" for name in ("Полное освещение", "Полутень", "Тень")}
        | {name: "humidity_types" for name in ("Мало воды", "Средняя", "Много воды")}
    ),
    additional_columns={f"USDA{i}" for i in range(1, 12)},
)
"""
Default sheets configuration.
"""
