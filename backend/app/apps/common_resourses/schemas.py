from enum import StrEnum
from typing import Annotated, Optional

from pydantic import BaseModel, Field


class PaginationResponse(BaseModel):
    items: list
    total: int
    page: int
    limit: int
    pages: int


class SortDirEnum(StrEnum):
    ASC = "asc"
    DESC = "desc"


class SortByEnum(StrEnum):
    ID = "id"
    CREATED_AT = "created_at"


class SearchParamsSchema(BaseModel):
    q: Annotated[Optional[str], Field(default=None)] = None
    page: Annotated[int, Field(default=1, ge=1)]
    limit: Annotated[int, Field(default=10, ge=1, le=50)]
    direction: SortDirEnum = SortDirEnum.DESC
    sort_by: SortByEnum = SortByEnum.ID
