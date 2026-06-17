"""
NCEA Level 2 English - Essay Feedback (Web App version)
Run with: streamlit run essay_feedback_app.py
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
import streamlit as st

# --- Config ---
MODEL_NAME = "gemini-2.5-flash-lite"

# --- Page setup ---
st.set_page_config(
    page_title="Essay Feedback",
    page_icon="📝",
    layout="wide",
)

# --- Title ---
st.title("📝 NCEA Essay Feedback Tool")
st.caption("Paste your source text and essay below. Get Excellence-level feedback in seconds.")

# --- API key check ---
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    st.error("No GEMINI_API_KEY found in .env file. Add one and refresh this page.")
    st.stop()
genai.configure(api_key=api_key)

# --- Input area ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Source Text")
    source = st.text_area(
        "The text you're analysing (story, poem, article...)",
        height=300,
        label_visibility="collapsed",
        placeholder="Paste the story / poem / article you are analysing here..."
    )
with col2:
    st.subheader("Your Essay")
    essay = st.text_area(
        "Your literary analysis essay",
        height=300,
        label_visibility="collapsed",
        placeholder="Paste your essay here..."
    )

# --- Generate feedback ---
if st.button("Get Feedback", type="primary", use_container_width=True):
    if not source.strip() or not essay.strip():
        st.warning("Please paste both the source text and your essay.")
    else:
        with st.spinner("Asking Gemini for feedback..."):
            prompt = f"""You are an experienced NCEA Level 2 English teacher in New Zealand marking a literary analysis essay.

You will be given:
1. A SOURCE TEXT — the text the student is analysing
2. The student's ESSAY — their analysis of that source text

CRITICAL RULES:
- Any quotes you use in your feedback MUST come word-for-word from the SOURCE TEXT below.
- NEVER invent, paraphrase as a quote, or fabricate quotes. If you can't find a real quote to support a point, do not invent one — make the point without a quote instead.
- Refer to the student as "you" in your feedback.
- Aim your feedback at helping the student reach the NCEA Level 2 Excellence standard, which requires perceptive, well-developed analysis with specific evidence and explanation of effects on the reader.

Your feedback must have EXACTLY these four sections, in this order, using these exact headers:

## STRENGTHS
What's working well in the essay. Be specific.

## WEAKNESSES
The biggest issues holding the essay back from Excellence. Be specific and honest.

## SPECIFIC IMPROVEMENTS
3-5 concrete, actionable changes the student can make. Each one should reference a specific part of the essay or a missing element.

## PREDICTED NCEA GRADE
One of: Not Achieved / Achieved / Merit / Excellence
Then 1-2 sentences explaining the prediction.

--- SOURCE TEXT ---
{source}

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