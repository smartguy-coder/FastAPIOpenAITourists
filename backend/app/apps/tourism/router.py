from fastapi import APIRouter, Header, status, HTTPException, Query

from ai_service.bl import get_ai_tourism_info
from apps.tourism.prompts import TourismSystemPromptsEnum, get_exclude_prompt
from apps.tourism.schemas import ResponseTourismDestinationSchema

router_tourism = APIRouter()


@router_tourism.get("/")
async def get_destination(
    request: str = Query(..., min_length=3, max_length=2048),
    num_places: int = Query(default=4, gt=0, le=100),
    exclude: str = Query("", min_length=0, max_length=2048),
) -> list[ResponseTourismDestinationSchema]:

    return await get_ai_tourism_info(
        user_request=request,
        system_prompt=TourismSystemPromptsEnum.SUGGEST_LOCATION.format(
            num_placed=num_places,
            exclude_prompt=get_exclude_prompt(exclude=exclude),
        ),
    )
