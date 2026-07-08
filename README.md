# Make Math Great Again

Backend-first framework plus a first usable Android prototype for a
primary-to-junior-high math learning app.

The project focuses on the reusable core:

- textbook route and understanding route for math topics
- knowledge point schema
- prerequisite graph traversal
- AI teacher prompt and student-facing answer policy
- spaced review scheduling
- thin FastAPI endpoints
- Android 16 prototype that loads topics, tracks local mastery, and asks the teacher

The Android app lives in `android-app/`. It is intentionally small: native Java Activity,
no Compose, no extra UI framework, and no app-side domain logic. It lists knowledge
points, opens a detail page, saves locally marked mastered topics, shows prerequisite
gaps, and asks the backend for a student-facing teacher answer.
