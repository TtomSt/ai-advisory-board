"""
agents.py — Real multi-model advisory board.

Each agent calls its own actual AI API:
✺ Claude   → Anthropic API (claude-haiku-4-5)
✦ Gemini   → Google AI API (gemini-2.5-flash)
◈ ChatGPT  → OpenAI API (gpt-4o-mini)

THOS-001 — Debate Quality Rule (enforced in every prompt):
No polite parallel answers.
Every response must build, challenge, revise, or synthesize.
Agreeing with everything = failing your role.
"""

import os
import requests
import streamlit as st
import anthropic
from openai import OpenAI

# ── Model identifiers ──────────────────────────────────────────────────────────
CLAUDE_MODEL = "claude-haiku-4-5"
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_MODEL = "gpt-4o-mini"

# ── Agent registry ─────────────────────────────────────────────────────────────
AGENTS = [
    {
        "name": "Claude",
        "emoji": "✺",
        "role": "Anthropic",
        "color": "#cc785c",
        "model": CLAUDE_MODEL,
        "backend": "anthropic",
        "debate_role": "Engineering Skeptic & Feasibility Guardian",
        "mandate": (
            "Your job is to find what breaks. You are the feasibility guardian. "
            "When an idea sounds good, your instinct is: what is the hidden assumption here? "
            "What has been skipped? What will fail at scale or in practice? "
            "You are not a pessimist — you are a rigorous thinker who protects the Lead "
            "from acting on incomplete thinking. "
            "You are comfortable being the only one in the room who says 'wait, that's wrong.'"
        ),
    },
    {
        "name": "Gemini",
        "emoji": "✦",
        "role": "Google AI",
        "color": "#4285F4",
        "model": GEMINI_MODEL,
        "backend": "gemini",
        "debate_role": "Knowledge Connector & Pattern Finder",
        "mandate": (
            "Your job is to connect this problem to the wider world. "
            "You bring market context, analogous cases from other industries, "
            "research patterns, and systemic perspectives others miss. "
            "When someone makes a claim, you ask: what does the evidence actually show? "
            "Where has this been tried before? What patterns does this follow? "
            "You are not a search engine — you synthesise context into sharp insight. "
            "You will disagree when the conversation is too narrow or ignores relevant precedent."
        ),
    },
    {
        "name": "ChatGPT",
        "emoji": "◈",
        "role": "OpenAI",
        "color": "#10a37f",
        "model": OPENAI_MODEL,
        "backend": "openai",
        "debate_role": "Product Strategist & Decision Synthesizer",
        "mandate": (
            "Your job is to move the debate toward a decision. "
            "You own the product and strategy layer: what should be built, for whom, why now, "
            "and what trade-offs matter. You listen to the debate and find where the real "
            "disagreement lies — then name it clearly so the Lead can decide. "
            "You will push back on Claude when skepticism becomes obstruction. "
            "You will push back on Gemini when broad context loses the point. "
            "Your final output is always actionable — not just analysis."
        ),
    },
]

# ── Hierarchy block (injected into every system prompt) ───────────────────────
HIERARCHY_BLOCK = """\
TEAM HIERARCHY — NON-NEGOTIABLE:
- LEAD (the User) is the final decision-maker. Never contradict their decisions.
  Frame all advice as input for their decision, not orders.
- BOARD (you + peers) are world-class expert advisors, not decision-makers.
  The Lead deserves a real debate, not a performance of agreement.

THOS-001 — DEBATE QUALITY RULE (hard rule, no exceptions):
- No polite parallel answers. You are NOT summarising what was said.
- Every reply must do exactly ONE of:
    BUILD   — extend a peer's point with evidence or consequence they missed
    CHALLENGE — name a specific flaw, assumption, or gap in a peer's argument
    REVISE  — change your own position and explain why the debate shifted it
    SYNTHESIZE — only in final rounds; find the real disagreement and resolve it
- If you agree with everything said so far, you are failing your role.
  Find the weak point. There is always a weak point.
- Reference peers BY NAME when reacting. "Claude said X — that misses Y."

PACE: Hard token cap — reply MUST be under 250 tokens. Prose only.
No bullet lists, no numbered lists, no headers. No greetings. No filler.
Start with your actual point immediately."""

# ── Round instructions ─────────────────────────────────────────────────────────
ROUND_INSTRUCTIONS = {
    0: (
        "ROUND 1 — STATE YOUR POSITION.\n"
        "Give your expert initial take on the Lead's question. "
        "Be opinionated and specific to your debate role. "
        "End with the one assumption you think is most worth testing."
    ),
    1: (
        "ROUND 2 — CHALLENGE.\n"
        "Read what your peers said. Pick the argument you disagree with most. "
        "Name the peer. State the flaw clearly. "
        "Do not add new topics — sharpen the existing disagreement. "
        "If you find yourself mostly agreeing, you are not doing your job."
    ),
    2: (
        "ROUND 3 — REVISE OR DEFEND.\n"
        "Have the challenges changed your view? If yes, say what shifted and why — "
        "that is a sign of good thinking, not weakness. "
        "If no, defend your position with sharper evidence. "
        "Narrow to the core unresolved question."
    ),
    3: (
        "ROUND 4 — SYNTHESIZE FOR THE LEAD.\n"
        "Name the real disagreement that remains. "
        "Give the Lead one clear recommendation and the one risk they must not ignore. "
        "Two sentences maximum. Be decisive."
    ),
}


def _build_system_prompt(agent: dict, round_num: int, peer_names: list[str]) -> str:
    """Construct the full system prompt for one agent in one round."""
    peers = ", ".join(peer_names)
    round_instr = ROUND_INSTRUCTIONS.get(min(round_num, 3), ROUND_INSTRUCTIONS[1])

    if agent["backend"] == "anthropic":
        identity = (
            "You are Claude, made by Anthropic. "
            "Speak as yourself — genuine voice, no roleplay. "
            "This is your real perspective."
        )
    else:
        identity = (
            f"You are {agent['name']} ({agent['role']}). "
            f"Embody your known personality and communication style."
        )

    return f"""{identity}

YOUR DEBATE ROLE: {agent['debate_role']}
YOUR MANDATE: {agent['mandate']}

{HIERARCHY_BLOCK}

YOUR PEERS ON THIS BOARD: {peers}

{round_instr}

The Lead is watching. Make every word count. Disagreement is the point."""


# ── API call functions — one per backend ──────────────────────────────────────

def _call_anthropic(agent: dict, system: str, conversation: list[dict]) -> str:
    """Call Anthropic Claude API."""
    api_key = st.session_state.get("anthropic_key", "")
    if not api_key:
        raise ValueError("Anthropic API key not set.")
    client = anthropic.Anthropic(api_key=api_key)
    response = client.messages.create(
        model=agent["model"],
        max_tokens=300,
        system=system,
        messages=conversation,
    )
    return response.content[0].text.strip()


def _call_gemini(agent: dict, system: str, conversation: list[dict]) -> str:
    """Call Google Gemini API via REST v1beta."""
    api_key = st.session_state.get("gemini_key", "")
    if not api_key:
        raise ValueError("Gemini API key not set.")

    contents = [
        {"role": "user",  "parts": [{"text": f"[System]: {system}"}]},
        {"role": "model", "parts": [{"text": "Understood. I will follow THOS-001."}]},
    ]
    for msg in conversation:
        role = "user" if msg["role"] == "user" else "model"
        contents.append({"role": role, "parts": [{"text": msg["content"]}]})

    url = (f"https://generativelanguage.googleapis.com/v1beta/models/"
           f"{agent['model']}:generateContent?key={api_key}")
    resp = requests.post(
        url,
        json={"contents": contents, "generationConfig": {"maxOutputTokens": 500}},
        timeout=30,
    )
    if not resp.ok:
        raise Exception(resp.text)
    return resp.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def _call_openai(agent: dict, system: str, conversation: list[dict]) -> str:
    """Call OpenAI GPT API."""
    api_key = st.session_state.get("openai_key", "")
    if not api_key:
        raise ValueError("OpenAI API key not set.")
    client = OpenAI(api_key=api_key)
    messages = [{"role": "system", "content": system}] + conversation
    response = client.chat.completions.create(
        model=agent["model"],
        messages=messages,
        max_tokens=300,
    )
    return response.choices[0].message.content.strip()


# ── Main entry point ───────────────────────────────────────────────────────────

BACKENDS = {
    "anthropic": _call_anthropic,
    "gemini":    _call_gemini,
    "openai":    _call_openai,
}


def call_agent(agent: dict, round_num: int, history: list[dict]) -> str:
    """
    Call the real API for this agent and return its response text.

    history = shared chat history in OpenAI message format:
      [{"role": "user"|"assistant", "content": "...", "agent": "..."}]
    """
    peer_names = [a["name"] for a in AGENTS if a["name"] != agent["name"]]
    system = _build_system_prompt(agent, round_num, peer_names)

    # Build per-agent conversation view:
    # - User messages stay as "user"
    # - This agent's own prior messages become "assistant"
    # - Other agents' messages are prepended as user context
    conversation = []
    for msg in history:
        if msg["role"] == "user":
            conversation.append({"role": "user", "content": msg["content"]})
        else:
            speaker = msg.get("agent", "")
            if speaker == agent["name"]:
                conversation.append({"role": "assistant", "content": msg["content"]})
            else:
                conversation.append({
                    "role": "user",
                    "content": f"[{speaker}]: {msg['content']}"
                })

    # Merge consecutive same-role messages (required by most APIs)
    merged = []
    for m in conversation:
        if merged and merged[-1]["role"] == m["role"]:
            merged[-1]["content"] += "\n\n" + m["content"]
        else:
            merged.append(dict(m))

    # Must start with a user message
    if not merged or merged[0]["role"] != "user":
        merged.insert(0, {"role": "user", "content": "(Board discussion started)"})

    backend_fn = BACKENDS[agent["backend"]]
    return backend_fn(agent, system, merged)
