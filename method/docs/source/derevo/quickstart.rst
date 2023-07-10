Quickstart
==========

derevo Framework quick start guide

How to use the **derevo** library
----------------------------------------------------

-  **Step 1**. Import needed modules.

.. code:: python

    from derevo import Plant, Territory
    from derevo import enumerations as c_enum
    from derevo import get_compositions
    from derevo.optimal_resolution import get_best_resolution

    from .data_collection import (
        collect_cohabitations,
        collect_light_polygons,
        collect_limitation_polygons,
        collect_plants,
        collect_plants_dataframe,
        collect_plants_suitable_for_light,
        collect_plants_with_limitation_resistance,
        collect_species_in_parks,
    )

-  **Step 2**. Format collected plants information into the list of `Plant` classes.

.. code:: python

    plants_list: list[Plant] = [
        Plant(
            name_ru="Название растения",
            name_latin="latin name",
            genus="Род растения",
            life_form="Жизненная форма",
            limitation_factors_resistances={
                c_enum.LimitationFactor.FLOODING: c_enum.ToleranceType.NEGATIVE,
                c_enum.LimitationFactor.GAS_POLLUTION: c_enum.ToleranceType.NEUTRAL,
            },
            humidity_preferences={
                c_enum.HumidityType.HIGH: c_enum.ToleranceType.NEGATIVE,
                c_enum.HumidityType.NORMAL: c_enum.ToleranceType.POSITIVE,
            },
            light_preferences={
                c_enum.LightType.LIGHT: c_enum.ToleranceType.POSITIVE,
            },
            usda_zone_preferences={
                c_enum.UsdaZone.USDA2: c_enum.ToleranceType.NEGATIVE,
                c_enum.UsdaZone.USDA3: c_enum.ToleranceType.NEUTRAL,
                c_enum.UsdaZone.USDA4: c_enum.ToleranceType.POSITIVE,
                c_enum.UsdaZone.USDA5: c_enum.ToleranceType.POSITIVE,
                c_enum.UsdaZone.USDA6: c_enum.ToleranceType.NEUTRAL,
                c_enum.UsdaZone.USDA7: c_enum.ToleranceType.NEGATIVE,
            },
            is_invasive=False,
        ),
    ]
    plants_present: list[Plant] = []


-  **Step 3**. Create Territory information class.

.. code:: python

    territory_info = Territory(
        usda_zone=c_enum.UsdaZone.USDA5,
        limitation_factors=[c_enum.LimitationFactor.WINDINESS],
        humidity_types=[c_enum.HumidityType.NORMAL, c_enum.HumidityType.LOW],
        light_types=[c_enum.LightType.LIGHT, c_enum.LightType.DARKENED],
        soil_fertility_types=[c_enum.FertilityType.FERTIL, c_enum.FertilityType.SLIGHTLY_FERTIL],
    )


-  **Step 4**. Form a list of GeneraCohabitation classes from your data.

.. code:: python

    cohabitation_attributes = [
        GeneraCohabitation("Род растения", "Род растения", CohabitationType.POSITIVE),
        GeneraCohabitation("Род растения", "Другой род растения", CohabitationType.NEGATIVE),
    ]


-  **Step 5**. Get available plants cohabitations for the given area.

.. code:: python

    composition_plants = get_compositions(
        plants_available=plants_list,
        cohabitation_attributes=cohabitation_attributes,
        territory=territory_info,
        plants_present=plants_present,
    )
