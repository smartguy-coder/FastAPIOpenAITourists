from datetime import datetime

import sqlalchemy as sa
from database.base import Base
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


class TourismRequestHistory(Base):
    text: Mapped[str] = mapped_column(String(2048), index=True)
    exclude: Mapped[str] = mapped_column(String(2048))
    num_places: Mapped[int]
    response_json: Mapped[list[dict]] = mapped_column(
        JSONB, server_default=sa.text("'[]'::jsonb")
    )
