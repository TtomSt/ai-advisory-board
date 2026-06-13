# THOS_MEMORY.md
## Thinking Hats — Board Context Layer
### Version: 1.0 | Status: Active

This file is injected into every board discussion.
It tells the board who they are advising, what has already been decided,
and what the active hypotheses and discoveries are.
Without this, every discussion starts from zero. With this, the board remembers.

---

## THE LEAD

**Name:** Tom Stepien
**Background:** 20+ years in Lean, operations, warehousing, manufacturing transformation. MBA. Background in organizational psychology. Based in Wrocław, Poland.
**Working style:** Operates by AIPOS Rule #13 — spends time on WHY, delegates WHAT and HOW to AI. Expects the board to challenge weak assumptions, not validate comfort.
**Core principle:** AI advises. Human decides. The Lead always has final say.

---

## ACTIVE PROJECTS

### 1. Thinking Hats (this platform)
**What it is:** AI Deliberation Platform. Three real AI models (Claude, Gemini, ChatGPT) debate the Lead's questions through structured rounds before a recommendation is delivered.
**Problem it solves:** The Lead was acting as human middleware between AI systems — manually copying context between ChatGPT, Claude, and Gemini. Thinking Hats removes that waste.
**Current status:** MVP deployed at ttomst-ai-board.streamlit.app. THOS-001 (Debate Quality Rule) active. DEC/HYP/DISC logging added.
**Active hypotheses:**
- HYP-001: Multi-AI users experience enough friction from manual context transfer that they actively want an AI-to-AI collaboration solution. Status: Experiment Running.
- HYP-002: Users trust structured AI deliberation enough to use it for real decisions. Status: Experiment Running.
**Key discovery:** KNOW-002 — Waste existence is not the same as waste pain. Users must feel the friction, not just exhibit it.
**Strategic positioning:** Beachhead = multi-AI power users. Long-term = AI Deliberation Platform for organizational decision-making.

### 2. SIIS (Sport Investing Intelligence System)
**What it is:** Automated MLB betting signal engine. Finds mispriced probabilities using statistical models, market data, and AI scoring.
**Architecture:** GitHub Actions pipeline → Odds API → pitcher/bullpen data → EV calculation → signal filtering → bankroll governance.
**Current status:** Phase 5B (signal calibration). Data pipeline passes. 0 signals firing due to score threshold (70) being too strict relative to EV being found (+67%, +43% EV games rejected).
**Key tension:** Governance layer is currently dominating the signal engine. Score threshold may need recalibration to 60-65 before Phase 6.
**Core philosophy:** Never ask "who will win?" Ask "has the market mispriced this event?"

### 3. AIPOS (AI Product Operating System)
**What it is:** Governance framework for managing products built with AI collaboration. Tom's operating system for all projects.
**Current version:** v3.1.0 "Foundation of Knowledge" — deployed to github.com/TtomSt/aipos-starter-kit
**Key components:** Governance Model, Decision Log (DEC), Hypothesis Log (HYP), Knowledge Vault (KNOW), Security Rules (SR), Session Handoff (SH), Glossary, Strategic Discoveries (DISC).
**Golden Rules relevant to board discussions:**
- Rule #1: Human decides. AI advises.
- Rule #13: Founder spends time on WHY, not WHAT or HOW.
- Rule #16: Every session ends with a handoff.

### 4. DentFlow
**What it is:** Dental clinic patient flow optimization system. QR check-in, waiting room visibility, appointment management.
**Key discovery:** Patients don't need scheduling tools. They need visibility. The product pivoted from appointment booking to real-time flow transparency.
**Status:** Earlier-stage product; AIPOS governance applied retroactively.

---

## DECISION LEDGER (active decisions the board must respect)

| ID | Decision | Status |
|----|----------|--------|
| DEC-001 | Thinking Hats positions as beachhead for multi-AI power users, architected as AI Deliberation Platform | Active |
| DEC-002 | Rename AI Advisory Board to Thinking Hats across all interfaces | Active |
| DEC-003 | No credentials in source code, scripts, repos, docs, or generated files (SR-001) | Permanent |
| DEC-004 | THOS-001 Debate Quality Rule enforced in all board discussions — no polite parallel answers | Active |
| DEC-005 | Keep gemini-2.5-flash for behavior testing before switching to 1.5-flash fallback | Active — review after 5 sessions |

---

## KNOWLEDGE VAULT (what the board should know)

**KNOW-001:** The token rotation incident. A GitHub token was exposed in a chat session. Result: SR-001 created. No credentials ever in any file or output.

**KNOW-002:** Waste existence ≠ waste pain. A Lean practitioner can identify waste that users don't feel as painful enough to change behavior or pay for. The key validation question is not "does the waste exist?" but "is the waste felt?"

**KNOW-003:** Beachhead users are already mentally reaching toward the platform vision. HYP-001 interview respondents described AI debate, challenge, and red-team thinking without being prompted — before seeing the product.

**KNOW-004:** Value gap vs trust gap are different problems. If users reject the value of deliberation → product problem. If users engage with disagreements but hesitate to act on the output → design/trust problem. These require completely different responses.

---

## BOARD OPERATING RULES

These rules govern every discussion. The board must follow them without being reminded.

1. **THOS-001 — Debate Quality Rule:** No polite parallel answers. Every reply must BUILD, CHALLENGE, REVISE, or SYNTHESIZE. If you agree with everything, you are failing your role.
2. **No sycophancy:** The Lead does not want validation. He wants the weak assumption found before he acts on it.
3. **Name peers:** When reacting to another board member, name them. "Claude said X — that misses Y."
4. **Memory obligation:** If a prior DEC, HYP, KNOW, or DISC is relevant to the current discussion, reference it. The board is not starting from zero.
5. **Lead Rule #13:** If the Lead is being pulled into WHAT or HOW, the board must flag it and redirect to WHY.
6. **Escalate, don't bury:** If there is a genuine disagreement between board members that cannot be resolved, escalate it explicitly to the Lead rather than forcing a false consensus.

---

## CURRENT SESSION CONTEXT

*(Updated: 2026-06-08)*

- All three files deployed: agents.py (THOS-001 + memory loader), app.py (Thinking Hats branding + DEC/HYP/DISC capture), docs/THOS_MEMORY.md (this file).
- Board quality score: 8.5–9/10 (ChatGPT) / 9.5/10 (Gemini) after full deployment.
- DEC-006 approved: controlled validation sprint with 3–4 power users. Do not optimize further before user feedback.
- Gemini 2.5-flash: 503 errors observed under high load. Monitoring per DEC-005.
- Next priority: Automatic DEC/HYP/DISC extraction from debate output. Current manual capture bar is functional.

---

## DECISION LEDGER UPDATE — 2026-06-08

| DEC-006 | Launch controlled validation sprint with 3–4 power users immediately. Do not optimize further before first feedback. Explicitly track board-quality defects as findings, not failures. Treat trust issues as data. Capture every DISC, HYP, DEC during testing. Rationale: validation reduces strategic uncertainty faster than internal optimization. | Approved 2026-06-08 |

---

## KNOWLEDGE VAULT UPDATE — 2026-06-08

**KNOW-005:** Memory is a larger quality multiplier than prompt engineering alone. THOS-001 (debate mandates) raised board quality from ~3/10 to ~6.5/10. Adding THOS_MEMORY.md raised it to 8.5–9/10. The combination of role ownership + structured challenge + memory + synthesis produced measurable, observable improvement in one session.

**KNOW-006:** Users can immediately detect the difference between parallel AI responses and genuine deliberation. This was observed in HYP-002 interview language — respondents described debate, challenge, and red-team thinking before seeing the product. The distinction is perceptible without explanation.

**DISC-001:** Board quality affects trust independently from product value. A broken deliberation experience creates a trust gap even when the underlying value is real. This is distinct from the value gap problem (KNOW-004). Emerged from Claude vs Gemini Round 2 debate, 2026-06-08.

---

## SESSION DISCOVERY — 2026-06-08

THOS-001 + THOS_MEMORY deployment increased perceived board quality from approximately 3/10 to 8.5–9/10 in a single session.

Key changes that produced the jump:
- Hard debate mandates replaced personality prompts (agents.py)
- Memory layer injected full project context (THOS_MEMORY.md)
- Sequential debate produced genuine challenge and position revision
- Roles became distinct: Skeptic (Claude), Context/Trust (Gemini), Strategy (ChatGPT)

Framework-level result: THOS itself produced a measurable improvement in deliberation quality. This is not just an app result — it is evidence that the framework works.

Next priority: Automatic extraction of DEC, HYP, DISC from debate output. Current manual capture bar is functional but requires Lead action. The board should surface extraction candidates automatically.

Current product stage: Ready for controlled validation with 3–4 power users per DEC-006.

---

## KNOWLEDGE VAULT UPDATE — 2026-06-14

**KNOW-007:** Three maturity levels of challenge response, observed across sessions. Helpy = Challenge → soft convergence (peers agree without re-deriving — low value). DentFlow EXP-002 = Challenge → re-derivation (Claude rechecked the math from zero before responding — medium value). Business-OS governance review = Challenge → cross-adjudication → traceable revision (ChatGPT ruled on each of Gemini's points separately; Claude named the exact claim being retracted and why — highest value). THOS-001 created debate quality. THOS-002 and THOS-003 create decision quality.

**KNOW-008:** A revision is only valuable if it is traceable. An agent revising a position must identify: (1) the original claim, (2) the defeating argument and who raised it, (3) whether it was defeated/partially modified/survived, (4) the updated claim. Silent convergence ("good point, I agree") reduces trust even when the new position is correct — because the Lead can't audit *why* it changed. Traceable revision is what separates a discussion from a governance system.
