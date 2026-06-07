# 06_Roadmap.md

# Roadmap — Thinking Caps

**Project:** Thinking Caps
**Last Updated:** 2026-06-05
**Owner:** Product AI (ChatGPT)
**AIPOS version:** v3.1.0

---

## Rule

Roadmap reflects validated hypotheses only.

No item enters Phase 2 or beyond without a validated HYP or approved DEC.

---

## Current Phase

**Phase 1 — Validation**
**Goal:** Prove that the beachhead user exists and values the core deliberation experience
**Target:** 2026-07-31 (proposed — Founder to confirm)

---

## Phase Overview

| Phase | Name | Goal | Status |
|---|---|---|---|
| 0 | Foundation | Governance, architecture, product direction | Complete — AIPOS onboarding sprint done |
| 1 | Validation | Prove beachhead user exists and values deliberation | In Progress |
| 2 | Implementation | Build validated features into stable product | Locked |
| 3 | Optimization | Improve UX, flow, performance, deliberation quality | Locked |
| 4 | Scale | Multi-model expansion, integrations, platform APIs | Locked |

---

## Phase 0 — Foundation

**Goal:** Project is ready to operate under AIPOS governance.

**Status: Complete**

| Item | Owner | Status |
|---|---|---|
| Working prototype exists | Engineering AI | Done |
| GitHub repository exists | Engineering AI | Done |
| Live deployment exists | Engineering AI | Done |
| AIPOS v3.1.0 onboarding sprint | Engineering AI | Done |
| 02_Product_Vision.md | Founder | Done |
| 03_Product_Hypotheses.md | Product AI | Done |
| 04_Decisions_Log.md | Product AI | Done |
| 07_Architecture.md | Engineering AI | Done |
| 06_Roadmap.md | Product AI | Done |

---

## Phase 1 — Validation

**Goal:** At least 3 external users confirm the beachhead pain and find deliberation value.

**Rule:** No Phase 2 features are built until Phase 1 exit criteria are met.

### Validation activities

| Activity | Linked HYP | Owner | Status |
|---|---|---|---|
| Identify 5–10 multi-AI power users for interviews | HYP-001 | Founder | Not started |
| Conduct structured interviews — friction discovery | HYP-001 | Founder | Not started |
| Run prototype sessions with 3–5 pilot users | HYP-002 | Founder | Not started |
| Evaluate trust in deliberated output vs manual process | HYP-002 | Founder / Product AI | Not started |
| Test advisory board vs technical framing | HYP-004 | Product AI | Not started |
| Ask willingness-to-pay question to pilot users | HYP-003 | Founder | Not started |

### Phase 1 exit criteria

All of the following must be true before Phase 2 begins:

- [ ] HYP-001: At least 4 of 7 interviewed users describe manual context transfer as an active friction point unprompted
- [ ] HYP-002: At least 3 of 5 pilot users trust the deliberated output without requiring raw individual responses
- [ ] HYP-003: At least 3 of 5 pilot users express willingness to pay €10–30/month for the prototype as-is
- [ ] Pilot feedback documented in 09_Pilot_Feedback.md
- [ ] Lessons Learned entry committed to 12_Lessons_Learned.md
- [ ] Session Handoff committed to docs/sessions/
- [ ] Founder written Go approval committed to GitHub

### Phase 1 known risks

| Risk | Mitigation |
|---|---|
| HYP-001 rejected — users tolerate the friction but don't actively want it removed | Stop. Do not build Phase 2. Reassess product positioning entirely. |
| HYP-002 rejected — users don't trust AI-to-AI deliberation over their own orchestration | Rework deliberation design and prompting before retesting. May be solvable without a pivot. |
| HYP-003 rejected — product has value but not commercial value at this price point | Test lower price points or alternative monetization before concluding. |
| Streamlit prototype too slow to impress pilot users | Fix P1 technical debt (error handling) before pilot sessions begin. |

---

## Phase 2 — Implementation

**Gate:** All Phase 1 exit criteria met. Founder Go approval on file.

**Rule:** Only approved, documented, and prioritized backlog items get built.

**Architecture decision required before Phase 2 begins:**
DEC-003 (Streamlit prototype) must be superseded by a production architecture decision. Key questions:
- Backend: FastAPI, Django, or other?
- Frontend: React, Next.js, or Streamlit extended?
- Storage: PostgreSQL, Supabase, or other?
- Auth: Clerk, Auth0, or other?
- Hosting: Vercel, Railway, Fly.io, or other?

**Candidate Phase 2 features (not approved — pending Phase 1 validation):**

| Feature | Linked HYP | Business Value |
|---|---|---|
| Parallel API calls | HYP-003 | Reduce deliberation latency |
| Error handling and recovery | — | Prototype stability |
| Session persistence | HYP-001 | Users can return to previous deliberations |
| Model selection UI | HYP-001 | User controls which models participate |
| Export deliberation output | HYP-001 | Users share or save results |
| User accounts | HYP-005 | Required for paid tier |

---

## Phase 3 — Optimization

**Gate:** Core product working, users retained after first session.

| Improvement | Goal |
|---|---|
| Deliberation quality tuning | Better challenge prompts, clearer synthesis |
| Latency reduction | Parallel calls, streaming responses |
| UX refinement | Cleaner deliberation display, better information hierarchy |
| Cost optimization | Smarter model routing, token efficiency |

---

## Phase 4 — Scale

**Gate:** Product validated and optimized, paying users exist.

| Initiative | Description |
|---|---|
| Additional models | Grok, DeepSeek, Perplexity, local models |
| Team features | Shared deliberation sessions, collaboration |
| Platform API | Allow external products to use Thinking Caps deliberation engine |
| Domain-specific deliberation | Research mode, legal mode, investment mode |
| Enterprise tier | SSO, admin controls, audit logs |

---

## Backlog (not yet phased)

| Item | Notes |
|---|---|
| Deliberation export (PDF/Markdown) | High interest from Founder — validate with pilot users first |
| Custom deliberation personas per model | Each model plays a defined role (devil's advocate, optimist, etc.) |
| Deliberation templates | Pre-configured question structures for common use cases |
