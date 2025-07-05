from enum import StrEnum
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class CoordinatesSchema(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class ResponseTourismDestinationSchema(BaseModel):
    name: str
    description: str
    coords: CoordinatesSchema


class UserRequestSchema(BaseModel):
    text: str = Field(min_length=3, max_length=2048)
    exclude: str | None = Field(default=None, min_length=3, max_length=2048)
    num_places: int | None = Field(default=None, gt=0, le=10)


class SortDirEnum(StrEnum):
    ASC = 'asc'
    DESC = 'desc'


class SortByEnum(StrEnum):
    ID = 'id'
    CREATED_AT = 'created_at'


class SearchParamsSchema(BaseModel):
    q: Annotated[Optional[str], Field(default=None)] = None
    page: Annotated[int, Field(default=1, ge=1)]
    limit: Annotated[int, Field(default=10, ge=1, le=50)]
    direction: SortDirEnum = SortDirEnum.DESC
    sort_by: SortByEnum = SortByEnum.ID


class PaginationResponse(BaseModel):
    items: list
    total: int
    page: int
    limit: int
    pages: int


class PaginationSavedHistoryResponse(PaginationResponse):
    items: list[ResponseTourismDestinationSchema]
