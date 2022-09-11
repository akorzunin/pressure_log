from typing import NewType, Optional
from pydantic import BaseModel

DateStamp = NewType("DateStamp", str) # dd.mm.yyyy
TimeStamp = NewType("TimeStamp", str) # hh:mm


class MeasureData(BaseModel):
    up: int
    down: int
    pulse: int
    timestamp: TimeStamp


class DayData(BaseModel):
    day_id: int
    date: DateStamp
    morning: Optional[MeasureData]
    evening: Optional[MeasureData]


class User(BaseModel):
    user_id: int
    items: list[DayData]
