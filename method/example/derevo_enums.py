"""
Derevo library enumerations names mapping is hardcoded here.
"""

from derevo import enumerations as d_enum


class EnumAdapters:  # pylint: disable=too-few-public-methods
    """
    Hardcoded class cointaining dictionaries to convert values from russian namings in the database
    to derevo enumerations
    """

    humidity = {
        "Мало воды": d_enum.HumidityType.LOW,
        "Средняя": d_enum.HumidityType.NORMAL,
        "Много воды": d_enum.HumidityType.HIGH,
        "Влажность в воздухе": d_enum.HumidityType.HIGH,
    }

    soil = {
        "Песчаная": d_enum.SoilType.SANDY,
        "Супесчаная": d_enum.SoilType.SUBSANDY,
        "Суглинистая": d_enum.SoilType.LOAMY,
        "Глинистая": d_enum.SoilType.CLAYEY,
        "Каменистые": d_enum.SoilType.ROCKY,
        "Каменистая": d_enum.SoilType.ROCKY,
        "Щебнистые": d_enum.SoilType.GRAVELLY,
        "Тяжёлая": d_enum.SoilType.HEAVY,
        "Хорошо дренированная": d_enum.SoilType.DRAINED,
    }

    acidity = {
        "Сильнокислые (4)": d_enum.AcidityType.from_value(4),
        "Кислые (5)": d_enum.AcidityType.from_value(5),
        "Слабокислые (6)": d_enum.AcidityType.from_value(6),
        "Нейтральные (7)": d_enum.AcidityType.from_value(7),
        "Слабощелочные (8)": d_enum.AcidityType.from_value(8),
        "Щелочные (9)": d_enum.AcidityType.from_value(9),
        "Сильнощелочные (10)": d_enum.AcidityType.from_value(10),
    }

    fertility = {
        "Плодородная": d_enum.FertilityType.FERTIL,
        "Средне плодородная": d_enum.FertilityType.SLIGHTLY_FERTIL,
        "Бедная почва": d_enum.FertilityType.BARREN,
    }

    light = {
        "Полное освещение": d_enum.LightType.LIGHT,
        "Полутень": d_enum.LightType.DARKENED,
        "Тень": d_enum.LightType.DARK,
    }

    limitation_factors = {
        "Устойчивость к переуплотнению": d_enum.LimitationFactor.OVERCONSOLIDATION,
        "Устойчивость к засолению": d_enum.LimitationFactor.SALINIZATION,
        "Устойчивость к пересыханию": d_enum.LimitationFactor.DROUGHT,
        "Устойчивость к подтоплению": d_enum.LimitationFactor.FLOODING,
        "Газостойкость": d_enum.LimitationFactor.GAS_POLLUTION,
        "Ветроустойчивость": d_enum.LimitationFactor.WINDINESS,
    }

    life_forms = {
        "Дерево": d_enum.LifeForm.TREE,
        "Кустарник": d_enum.LifeForm.BUSH,
        "Почвопокровное ": d_enum.LifeForm.GROUND_COVER,
        "Лиана": d_enum.LifeForm.LIANA,
        "Многолетние травы": d_enum.LifeForm.PERENNIAL,
        "Луковичные": d_enum.LifeForm.BULBOUS,
        "Однолетники": d_enum.LifeForm.ANNUAL,
        "Болотное растение": d_enum.LifeForm.SWAMP_PLANT,
    }

    aggressiveness_levels = {value: d_enum.AggressivenessLevel.from_value(value) for value in range(-1, 2)}

    survivability_levels = {value: d_enum.SurvivabilityLevel.from_value(value) for value in range(-1, 2)}
