# 📝 NCEA Essay Feedback Tool

> AI-powered Excellence-level feedback on NCEA Level 2 English literary analysis essays.

🚀 **[Live demo](https://essay-feedback-eru.streamlit.app/)** — try it now

<img width="944" height="433" alt="image" src="https://github.com/user-attachments/assets/86ccec79-42d8-4600-9a6c-e3143dc2de38" />


## What it does

Paste your literary analysis essay along with the source text (story, poem, article you're analysing). The tool sends it to Google's Gemini AI with a prompt tuned for NCEA Level 2 English **Excellence criteria**, and returns structured feedback in 4 sections:

- **Strengths** — what's working
- **Weaknesses** — the biggest gaps holding you back from Excellence
- **Specific improvements** — concrete rewrites you can do tonight
- **Predicted NCEA grade** — Not Achieved / Achieved / Merit / Excellence

**Built-in safeguard:** the AI is instructed to only quote from the source text you provide — it won't fabricate quotes or invent evidence.

## How to use

1. Open the [live app](https://essay-feedback-eru.streamlit.app/)
2. Paste or upload your source text (left) and your essay (right)
3. Click **Get Feedback**
4. Read the feedback, rewrite your essay, run it again

Source text is optional — if you don't have one, the tool gives general writing feedback instead.

## Tech stack

- **Python** — core language
- **Streamlit** — web UI
- **Google Gemini API** (`gemini-2.5-flash-lite`) — the AI engine
- **python-dotenv** — secret management
- **python-docx** — `.docx` file upload support

## Run it yourself

```bash
git clone https://github.com/Eru-ai/essay-feedback.git
cd essay-feedback
python -m venv .venv
.\.venv\Scripts\Activate.ps1     # Windows
# source .venv/bin/activate       # Mac/Linux
pip install -r requirements.txt
echo "GEMINI_API_KEY=your_key_here" > .env
streamlit run essay_feedback_app.py
```

Get a free Gemini API key from [aistudio.google.com](https://aistudio.google.com).

## About

Built by [Eru Kawakami](https://github.com/Eru-ai), 16, NCEA Level 2 student in New Zealand. Shipped in 5 sessions of learning Python and AI from scratch.

Follow the journey: [@erukawa_ai](https://x.com/erukawa_ai)
