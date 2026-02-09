# 🧠 AI Agent-Based Educational Content Generator

An interactive AI system that uses **two agents** — a Generator and a Reviewer — to create and validate educational content for school students.

Built as part of an **Agent-Based AI Assessment** using **Groq LLM** and **Streamlit**.

---

## ✨ What this project does

This app simulates a simple but realistic **agent pipeline**:


- The **Generator Agent** creates explanations and MCQs for a given grade and topic  
- The **Reviewer Agent** evaluates the content for clarity, correctness, and age suitability  
- If issues are found, the Generator runs **once more** using reviewer feedback  

Everything is visible and interactive in the UI.

---

## 🚀 Live Demo Flow (Interactive)


⬇️  
🧠 Generated Content  
🔍 Reviewer Feedback  
♻️ Refined Output (only if needed)

---

## 📦 Tech Stack

- **Python**
- **Streamlit** – UI
- **Groq LLM** – Content generation & review
- **Pydantic** – Structured outputs (JSON safety)

No LangChain. No heavy frameworks.  
Just clean, explainable agent logic.

---

## 🧠 Agent Design

### 🟦 Generator Agent
- Input: `grade`, `topic`, optional `feedback`
- Output:
```json
{
  "explanation": "...",
  "mcqs": [
    {
      "question": "...",
      "options": ["A", "B", "C", "D"],
      "answer": "A"
    }
  ]
}

▶️ How to Run Locally
1️⃣ Clone the repo
git clone https://github.com/your-username/ai-edu-agent.git
cd ai-edu-agent

2️⃣ Install dependencies
pip install -r requirements.txt

3️⃣ Run the app
streamlit run app.py
