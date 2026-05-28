# ✺ AI Advisory Board
### Claude · Gemini · ChatGPT — Three real AIs, one group chat

You are the **Lead** (final decision-maker). Three real AI models debate your questions — each calling its own actual API.

| | Agent | Real Model | API |
|--|-------|-----------|-----|
| ✺ | Claude | claude-haiku-3-5-20251001 | Anthropic |
| ✦ | Gemini | gemini-1.5-flash | Google AI (free tier) |
| ◈ | ChatGPT | gpt-4o-mini | OpenAI |

---

## 🔑 Get your API keys (all free to start)

| Service | URL | Free tier |
|---------|-----|-----------|
| Anthropic | console.anthropic.com | Pay-as-you-go (~$0.001/msg) |
| Google Gemini | aistudio.google.com | Free — 15 req/min |
| OpenAI | platform.openai.com | $5 credit on new accounts |

---

## ☁️ Deploy to Streamlit Cloud

```bash
# 1. Push to GitHub
git init && git add . && git commit -m "AI Advisory Board"
gh repo create ai-advisory-board --public --push

# 2. Go to share.streamlit.io → New app → select repo → app.py
# 3. Settings → Secrets → paste:
```

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
GEMINI_API_KEY    = "AIza..."
OPENAI_API_KEY    = "sk-proj-..."
```

---

## 💻 Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
# Enter keys in the sidebar at runtime
```

---

## 📁 Files

```
├── app.py                  # Streamlit UI + discussion engine
├── agents.py               # Real API routing per model
├── requirements.txt        # anthropic + google-generativeai + openai
└── .streamlit/
    ├── secrets.toml        # API keys (never commit this)
    └── config.toml         # Dark theme
```

---

## ⚖️ Team hierarchy (enforced in every prompt)

- 👤 **Lead** (you) — final decision-maker, never overridden
- 🤖 **Board** — real AI advisors, ≤250 tokens per reply, prose only
