"""
Thinking Hats — Claude · Gemini · ChatGPT
Three real AIs, one group chat. You are the Lead.

THOS v1.0 — Thinking Hats Operating System
DEC / HYP / DISC logging active.

Deploy: share.streamlit.io
Local:  streamlit run app.py
"""

import os, time, json
import streamlit as st
from agents import AGENTS, call_agent

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Thinking Hats",
    page_icon="✺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
section[data-testid="stSidebar"] { background: #0d1117; border-right: 1px solid #1e2433; }
section[data-testid="stSidebar"] * { color: #c9d1d9 !important; }
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 { color: #fff !important; font-family: 'JetBrains Mono' !important; }
#MainMenu, footer, header { visibility: hidden; }
.main .block-container { padding-top: 1rem; max-width: 860px; }
.ai-label { font-family: 'JetBrains Mono', monospace; font-size: 11px; font-weight: 600;
            text-transform: uppercase; letter-spacing: 1px; margin-bottom: 4px; }
.brand-card { background: #0d1117; border: 1px solid #1e2433; border-radius: 14px;
              padding: 16px; text-align: center; }
.key-ok  { color: #4ade80 !important; font-size: 11px; font-family: 'JetBrains Mono' !important; }
.key-bad { color: #f87171 !important; font-size: 11px; font-family: 'JetBrains Mono' !important; }
.thos-log-entry { background: #0d1117; border: 1px solid #1e2433; border-radius: 8px;
                  padding: 10px 14px; font-size: 12px; font-family: 'JetBrains Mono';
                  margin-bottom: 8px; }
</style>
""", unsafe_allow_html=True)

BRAND_COLORS = {a["name"]: a["color"] for a in AGENTS}

# ── Round labels aligned with THOS-001 ────────────────────────────────────────
ROUND_LABELS = {
    0: "stating position…",
    1: "challenging…",
    2: "revising or defending…",
    3: "synthesising…",
}

# ── Resolve keys: Streamlit secrets → env → session ───────────────────────────
def _secret(name: str) -> str:
    try: return st.secrets[name]
    except: return os.environ.get(name, "")

for key_name, session_key in [
    ("ANTHROPIC_API_KEY", "anthropic_key"),
    ("GEMINI_API_KEY",    "gemini_key"),
    ("OPENAI_API_KEY",    "openai_key"),
]:
    if session_key not in st.session_state:
        st.session_state[session_key] = _secret(key_name)

# ── Other session defaults ─────────────────────────────────────────────────────
for k, v in {
    "messages":      [],
    "active_agents": [a["name"] for a in AGENTS],
    "rounds":        2,
    "thread":        "AI Roundtable",
    "pending":       None,
    "thos_log":      [],          # DEC / HYP / DISC entries
    "thos_counter":  {"DEC": 0, "HYP": 0, "DISC": 0},
    "show_log":      False,
}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── THOS log helpers ───────────────────────────────────────────────────────────
def _log_entry(entry_type: str, content: str, context: str = ""):
    """Add a DEC / HYP / DISC entry to the in-session THOS log."""
    st.session_state.thos_counter[entry_type] += 1
    n = st.session_state.thos_counter[entry_type]
    entry = {
        "id":      f"{entry_type}-{n:03d}",
        "type":    entry_type,
        "content": content,
        "context": context,
        "thread":  st.session_state.thread,
        "status":  "Open" if entry_type in ("HYP", "DISC") else "Decided",
    }
    st.session_state.thos_log.append(entry)
    return entry["id"]

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## ✺ Thinking Hats")
    st.markdown("*Claude · Gemini · ChatGPT*")
    st.markdown("---")

    # ── API keys ───────────────────────────────────────────────────────────────
    st.markdown("### 🔑 API Keys")
    for label, session_key, placeholder, help_url in [
        ("Anthropic (Claude)", "anthropic_key", "sk-ant-...",  "console.anthropic.com"),
        ("Google (Gemini)",    "gemini_key",    "AIza...",     "aistudio.google.com"),
        ("OpenAI (ChatGPT)",   "openai_key",    "sk-proj-...", "platform.openai.com"),
    ]:
        val = st.text_input(
            label, value=st.session_state[session_key],
            type="password", placeholder=placeholder,
            help=f"Get your key at {help_url}",
            key=f"input_{session_key}",
        )
        if val:
            st.session_state[session_key] = val
        status = "✔ set" if st.session_state[session_key] else "✘ missing"
        css    = "key-ok" if st.session_state[session_key] else "key-bad"
        st.markdown(f"<span class='{css}'>{status}</span>", unsafe_allow_html=True)

    st.markdown("---")

    # ── Active agents ──────────────────────────────────────────────────────────
    st.markdown("### 🤖 Active AIs")
    selected = []
    for agent in AGENTS:
        if st.checkbox(
            f"**{agent['emoji']} {agent['name']}** — *{agent['role']}*",
            value=agent["name"] in st.session_state.active_agents,
            key=f"chk_{agent['name']}",
        ):
            selected.append(agent["name"])
    st.session_state.active_agents = selected

    st.markdown("---")

    # ── Settings ───────────────────────────────────────────────────────────────
    st.markdown("### ⚙️ Settings")
    st.session_state.rounds = st.slider(
        "Discussion rounds", 1, 4, st.session_state.rounds,
        help="1 = positions only. 2 = challenge. 3 = revise. 4 = synthesise.",
    )
    st.session_state.thread = st.text_input("Thread name", value=st.session_state.thread)

    st.markdown("---")

    # ── Quick topics ───────────────────────────────────────────────────────────
    st.markdown("### 💡 Quick Topics")
    for topic in [
        "Which AI company is winning the race right now?",
        "Will AI replace software engineers in 5 years?",
        "Should I launch my startup with app or web first?",
        "What are the biggest risks of AGI?",
        "How should a small business adopt AI today?",
        "Is RAG dead now that context windows are huge?",
    ]:
        label = f"▸ {topic[:38]}…" if len(topic) > 40 else f"▸ {topic}"
        if st.button(label, key=f"qt_{topic[:16]}", use_container_width=True):
            st.session_state.pending = topic

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thos_log = []
            st.session_state.thos_counter = {"DEC": 0, "HYP": 0, "DISC": 0}
            st.rerun()
    with c2:
        if st.session_state.messages:
            export_data = {
                "messages": st.session_state.messages,
                "thos_log": st.session_state.thos_log,
            }
            st.download_button(
                "📥 Export", use_container_width=True,
                data=json.dumps(export_data, indent=2),
                file_name="board_session.json", mime="application/json",
            )

    st.markdown("---")

    # ── THOS log toggle ────────────────────────────────────────────────────────
    log_count = len(st.session_state.thos_log)
    log_label = f"📋 THOS Log ({log_count})" if log_count else "📋 THOS Log"
    st.session_state.show_log = st.toggle(log_label, value=st.session_state.show_log)

    st.markdown("---")

    # ── Hierarchy legend ───────────────────────────────────────────────────────
    st.markdown("### ⚖️ Hierarchy")
    st.markdown(
        "<div style='font-size:11px;line-height:1.8;color:#6e7681;font-family:JetBrains Mono;'>"
        "<span style='color:#f59e0b;font-weight:700;'>👤 YOU = LEAD</span><br>"
        "Final decision-maker. Board advises, you decide.<br><br>"
        "<span style='color:#c9d1d9;font-weight:600;'>🤖 AIs = BOARD</span><br>"
        "Real models. Genuine debate. THOS-001 enforced.<br><br>"
        "<span style='color:#3d4b5c;'>≤250 tokens · prose only · no polite agreement</span>"
        "</div>", unsafe_allow_html=True,
    )
    st.markdown("---")

    n = len(st.session_state.active_agents)
    keys_set = sum(1 for k in ["anthropic_key","gemini_key","openai_key"] if st.session_state.get(k))
    st.markdown(
        f"<div style='font-size:11px;color:#6e7681;font-family:JetBrains Mono;'>"
        f"🟢 {n} AI{'s' if n!=1 else ''} active &nbsp;·&nbsp; "
        f"🔑 {keys_set}/3 keys &nbsp;·&nbsp; "
        f"{len(st.session_state.messages)} messages</div>",
        unsafe_allow_html=True,
    )

# ── Header ─────────────────────────────────────────────────────────────────────
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown(
        f"<h2 style='font-family:JetBrains Mono;font-size:1.05rem;color:#c9d1d9;'>"
        f"# {st.session_state.thread}</h2>", unsafe_allow_html=True,
    )
with c2:
    pills = " · ".join(
        "<span style='color:{}'>{}</span>".format(BRAND_COLORS.get(n, "#fff"), n)
        for n in st.session_state.active_agents
    )
    st.markdown(
        f"<div style='background:#0d1117;border:1px solid #1e2433;border-radius:8px;"
        f"padding:6px 12px;font-size:11px;font-family:JetBrains Mono;text-align:right;'>"
        f"{pills}</div>", unsafe_allow_html=True,
    )

# ── THOS Log panel ─────────────────────────────────────────────────────────────
if st.session_state.show_log:
    with st.expander("📋 THOS Log — DEC / HYP / DISC", expanded=True):
        if not st.session_state.thos_log:
            st.markdown(
                "<div style='color:#3d4b5c;font-family:JetBrains Mono;font-size:12px;'>"
                "No entries yet. Use the capture buttons after a discussion.</div>",
                unsafe_allow_html=True,
            )
        else:
            for entry in reversed(st.session_state.thos_log):
                color_map = {"DEC": "#f59e0b", "HYP": "#4285F4", "DISC": "#10a37f"}
                color = color_map.get(entry["type"], "#888")
                st.markdown(
                    f"<div class='thos-log-entry' style='border-left:3px solid {color};'>"
                    f"<span style='color:{color};font-weight:700;'>{entry['id']}</span>"
                    f"<span style='color:#3d4b5c;margin-left:8px;font-size:10px;'>{entry['status']}</span>"
                    f"<br><span style='color:#c9d1d9;'>{entry['content']}</span>"
                    f"{'<br><span style=\"color:#6e7681;font-size:10px;\">Context: ' + entry['context'] + '</span>' if entry['context'] else ''}"
                    f"</div>",
                    unsafe_allow_html=True,
                )

# ── Welcome screen ─────────────────────────────────────────────────────────────
if not st.session_state.messages:
    active_list = [a for a in AGENTS if a["name"] in st.session_state.active_agents]
    st.markdown(
        "<div style='text-align:center;padding:2rem 1rem 1.5rem;color:#6e7681;'>"
        "<div style='font-size:2rem;margin-bottom:.5rem;'>✺ ✦ ◈</div>"
        "<h3 style='color:#c9d1d9;font-family:JetBrains Mono;font-size:1rem;'>"
        "Three real AIs. One conversation.</h3>"
        "<p style='font-size:13px;margin:.4rem 0;'>"
        "You are the <strong style='color:#f59e0b;'>Lead</strong>. "
        "Each AI has a debate role. THOS-001 enforced: no polite parallel answers.</p>"
        "<div style='display:inline-flex;gap:16px;margin-top:8px;font-size:11px;"
        "font-family:JetBrains Mono;background:#0d1117;border:1px solid #1e2433;"
        "border-radius:8px;padding:8px 18px;'>"
        "<span style='color:#f59e0b;'>👤 You = Lead</span>"
        "<span style='color:#3d4b5c;'>|</span>"
        "<span style='color:#cc785c;'>✺ Claude — Skeptic</span>"
        "<span style='color:#3d4b5c;'>|</span>"
        "<span style='color:#4285F4;'>✦ Gemini — Context</span>"
        "<span style='color:#3d4b5c;'>|</span>"
        "<span style='color:#10a37f;'>◈ ChatGPT — Strategy</span>"
        "</div></div>", unsafe_allow_html=True,
    )

    if active_list:
        cols = st.columns(len(active_list))
        for i, agent in enumerate(active_list):
            with cols[i]:
                color = agent["color"]
                st.markdown(
                    f"<div class='brand-card' style='border-top:3px solid {color};'>"
                    f"<div style='font-size:1.8rem;margin-bottom:6px;'>{agent['emoji']}</div>"
                    f"<div style='font-weight:600;color:{color};font-family:JetBrains Mono;"
                    f"font-size:13px;'>{agent['name']}</div>"
                    f"<div style='font-size:11px;color:#6e7681;margin:3px 0 6px;'>{agent['role']}</div>"
                    f"<div style='font-size:10px;color:#3d4b5c;font-family:JetBrains Mono;'>"
                    f"{agent.get('debate_role', agent['model'])}</div>"
                    f"</div>", unsafe_allow_html=True,
                )

# ── Helpers ────────────────────────────────────────────────────────────────────
def agent_emoji(name: str) -> str:
    for a in AGENTS:
        if a["name"] == name: return a["emoji"]
    return "🤖"

# ── Render history ─────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar="user"):
            st.markdown(
                "<span style='font-family:JetBrains Mono;font-size:10px;font-weight:700;"
                "text-transform:uppercase;letter-spacing:1px;color:#f59e0b;'>"
                "👤 Lead · Final Decision-Maker</span>", unsafe_allow_html=True,
            )
            st.markdown(msg["content"])
    else:
        name  = msg.get("agent", "")
        color = BRAND_COLORS.get(name, "#888")
        rnd   = msg.get("round", 0)
        with st.chat_message(name, avatar="assistant"):
            st.markdown(
                f"<div class='ai-label' style='color:{color};'>"
                f"{agent_emoji(name)} {name}"
                f"<span style='color:#3d4b5c;font-weight:400;margin-left:6px;'>"
                f"Round {rnd + 1} · Board Expert</span></div>", unsafe_allow_html=True,
            )
            st.markdown(msg["content"])

# ── Discussion engine ──────────────────────────────────────────────────────────
def _keys_ok(active: list) -> bool:
    key_map = {"anthropic": "anthropic_key", "gemini": "gemini_key", "openai": "openai_key"}
    missing = [
        a["name"] for a in active
        if not st.session_state.get(key_map[a["backend"]], "")
    ]
    if missing:
        st.error(f"⚠️ Missing API keys for: {', '.join(missing)}. Add them in the sidebar.")
        return False
    return True


def run_discussion(user_msg: str):
    active = [a for a in AGENTS if a["name"] in st.session_state.active_agents]
    if not active:
        st.warning("⚠️ Select at least one AI in the sidebar.")
        return
    if not _keys_ok(active):
        return

    # Save + render user message
    st.session_state.messages.append({"role": "user", "content": user_msg})
    with st.chat_message("user", avatar="user"):
        st.markdown(
            "<span style='font-family:JetBrains Mono;font-size:10px;font-weight:700;"
            "text-transform:uppercase;letter-spacing:1px;color:#f59e0b;'>"
            "👤 Lead · Final Decision-Maker</span>", unsafe_allow_html=True,
        )
        st.markdown(user_msg)

    # Hierarchy banner
    st.markdown(
        "<div style='background:#0d1117;border:1px solid #1e2433;"
        "border-left:3px solid #f59e0b;border-radius:0 6px 6px 0;"
        "padding:6px 14px;font-size:11px;font-family:JetBrains Mono;"
        "color:#6e7681;margin:4px 0 8px;'>"
        "⚖️ <strong style='color:#f59e0b;'>Lead</strong> has final say &nbsp;·&nbsp; "
        "Real AI responses below &nbsp;·&nbsp; "
        "<span style='color:#3d4b5c;'>THOS-001: build · challenge · revise · synthesise</span></div>",
        unsafe_allow_html=True,
    )

    for round_num in range(st.session_state.rounds):
        if round_num > 0:
            st.markdown(
                f"<div style='text-align:center;color:#3d4b5c;font-size:10px;"
                f"font-family:JetBrains Mono;padding:4px 0;'>── Round {round_num + 1} ──</div>",
                unsafe_allow_html=True,
            )

        for agent in active:
            color      = agent["color"]
            round_label = ROUND_LABELS.get(round_num, "debating…")

            with st.chat_message(agent["name"], avatar="assistant"):
                st.markdown(
                    f"<div class='ai-label' style='color:{color};'>"
                    f"{agent['emoji']} {agent['name']} · {agent['role']}"
                    f"<span style='color:#3d4b5c;font-weight:400;margin-left:6px;'>"
                    f"{round_label}</span></div>",
                    unsafe_allow_html=True,
                )
                placeholder = st.empty()
                placeholder.markdown("*thinking…*")

                try:
                    response = call_agent(agent, round_num, st.session_state.messages)
                    placeholder.markdown(response)
                    st.session_state.messages.append({
                        "role":    "assistant",
                        "content": response,
                        "agent":   agent["name"],
                        "round":   round_num,
                        "model":   agent["model"],
                    })

                except ValueError as e:
                    placeholder.markdown(f"*⚠️ {e}*")

                except Exception as e:
                    err = str(e).lower()
                    if "auth" in err or "api key" in err or "401" in err:
                        placeholder.markdown(f"*❌ Invalid API key for {agent['name']}.*")
                        return
                    elif "rate" in err or "429" in err:
                        placeholder.markdown("*⏳ Rate limit — waiting 10s…*")
                        time.sleep(10)
                        try:
                            response = call_agent(agent, round_num, st.session_state.messages)
                            placeholder.markdown(response)
                            st.session_state.messages.append({
                                "role": "assistant", "content": response,
                                "agent": agent["name"], "round": round_num,
                                "model": agent["model"],
                            })
                        except Exception as e2:
                            placeholder.markdown(f"*❌ {e2}*")
                    else:
                        placeholder.markdown(f"*❌ {agent['name']} error: {e}*")

            time.sleep(0.2)

    # ── Lead Decision Capture ──────────────────────────────────────────────────
    st.markdown("---")
    st.markdown(
        "<div style='font-family:JetBrains Mono;font-size:11px;color:#6e7681;"
        "margin-bottom:8px;'>📋 THOS — Capture this discussion</div>",
        unsafe_allow_html=True,
    )
    col1, col2, col3, col4 = st.columns([3, 1, 1, 1])

    with col1:
        capture_text = st.text_input(
            "Decision / Hypothesis / Discovery",
            placeholder="e.g. Launch pilot before full build",
            label_visibility="collapsed",
            key=f"capture_{len(st.session_state.messages)}",
        )
    with col2:
        if st.button("✅ DEC", help="Log as a Lead Decision", use_container_width=True,
                     key=f"dec_{len(st.session_state.messages)}"):
            if capture_text:
                entry_id = _log_entry("DEC", capture_text, context=user_msg[:80])
                st.success(f"{entry_id} logged.")
    with col3:
        if st.button("🔬 HYP", help="Log as a Hypothesis to test", use_container_width=True,
                     key=f"hyp_{len(st.session_state.messages)}"):
            if capture_text:
                entry_id = _log_entry("HYP", capture_text, context=user_msg[:80])
                st.info(f"{entry_id} logged.")
    with col4:
        if st.button("💡 DISC", help="Log as a Discovery", use_container_width=True,
                     key=f"disc_{len(st.session_state.messages)}"):
            if capture_text:
                entry_id = _log_entry("DISC", capture_text, context=user_msg[:80])
                st.info(f"{entry_id} logged.")

    st.markdown("---")


# ── Input handling ─────────────────────────────────────────────────────────────
if st.session_state.pending:
    msg = st.session_state.pending
    st.session_state.pending = None
    run_discussion(msg)
    st.rerun()

if prompt := st.chat_input(f"Message the board…"):
    run_discussion(prompt)
    st.rerun()
