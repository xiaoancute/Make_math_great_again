# Make Math Great Again

**Product meaning:** help students stop freezing on math terms, and first
understand *what relationship is being talked about*, before formal textbook
language. See [`docs/product.md`](docs/product.md).

Backend-first framework plus a thin Android learning shell for a
primary-to-junior-high math learning app.

The project focuses on the reusable core:

- textbook route and understanding route for math topics
- knowledge point schema
- prerequisite graph traversal
- AI teacher prompt and student-facing answer policy
- spaced review scheduling
- thin FastAPI endpoints
- Android 16 prototype that loads topics, tracks local mastery, and asks the teacher

Open-source projects used as design references are tracked in
[`docs/open-source-reference.md`](docs/open-source-reference.md). The short version:
borrow learning memory and graph ideas from MathClaw, graph structure ideas from
math-knowledge-graph, and AI tutor interaction patterns from MathVoice, while keeping
MMGA focused on Chinese curriculum alignment, prerequisite diagnosis, and concept
understanding rather than homework solving.

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
