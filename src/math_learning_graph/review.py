from __future__ import annotations

from datetime import UTC, datetime, timedelta
from enum import IntEnum

from pydantic import BaseModel, ConfigDict, Field


class ReviewRating(IntEnum):
    FORGOT = 0
    HARD = 3
    GOOD = 4
    EASY = 5


class ReviewMemory(BaseModel):
    model_config = ConfigDict(frozen=True)

    topic_id: str
    review_count: int = 0
    interval_days: int = 0
    ease_factor: float = 2.5
    lapse_count: int = 0
    due_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


def schedule_next_review(
    memory: ReviewMemory,
    rating: ReviewRating,
    now: datetime | None = None,
) -> ReviewMemory:
    now = now or datetime.now(UTC)

    if rating == ReviewRating.FORGOT:
        interval_days = 1
        review_count = 0
        lapse_count = memory.lapse_count + 1
        ease_factor = max(1.3, memory.ease_factor - 0.25)
    else:
        review_count = memory.review_count + 1
        lapse_count = memory.lapse_count
        ease_factor = _next_ease(memory.ease_factor, rating)
        interval_days = _next_interval(memory.interval_days, review_count, ease_factor, rating)

    return memory.model_copy(
        update={
            "review_count": review_count,
            "interval_days": interval_days,
            "ease_factor": ease_factor,
            "lapse_count": lapse_count,
            "due_at": now + timedelta(days=interval_days),
        }
    )


def _next_ease(ease_factor: float, rating: ReviewRating) -> float:
    if rating == ReviewRating.HARD:
        return max(1.3, ease_factor - 0.15)
    if rating == ReviewRating.EASY:
        return ease_factor + 0.15
    return ease_factor


def _next_interval(
    interval_days: int,
    review_count: int,
    ease_factor: float,
    rating: ReviewRating,
) -> int:
    if review_count == 1:
        return 1
    if review_count == 2:
        return 3 if rating == ReviewRating.HARD else 6

    multiplier = 1.2 if rating == ReviewRating.HARD else ease_factor
    if rating == ReviewRating.EASY:
        multiplier = ease_factor + 0.3
    return max(1, round(max(interval_days, 1) * multiplier))
