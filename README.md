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

The Android app lives in `android-app/`. It uses Kotlin, Jetpack Compose, and Material 3.
The app keeps domain logic in the backend: it lists knowledge points, opens a detail page,
saves locally marked mastered topics, shows prerequisite gaps, and asks the backend for a
student-facing teacher answer.

## AI teacher

The backend uses a deterministic local teacher when no API key is configured. Set
`OPENAI_API_KEY` to enable real model answers through the OpenAI Responses API. Set the
model name in the Android settings screen, or set `OPENAI_MODEL` on the backend. The Android
settings screen also accepts the backend host and port, for example `http://10.0.2.2:8000`,
and can test whether the backend, API key, and selected model are configured.
