"""
NCEA Level 2 English - Essay Feedback (Web App version, v2)
Run with: streamlit run essay_feedback_app.py
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st
from docx import Document

# --- Config ---
MODEL_NAME = "gemini-2.5-flash-lite"

# --- Page setup ---
st.set_page_config(
    page_title="NCEA Essay Feedback",
    page_icon="📝",
    layout="wide",
)

# --- Title and description ---
st.title("📝 NCEA Essay Feedback Tool")
st.markdown(
    "Get instant **NCEA Level 2 English Excellence-level feedback** on your literary analysis essays. "
    "Predicts your grade and tells you exactly what to improve."
)

with st.expander("ℹ️  How to use this tool"):
    st.markdown(
        """
**Steps:**
1. **Source text** (left column): paste or upload the text you're analysing — story, poem, article, extract.
2. **Your essay** (right column): paste or upload your literary analysis essay.
3. Hit **Get Feedback** and wait a few seconds.

**How to use the feedback you get:**
- **Strengths** — keep doing these in your next draft.
- **Weaknesses** — the gap between you and Excellence. Focus your effort here.
- **Specific improvements** — use as a rewrite checklist.
- **Predicted grade** — your starting point, not your ceiling. Rewrite and run again.

**Note:** the tool only quotes from the source text you paste/upload — it won't make up quotes.
"""
    )

# --- API key check ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("No GEMINI_API_KEY found. Set it in your .env file or in Streamlit secrets.")
    st.stop()
genai.configure(api_key=api_key)


# --- Helper: read uploaded file ---
def read_uploaded_file(uploaded_file):
    """Read content from a .txt or .docx file."""
    if uploaded_file.name.lower().endswith(".docx"):
        doc = Document(uploaded_file)
        return "\n".join(p.text for p in doc.paragraphs)
    return uploaded_file.getvalue().decode("utf-8")


# --- Input area ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Source Text")
    source_file = st.file_uploader(
        "Upload .txt or .docx",
        type=["txt", "docx"],
        key="source_upload",
    )
    source_text_area = st.text_area(
        "Or paste here",
        height=250,
        key="source_text",
        placeholder="Paste the story, poem, or article you are analysing...",
    )
    source = read_uploaded_file(source_file) if source_file else source_text_area

with col2:
    st.subheader("Your Essay")
    essay_file = st.file_uploader(
        "Upload .txt or .docx",
        type=["txt", "docx"],
        key="essay_upload",
    )
    essay_text_area = st.text_area(
        "Or paste here",
        height=250,
        key="essay_text",
        placeholder="Paste your literary analysis essay...",
    )
    essay = read_uploaded_file(essay_file) if essay_file else essay_text_area

# --- Generate feedback ---
if st.button("Get Feedback", type="primary", use_container_width=True):
    if not essay.strip():
        st.warning("Please provide your essay (paste or upload).")
    else:
        has_source = bool(source.strip())
        if not has_source:
            st.info(
                "ℹ️ No source text provided — feedback will focus on general writing quality. "
                "For full Excellence-level analysis with quote-checking, add the source text too."
            )

        with st.spinner("Asking Gemini for feedback..."):
            if has_source:
                prompt = f"""You are an experienced NCEA Level 2 English teacher in New Zealand marking a literary analysis essay.

You will be given:
1. A SOURCE TEXT — the text the student is analysing
2. The student's ESSAY — their analysis of that source text

CRITICAL RULES:
- Any quotes you use in your feedback MUST come word-for-word from the SOURCE TEXT below.
- NEVER invent, paraphrase as a quote, or fabricate quotes. If you can't find a real quote to support a point, do not invent one — make the point without a quote instead.
- Refer to the student as "you" in your feedback.
- Aim your feedback at helping the student reach the NCEA Level 2 Excellence standard.

Your feedback must have EXACTLY these four sections:

## STRENGTHS
What's working well. Be specific.

## WEAKNESSES
The biggest issues holding the essay back from Excellence.

## SPECIFIC IMPROVEMENTS
3-5 concrete, actionable changes — reference specific parts of the essay.

## PREDICTED NCEA GRADE
One of: Not Achieved / Achieved / Merit / Excellence
Then 1-2 sentences explaining the prediction.

--- SOURCE TEXT ---
{source}

--- STUDENT ESSAY ---
{essay}

Now write the feedback."""
            else:
                prompt = f"""You are an experienced NCEA Level 2 English teacher in New Zealand marking a literary analysis essay.

The student has provided their ESSAY but no source text. You CANNOT verify whether any quotes in the essay are accurate — acknowledge this in your feedback and encourage them to double-check quotes themselves. Focus on what you CAN judge: structure, argument development, vocabulary, depth of analysis, sentence-level craft.

Refer to the student as "you" and aim feedback at helping them reach NCEA Level 2 Excellence.

Your feedback must have EXACTLY these four sections:

## STRENGTHS
What's working well. Be specific.

## WEAKNESSES
The biggest issues holding the essay back from Excellence.

## SPECIFIC IMPROVEMENTS
3-5 concrete, actionable changes — reference specific parts of the essay.

## PREDICTED NCEA GRADE
One of: Not Achieved / Achieved / Merit / Excellence
Note that without the source text this prediction is tentative.

--- STUDENT ESSAY ---
{essay}

Now write the feedback."""

            model = genai.GenerativeModel(MODEL_NAME)
            response = model.generate_content(prompt)

        st.divider()
        st.markdown(response.text)

        st.download_button(
            label="📥 Download feedback as .txt",
            data=response.text,
            file_name="feedback_output.txt",
            mime="text/plain",
        )