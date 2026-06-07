# 04_Decisions_Log.md

# Decisions Log — Thinking Caps

**Project:** Thinking Caps
**Last Updated:** 2026-06-05
**AIPOS version:** v3.1.0

---

## Purpose

This file is the source of truth for strategic project decisions.

Chat is not the source of truth.

Only decisions that are still actively directing the project are documented here. Decisions made before AIPOS governance that are no longer live are not backfilled.

---

## DEC-001

### Date
2026-06-05

### Status
Approved

### Category
D1 — Strategic

### Title
Product definition: Thinking Caps is an AI Deliberation Platform

### Context
The project was initially conceived as an "AI Advisory Board" — multiple AI models giving opinions. During AIPOS onboarding, the Founder identified the real problem: humans acting as manual communication layer between AI systems. This reframing changed the product definition from a presentation layer to a platform.

### Decision
Thinking Caps is an AI Deliberation Platform. Its core purpose is to remove human middleware from multi-AI workflows by enabling structured AI-to-AI deliberation before output is presented to the human decision maker.

The "Executive Advisory Board" concept is the first application of the platform, not the platform itself.

### Expected Impact
All product, architecture, and roadmap decisions now derive from the platform framing rather than the advisory board framing. This prevents premature narrowing of the product vision.

### Validation Method
Phase 1 validates the beachhead (power users). If validated, the platform framing is confirmed. If the beachhead does not exist, the framing must be revisited.

### Owner
Founder

---

## DEC-002

### Date
2026-06-05

### Status
Approved

### Category
D1 — Strategic

### Title
Phase 1 beachhead: multi-AI power users, not enterprise decision makers

### Context
Two valid markets exist: (1) power users who manually orchestrate AI systems, (2) organizations needing AI deliberation for high-stakes decisions. The enterprise market is larger but harder to validate and slower to access. The power user market is smaller but immediately accessible and personally validated.

### Decision
Phase 1 validation targets multi-AI power users — individuals who currently copy-paste context between 2+ AI systems and experience this as waste. Enterprise decision makers are the long-term market, not the Phase 1 target.

The Founder is the first confirmed user in this persona.

### Expected Impact
Phase 1 interviews, pilot sessions, and success criteria are all scoped to power users. No enterprise features, sales cycles, or organizational pilots in Phase 1.

### Validation Method
HYP-001 validates this decision. If 3–5 external power users confirm the pain, DEC-002 is confirmed. If the persona does not exist at sufficient scale, this decision must be revisited.

### Owner
Founder

---

## DEC-003

### Date
2026-06-05

### Status
Approved

### Category
D3 — Technical

### Title
Prototype built on Streamlit + direct API calls to OpenAI, Anthropic, Gemini

### Context
The prototype needed to be built quickly to validate the deliberation concept. Streamlit was chosen for rapid iteration. API calls go directly to OpenAI (GPT-4), Anthropic (Claude), and Google (Gemini).

### Decision
Current prototype uses Streamlit as the frontend and backend framework. AI model responses are fetched via direct API calls. No persistent storage, no authentication, no session management. This is a validation prototype, not a production architecture.

### Expected Impact
Fast iteration is enabled. Production constraints (latency, cost, scalability) are deferred. Architecture will be reassessed at Phase 1 exit before Phase 2 implementation begins.

### Validation Method
If Phase 1 validates the product, a Phase 2 architecture decision (DEC-XXX) will supersede this decision with a production-grade stack.

### Owner
Engineering AI

---

## DEC-004

### Date
2026-06-05

### Status
Approved

### Category
D6 — Research

### Title
Apply AIPOS v3.1.0 governance to Thinking Caps mid-project

### Context
Thinking Caps was started without formal governance. A working prototype exists at https://ttomst-ai-board.streamlit.app and https://github.com/TtomSt/ai-advisory-board. The decision was made to apply AIPOS v3.1.0 governance retroactively using the controlled entry point approach — producing only living documents, not backfilling history.

### Decision
Thinking Caps adopts AIPOS v3.1.0 governance from 2026-06-05. The AIPOS Onboarding Sprint produces 5 core documents. All prior undocumented decisions are superseded by the governance documents produced in this sprint. Development from this point forward follows full AIPOS discipline.

### Expected Impact
Clear phase structure, documented hypotheses, traceable decisions, and backlog control from this point forward. The prototype's existence is acknowledged but the product is formally treated as Phase 1 — Validation.

### Validation Method
Governance is working if: (a) no features are built without a validated HYP, (b) all significant decisions have DEC entries, (c) Phase 1 exit criteria are met before implementation begins.

### Owner
Founder

---

## Decision Category Definitions

| Category | Name | Owner | Examples |
|---|---|---|---|
| D1 | Strategic | Founder | Vision, direction, business model, market positioning |
| D2 | Product | Product AI | Feature decisions, roadmap, backlog, acceptance criteria |
| D3 | Technical | Engineering AI | Architecture, stack, implementation approach |
| D4 | Security | Engineering AI | Credentials, access, compliance, threat model |
| D5 | Operational | Product AI | Process, tooling, workflow, team structure |
| D6 | Research | Founder / Product AI | Market questions, experiments, competitor analysis |

---

## Decision Status Definitions

Hypothesis: Not yet proven.

Approved: Accepted direction.

Rejected: Decided not to pursue.

Superseded: Replaced by a newer decision.
