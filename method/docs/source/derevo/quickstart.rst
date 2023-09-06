##########
Quickstart
##########

derevo Framework quick start guide

How to use the **derevo** library
----------------------------------------------------

-  **Step 1**. Import needed modules (example package can be found in the project repository).

.. code:: python

    from derevo import Plant, Territory
    from derevo import enumerations as d_enum
    from derevo import get_compositions

    from example.data_collection import (
        collect_cohabitations,
        collect_light_polygons,
        collect_limitation_polygons,
        collect_plants,
        collect_plants_dataframe,
        collect_plants_suitable_for_light,
        collect_plants_with_limitation_resistance,
        collect_species_in_parks,
    )
    from derevo.models.cohabitation import CohabitationType, GeneraCohabitation

-  **Step 2**. Format collected plants information into the list of `Plant` classes.

.. code:: python

    plants_list: list[Plant] = [
        Plant(
            name_ru="Название растения",
            name_latin="latin name",
            genus="Род растения",
            life_form="Жизненная форма",
            limitation_factors_resistances={
                d_enum.LimitationFactor.FLOODING: d_enum.ToleranceType.NEGATIVE,
                d_enum.LimitationFactor.GAS_POLLUTION: d_enum.ToleranceType.NEUTRAL,
            },
            humidity_preferences={
                d_enum.HumidityType.HIGH: d_enum.ToleranceType.NEGATIVE,
                d_enum.HumidityType.NORMAL: d_enum.ToleranceType.POSITIVE,
            },
            light_preferences={
                d_enum.LightType.LIGHT: d_enum.ToleranceType.POSITIVE,
            },
            usda_zone_preferences={
                d_enum.UsdaZone.USDA2: d_enum.ToleranceType.NEGATIVE,
                d_enum.UsdaZone.USDA3: d_enum.ToleranceType.NEUTRAL,
                d_enum.UsdaZone.USDA4: d_enum.ToleranceType.POSITIVE,
                d_enum.UsdaZone.USDA5: d_enum.ToleranceType.POSITIVE,
                d_enum.UsdaZone.USDA6: d_enum.ToleranceType.NEUTRAL,
                d_enum.UsdaZone.USDA7: d_enum.ToleranceType.NEGATIVE,
            },
            is_invasive=False,
        ),
    ]
    plants_present: list[Plant] = []


-  **Step 3**. Create Territory information class.

.. code:: python

    territory_info = Territory(
        usda_zone=d_enum.UsdaZone.USDA5,
        limitation_factors=[d_enum.LimitationFactor.WINDINESS],
        humidity_types=[d_enum.HumidityType.NORMAL, d_enum.HumidityType.LOW],
        light_types=[d_enum.LightType.LIGHT, d_enum.LightType.DARKENED],
        soil_fertility_types=[d_enum.FertilityType.FERTIL, d_enum.FertilityType.SLIGHTLY_FERTIL],
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
