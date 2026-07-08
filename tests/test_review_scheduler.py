from datetime import UTC, datetime, timedelta

from math_learning_graph.review import ReviewMemory, ReviewRating, schedule_next_review


def test_new_memory_reviews_tomorrow_after_good_recall():
    now = datetime(2026, 7, 8, tzinfo=UTC)

    memory = schedule_next_review(
        ReviewMemory(topic_id="fraction"),
        rating=ReviewRating.GOOD,
        now=now,
    )

    assert memory.topic_id == "fraction"
    assert memory.review_count == 1
    assert memory.interval_days == 1
    assert memory.due_at == now + timedelta(days=1)


def test_forgotten_memory_resets_interval_and_marks_lapse():
    now = datetime(2026, 7, 8, tzinfo=UTC)
    existing = ReviewMemory(
        topic_id="fraction",
        review_count=4,
        interval_days=12,
        ease_factor=2.8,
        lapse_count=1,
    )

    memory = schedule_next_review(existing, rating=ReviewRating.FORGOT, now=now)

    assert memory.review_count == 0
    assert memory.interval_days == 1
    assert memory.ease_factor < existing.ease_factor
    assert memory.lapse_count == 2
    assert memory.due_at == now + timedelta(days=1)
