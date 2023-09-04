"""Sheets configuration class is defined here."""

from pydantic import BaseModel, Field


class LifeformsConfiguration(BaseModel):
    """Lifeforms sheet configuration"""

    short_name_column: str = "short_name"
    full_name_column: str = "full_name"


class PlantsConfiguration(BaseModel):
    """Plants sheet configuration"""

    name_ru_column: str = "name_ru"
    name_lat_column: str = "name_lat"
    height_column: str = "height"
    crown_diameter_column: str = "crown_diameter"
    lifeform_short_column: str = "lifeform_short"
    survivability_column: str = "survivability"
    aggressiveness_column: str = "aggressiveness"
    invasiveness_column: str = "invasiveness"


class PlantsGeneraConfiguration(BaseModel):
    """Plants-genera sheet configuration"""

    genus_column: str = "genus"
    plant_column: str = "plant"


class GeneraCohabitationConfiguration(BaseModel):
    """Plants-genera sheet configuration"""

    genus_1_column: str = "genus_1"
    cohabitation_column: str = "cohabitation"
    genus_2_column: str = "genus_2"
    comment_column: str = "comment"


class SheetsConfiguration(BaseModel):
    """Excel sheets configuration used for update plants information"""

    lifeforms_sheet: str = "lifeforms"
    plants_sheet: str = "plants"
    plants_genera_sheet: str = "plants_genera"
    genera_cohabitation_sheet: str = "genera_cohabitation"
    parks_sheets: list[str] = Field(default_factory=list)

    lifeforms_config: LifeformsConfiguration = Field(default_factory=LifeformsConfiguration)
    plants_config: PlantsConfiguration = Field(default_factory=PlantsConfiguration)
    plants_genera_config: PlantsGeneraConfiguration = Field(default_factory=PlantsGeneraConfiguration)
    genera_cohabitation_config: GeneraCohabitationConfiguration = Field(default_factory=GeneraCohabitationConfiguration)
