"""
NCEA Level 2 English - Essay Feedback Tool
Reads your essay and source text, asks Gemini for Excellence-level feedback.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# --- Config ---
ESSAY_FILE = "essay.txt"
SOURCE_FILE = "source.txt"
OUTPUT_FILE = "feedback_output.txt"
MODEL_NAME = "gemini-2.5-flash-lite"


def load_text_file(filename):
    """Read a text file. Stop the program if it's missing or empty."""
    if not os.path.exists(filename):
        print(f"ERROR: {filename} not found. Create it and paste your text in.")
        exit()

    with open(filename, "r", encoding="utf-8") as file:
        text = file.read().strip()

    if not text:
        print(f"ERROR: {filename} is empty. Paste your text in and try again.")
        exit()

    return text


def build_prompt(essay, source):
    """Build the prompt sent to Gemini."""
    return f"""You are an experienced NCEA Level 2 English teacher in New Zealand marking a literary analysis essay.

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


def get_feedback(prompt):
    """Send the prompt to Gemini and return the response text."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("ERROR: No GEMINI_API_KEY found in .env file.")
        exit()

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel(MODEL_NAME)

    print("Asking Gemini for feedback... (this takes a few seconds)\n")
    response = model.generate_content(prompt)
    return response.text


def save_feedback(feedback):
    """Save the feedback to a text file."""
    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        file.write(feedback)


def main():
    essay = load_text_file(ESSAY_FILE)
    source = load_text_file(SOURCE_FILE)
    prompt = build_prompt(essay, source)
    feedback = get_feedback(prompt)

    print("=" * 60)
    print("  ESSAY FEEDBACK")
    print("=" * 60)
    print(feedback)
    print("=" * 60)

    save_feedback(feedback)
    print(f"\nFeedback saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()