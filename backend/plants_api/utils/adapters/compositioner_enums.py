"""
Compositioner enumerations names mapping is hardcoded here.
"""

from compositioner import enumerations as c_enum


class EnumAdapters:  # pylint: disable=too-few-public-methods
    """
    Hardcoded class cointaining dictionaries to convert values from russian namings in the database
    to compositioner enumerations
    """

    humidity = {
        "Мало воды": c_enum.HumidityType.LOW,
        "Средняя": c_enum.HumidityType.NORMAL,
        "Много воды": c_enum.HumidityType.HIGH,
        "Влажность в воздухе": c_enum.HumidityType.HIGH,
    }

    soil = {
        "Песчаная": c_enum.SoilType.SANDY,
        "Супесчаная": c_enum.SoilType.SUBSANDY,
        "Суглинистая": c_enum.SoilType.LOAMY,
        "Глинистая": c_enum.SoilType.CLAYEY,
        "Каменистые": c_enum.SoilType.ROCKY,
        "Каменистая": c_enum.SoilType.ROCKY,
        "Щебнистые": c_enum.SoilType.GRAVELLY,
        "Тяжёлая": c_enum.SoilType.HEAVY,
        "Хорошо дренированная": c_enum.SoilType.DRAINED,
    }

    acidity = {
        "Сильнокислые (4)": c_enum.AcidityType.from_value(4),
        "Кислые (5)": c_enum.AcidityType.from_value(5),
        "Слабокислые (6)": c_enum.AcidityType.from_value(6),
        "Нейтральные (7)": c_enum.AcidityType.from_value(7),
        "Слабощелочные (8)": c_enum.AcidityType.from_value(8),
        "Щелочные (9)": c_enum.AcidityType.from_value(9),
        "Сильнощелочные (10)": c_enum.AcidityType.from_value(10),
    }

    fertility = {
        "Плодородная": c_enum.FertilityType.FERTIL,
        "Средне плодородная": c_enum.FertilityType.SLIGHTLY_FERTIL,
        "Бедная почва": c_enum.FertilityType.BARREN,
    }

    light = {
        "Полное освещение": c_enum.LightType.LIGHT,
        "Полутень": c_enum.LightType.DARKENED,
        "Тень": c_enum.LightType.DARK,
    }

    limitation_factors = {
        "Устойчивость к переуплотнению": c_enum.LimitationFactor.OVERCONSOLIDATION,
        "Устойчивость к засолению": c_enum.LimitationFactor.SALINIZATION,
        "Устойчивость к пересыханию": c_enum.LimitationFactor.DROUGHT,
        "Устойчивость к подтоплению": c_enum.LimitationFactor.FLOODING,
        "Газостойкость": c_enum.LimitationFactor.GAS_POLLUTION,
        "Ветроустойчивость": c_enum.LimitationFactor.WINDINESS,
    }

    life_forms = {
        "Дерево": c_enum.LifeForm.TREE,
        "Кустарник": c_enum.LifeForm.BUSH,
        "Почвопокровное ": c_enum.LifeForm.GROUND_COVER,
        "Лиана": c_enum.LifeForm.LIANA,
        "Многолетние травы": c_enum.LifeForm.PERENNIAL,
        "Луковичные": c_enum.LifeForm.BULBOUS,
        "Однолетники": c_enum.LifeForm.ANNUAL,
        "Болотное растение": c_enum.LifeForm.SWAMP_PLANT,
    }

    aggressiveness_levels = {value: c_enum.AggressivenessLevel.from_value(value) for value in range(-1, 2)}

    survivability_levels = {value: c_enum.SurvivabilityLevel.from_value(value) for value in range(-1, 2)}
