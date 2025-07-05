from datetime import datetime

from apps.common_resourses.schemas import PaginationResponse
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


class SavedHistoryItemSchema(BaseModel):
    id: int
    created_at: datetime
    text: str
    exclude: str
    num_places: int
    response_json: list[ResponseTourismDestinationSchema]

    class Config:
        from_attributes = True


class PaginationSavedHistoryResponse(PaginationResponse):
    items: list[SavedHistoryItemSchema]
