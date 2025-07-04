from pydantic import BaseModel, Field


class CoordinatesSchema(BaseModel):
    lat: float = Field(..., ge=-90, le=90)
    lng: float = Field(..., ge=-180, le=180)


class ResponseTourismDestinationSchema(BaseModel):
    name: str
    description: str
    coords: CoordinatesSchema
