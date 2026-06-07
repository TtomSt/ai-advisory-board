# 07_Architecture.md

# Architecture — Thinking Caps

**Project:** Thinking Caps
**Version:** 1.0 — Prototype
**Date:** 2026-06-05
**Author:** Engineering AI (Claude)
**AIPOS version:** v3.1.0
**Status:** Working prototype — not production architecture

---

## Purpose

Document the technical structure of the current working prototype.

This is not a conceptual design. A working prototype exists at:
- Repository: https://github.com/TtomSt/ai-advisory-board
- Live deployment: https://ttomst-ai-board.streamlit.app

---

## System Overview

Thinking Caps is a multi-model AI deliberation platform. The user submits a single question. The platform routes it to multiple AI models simultaneously. Each model produces an initial response. The models then receive each other's responses and produce challenge/refinement responses. The final output is a structured deliberation the user can read and act on.

Current prototype implements this as a Streamlit web application with direct API calls to three AI providers.

---

## Current Tech Stack

| Layer | Technology | Notes |
|---|---|---|
| Frontend | Streamlit | Python-based web UI |
| Backend | Streamlit (same process) | No separate backend service |
| AI — Model 1 | OpenAI API (GPT-4) | Direct API call |
| AI — Model 2 | Anthropic API (Claude) | Direct API call |
| AI — Model 3 | Google Generative AI (Gemini) | Direct API call |
| Hosting | Streamlit Community Cloud | ttomst-ai-board.streamlit.app |
| Storage | None | No persistent storage in prototype |
| Authentication | None | No auth in prototype |
| Database | None | Session state only |

---

## System Diagram

```
User (browser)
      │
      ▼
┌─────────────────────────────┐
│     Streamlit App           │
│  (frontend + backend)       │
│                             │
│  1. Receive question        │
│  2. Route to all models     │
│  3. Collect responses       │
│  4. Route responses back    │
│  5. Collect challenges      │
│  6. Display deliberation    │
└─────────────────────────────┘
      │           │           │
      ▼           ▼           ▼
 OpenAI API  Anthropic API  Google AI API
  (GPT-4)    (Claude)       (Gemini)
```

---

## Data Flow

1. User enters a question in the Streamlit interface
2. App sends the question simultaneously (or sequentially) to all three AI APIs
3. Each model returns an initial response
4. App compiles all initial responses and sends each model the question + all other models' responses
5. Each model produces a challenge/refinement response
6. App displays the full deliberation: initial responses + challenges + any synthesis
7. User reads the output and makes a final decision

---

## Key Technical Decisions

| Decision | Choice | Reason |
|---|---|---|
| Framework | Streamlit | Fastest path to working prototype; Python-native |
| API calls | Direct (no middleware) | Simplicity; no abstraction layer needed for prototype |
| Hosting | Streamlit Community Cloud | Free, zero-config deployment for validation phase |
| Storage | None | Validation prototype does not need persistence |
| Models | GPT-4, Claude, Gemini | The three dominant general-purpose models; widest coverage |

---

## Future Model Candidates

The architecture should support additional models without structural changes. Candidates approved for future integration:

- Grok (xAI)
- DeepSeek
- Perplexity
- Open-source local models (Ollama or similar)

---

## Constraints

**Prototype constraints (intentional):**
- No session persistence — each page load starts fresh
- No user accounts — single-user, no identity layer
- No conversation history — no memory across sessions
- Sequential API calls may add latency — parallel calls not yet implemented
- API costs paid by Founder — no billing layer

**External constraints:**
- API rate limits from OpenAI, Anthropic, Google
- Streamlit Community Cloud limits on compute and memory
- API keys stored as Streamlit secrets (environment variables) — not in code

---

## Security Considerations

- API keys stored in Streamlit secrets (environment variables), never in source code — SR-001 compliant
- No user data stored — no PII risk in prototype
- No authentication — intentional for prototype; required before any multi-user deployment
- GitHub repository is public — source code is visible; no secrets in repository

---

## Technical Risks

| Risk | Level | Mitigation |
|---|---|---|
| API latency makes deliberation feel slow | Medium | Parallel API calls in Phase 2 |
| Streamlit not suitable for production scale | High | Architecture redesign at Phase 1 exit (DEC-003) |
| API costs become significant with real users | Medium | Cost tracking before Phase 2 rollout |
| Model API changes break integration | Low | Thin abstraction layer in Phase 2 |

---

## Known Technical Debt

| Item | Priority | Notes |
|---|---|---|
| Sequential vs parallel API calls | P2 | Parallel calls reduce latency significantly |
| No error handling for API failures | P1 | If one model fails, session breaks |
| No loading states or progress indicators | P2 | UX improvement for Phase 2 |
| Streamlit session state only | P3 | Replaced entirely in Phase 2 architecture |

---

## Out of Scope — Phase 1

The following are explicitly not built in Phase 1:

- User accounts or authentication
- Persistent conversation storage
- Multi-user or team features
- Custom model selection per session
- API cost tracking dashboard
- Export or sharing of deliberation outputs
- Mobile-optimized interface

---

## Phase 2 Architecture Note

If Phase 1 validates the product, the production architecture will be reassessed before Phase 2 implementation begins. Streamlit is a prototype framework. Production will likely require a dedicated backend (FastAPI or similar), persistent storage, authentication, and a proper frontend. This will be captured as a new DEC entry superseding DEC-003.
