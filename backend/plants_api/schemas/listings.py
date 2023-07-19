"""
Listing response is defined here.
"""

from pydantic import BaseModel

from plants_api.dto import ListingDto


class Listing(BaseModel):
    """
    Inner class of ListingResponse containing one entity name and id.
    """

    id: int
    name: str

    @classmethod
    def from_dto(cls, dto: ListingDto) -> "Listing":
        """
        Construct from DTO.
        """
        return cls(id=dto.id, name=dto.name)


class ListingResponse(BaseModel):
    """
    Listing response is shared by all listing endpoints as they all return names and ids of entities.
    """

    values: list[Listing]

    @classmethod
    def from_dtos(cls, dtos: list[ListingDto]) -> "ListingResponse":
        """
        Construct from DTOs list.
        """
        return cls(values=[Listing.from_dto(dto) for dto in dtos])
