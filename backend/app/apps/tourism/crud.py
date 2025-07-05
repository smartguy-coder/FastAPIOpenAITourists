from math import ceil

from apps.common_resourses.schemas import SearchParamsSchema, SortDirEnum
from apps.tourism.models import TourismRequestHistory
from apps.tourism.schemas import PaginationSavedHistoryResponse, SavedHistoryItemSchema
from sqlalchemy import and_, asc, desc, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession


async def create_history(
    text: str,
    exclude: str | None,
    num_places: int,
    response_json: list[dict],
    session: AsyncSession,
) -> TourismRequestHistory:
    history = TourismRequestHistory(
        text=text,
        exclude=exclude or "",
        num_places=num_places,
        response_json=response_json,
    )
    session.add(history)

    await session.commit()
    return history


async def get_history_paginated(
    params: SearchParamsSchema, session: AsyncSession
) -> PaginationSavedHistoryResponse:
    direction = asc if params.direction == SortDirEnum.ASC else desc
    query = select(TourismRequestHistory)
    count_query = select(func.count()).select_from(TourismRequestHistory)

    if params.q:
        # almost full text search. if need - add more search_field
        params_cleaned = params.q.translate(str.maketrans("-,.", "   "))
        words = [word for word in params_cleaned.strip().split() if len(word) > 1]
        search_filter_condition = or_(
            and_(*(search_field.icontains(word) for word in words))
            for search_field in [TourismRequestHistory.text]
        )

        query = query.filter(search_filter_condition)
        count_query = count_query.filter(search_filter_condition)

    sort_field = getattr(
        TourismRequestHistory, params.sort_by, TourismRequestHistory.id
    )
    query = query.order_by(direction(sort_field))

    offset = (params.page - 1) * params.limit
    query = query.offset(offset).limit(params.limit)

    result = await session.execute(query)

    result_count = await session.execute(count_query)
    total_count = result_count.scalar()

    return PaginationSavedHistoryResponse(
        items=[
            SavedHistoryItemSchema.model_validate(item)
            for item in result.scalars().all()
        ],
        total=total_count,
        page=params.page,
        limit=params.limit,
        pages=ceil(total_count / params.limit),
    )
