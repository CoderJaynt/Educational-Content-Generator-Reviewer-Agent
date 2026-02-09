import streamlit as st
import json
from groq import Groq
from pydantic import BaseModel
from typing import List

st.set_page_config(page_title="AI Education Agent")

st.title("AI Educational Content Generator")
st.subheader("-- By Jayant Yadav")
st.write("Generator and Reviewer agents working together")

# Sidebar for API key
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_..."
)

if not api_key:
    st.sidebar.warning("Enter your Groq API key to continue")
    st.stop()

llm = Groq(api_key=api_key)
MODEL_NAME = "llama-3.1-8b-instant"


class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str


class GeneratorOutput(BaseModel):
    explanation: str
    mcqs: List[MCQ]


class ReviewerOutput(BaseModel):
    status: str
    feedback: List[str]


GENERATOR_PROMPT = """
Create educational content for a student.

Grade: {grade}
Topic: {topic}

{feedback}

Return only valid JSON:
{{
  "explanation": "string",
  "mcqs": [
    {{
      "question": "string",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }}
  ]
}}
"""

REVIEWER_PROMPT = """
Review the following content for clarity, correctness, and age suitability.

Content:
{content}

Return only valid JSON:
{{
  "status": "pass" or "fail",
  "feedback": ["string"]
}}
"""


def generator_agent(grade, topic, feedback=None):
    fb = ""
    if feedback:
        fb = "Fix the following issues:\n" + ", ".join(feedback)

    prompt = GENERATOR_PROMPT.format(
        grade=grade,
        topic=topic,
        feedback=fb
    )

    response = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return GeneratorOutput(**json.loads(response.choices[0].message.content))


def reviewer_agent(content):
    prompt = REVIEWER_PROMPT.format(content=content.json())

    response = llm.chat.completions.create(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        response_format={"type": "json_object"}
    )

    return ReviewerOutput(**json.loads(response.choices[0].message.content))


def run_pipeline(grade, topic):
    generated = generator_agent(grade, topic)
    review = reviewer_agent(generated)

    refined = None
    if review.status == "fail":
        refined = generator_agent(
            grade, topic, feedback=review.feedback
        )

    return generated, review, refined


grade = st.selectbox("Grade", [1, 2, 3, 4, 5,6,7,8,9,10,11,12])
topic = st.text_input("Topic", placeholder="Types of angles")

if st.button("Generate"):
    if not topic:
        st.warning("Please enter a topic")
    else:
        with st.spinner("Generating content..."):
            gen, review, refined = run_pipeline(grade, topic)

        st.subheader("Generated Content")
        st.write(gen.explanation)

        for i, q in enumerate(gen.mcqs, 1):
            st.write(f"Q{i}. {q.question}")
            for opt in q.options:
                st.write(f"- {opt}")
            st.write(f"Answer: {q.answer}")

        st.subheader("Reviewer Result")
        st.write("Status:", review.status)

        if review.feedback:
            for f in review.feedback:
                st.write("-", f)
        else:
            st.write("No issues found")

        if refined:
            st.subheader("Refined Content")
            st.write(refined.explanation)
