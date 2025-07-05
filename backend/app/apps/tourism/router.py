import random
from typing import Annotated

from ai_service.bl import get_ai_tourism_info
from apps.common_resourses.schemas import SearchParamsSchema
from apps.tourism.crud import create_history, get_history_paginated
from apps.tourism.prompts import TourismSystemPromptsEnum, get_exclude_prompt
from apps.tourism.schemas import (
    PaginationSavedHistoryResponse,
    ResponseTourismDestinationSchema,
    UserRequestSchema,
)
from database.dependencies import get_async_session
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router_tourism = APIRouter()


@router_tourism.get("/")
async def get_destination(
    user_request: Annotated[UserRequestSchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> list[ResponseTourismDestinationSchema]:
    if not user_request.num_places:
        user_request.num_places = random.randint(3, 4)

    output = await get_ai_tourism_info(
        user_text=user_request.text,
        system_prompt=TourismSystemPromptsEnum.SUGGEST_LOCATION.format(
            num_placed=user_request.num_places,
            exclude_prompt=get_exclude_prompt(exclude=user_request.exclude),
        ),
    )
    if len(output) != user_request.num_places:
        # todo retry one time more? may be 2x costly.
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"AI failed to return exactly {user_request.num_places} places.",
        )

    await create_history(
        text=user_request.text,
        num_places=user_request.num_places,
        exclude=user_request.exclude,
        response_json=[row.dict() for row in output],
        session=session,
    )

    return output


@router_tourism.get("/history")
async def get_history(
    params: Annotated[SearchParamsSchema, Depends()],
    session: AsyncSession = Depends(get_async_session),
) -> PaginationSavedHistoryResponse:
    response = await get_history_paginated(params, session)
    return response
