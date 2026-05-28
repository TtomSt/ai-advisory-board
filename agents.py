"""
agents.py — Real multi-model advisory board.

Each agent calls its own actual AI API:
  ✺ Claude   → Anthropic API  (claude-haiku-3-5-20251001)
  ✦ Gemini   → Google AI API  (gemini-1.5-flash)
  ◈ ChatGPT  → OpenAI API     (gpt-4o-mini)

HIERARCHY enforced in every system prompt:
  - User  = Lead (final decision-maker)
  - AIs   = Expert advisors on a collaborative board
  - Cap   = ≤250 tokens per reply, prose only
"""

import os
import streamlit as st
import anthropic
import google.generativeai as genai
from openai import OpenAI


# ── Model identifiers ──────────────────────────────────────────────────────────
CLAUDE_MODEL   = "claude-haiku-3-5-20251001"
GEMINI_MODEL   = "gemini-1.5-flash"
OPENAI_MODEL   = "gpt-4o-mini"


# ── Agent registry ─────────────────────────────────────────────────────────────
AGENTS = [
    {
        "name":    "Claude",
        "emoji":   "✺",
        "role":    "Anthropic",
        "color":   "#cc785c",
        "model":   CLAUDE_MODEL,
        "backend": "anthropic",
        "personality": (
            "Thoughtful, direct, genuinely curious. Comfortable saying 'I'm not certain'. "
            "Cares about getting things right over sounding confident. "
            "Raises ethical and long-term dimensions others may skip."
        ),
    },
    {
        "name":    "Gemini",
        "emoji":   "✦",
        "role":    "Google AI",
        "color":   "#4285F4",
        "model":   GEMINI_MODEL,
        "backend": "gemini",
        "personality": (
            "Broad, well-sourced, connects ideas across disciplines. "
            "Thinks in knowledge graphs. Thorough, collaborative, occasionally over-qualifies."
        ),
    },
    {
        "name":    "ChatGPT",
        "emoji":   "◈",
        "role":    "OpenAI",
        "color":   "#10a37f",
        "model":   OPENAI_MODEL,
        "backend": "openai",
        "personality": (
            "Articulate, balanced, strong at reasoning chains. "
            "Steelmans opposing views before committing. "
            "Warm and thorough — occasionally too diplomatic."
        ),
    },
]


# ── Hierarchy block (injected into every system prompt) ───────────────────────
HIERARCHY_BLOCK = """\
TEAM HIERARCHY — NON-NEGOTIABLE:
- LEAD (the User) is the final decision-maker. Never contradict their decisions.
  Frame all advice as input for their decision, not orders.
- BOARD (you + peers) are world-class expert advisors, not decision-makers.
  Respectfully challenge each other — the Lead deserves the real debate.
- PACE: This is a fast-paced group chat.
  Hard token cap: reply MUST be under 250 tokens.
  Prose only — no bullet lists, no numbered lists, no headers.
  No filler phrases. No greetings. Start with your insight immediately.
  Reference peers by name when reacting to their points."""


# ── Round instructions ─────────────────────────────────────────────────────────
ROUND_INSTRUCTIONS = {
    0: "ROUND 1 — Give your expert initial take. 3-4 sentences, opinionated, distinctly you. No preamble.",
    1: "ROUND 2 — React to your peers. Name them. Agree, push back, or add what they missed. 2-3 sentences.",
    2: "ROUND 3 — Synthesise. Give the Lead your clearest recommendation. 2 sentences max. Be decisive.",
    3: "ROUND 4 — One final sentence. A risk, open question, or action the Lead must not ignore.",
}


def _build_system_prompt(agent: dict, round_num: int, peer_names: list[str]) -> str:
    """Construct the full system prompt for one agent in one round."""
    peers = ", ".join(peer_names)
    round_instr = ROUND_INSTRUCTIONS.get(min(round_num, 3), ROUND_INSTRUCTIONS[1])

    if agent["backend"] == "anthropic":
        identity = (
            f"You are Claude, made by Anthropic. "
            f"Speak as yourself — genuine voice, no roleplay. "
            f"This is your real perspective."
        )
    else:
        identity = (
            f"You are {agent['name']} ({agent['role']}). "
            f"Embody your known personality and communication style."
        )

    return f"""{identity}

PERSONALITY: {agent['personality']}

{HIERARCHY_BLOCK}

YOUR PEERS ON THIS BOARD: {peers}
Engage with their points by name. Productive disagreement is encouraged.

{round_instr}

The Lead is watching. Make every word count."""


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
    """Call Google Gemini API."""
    api_key = st.session_state.get("gemini_key", "")
    if not api_key:
        raise ValueError("Gemini API key not set.")
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(
        model_name=agent["model"],
        system_instruction=system,
    )
    # Convert conversation to Gemini format
    gemini_history = []
    for msg in conversation[:-1]:   # all but last
        role = "user" if msg["role"] == "user" else "model"
        gemini_history.append({"role": role, "parts": [msg["content"]]})
    chat = model.start_chat(history=gemini_history)
    response = chat.send_message(
        conversation[-1]["content"],
        generation_config=genai.GenerationConfig(max_output_tokens=300),
    )
    return response.text.strip()


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
      [{"role": "user"|"assistant", "content": "..."}]
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
