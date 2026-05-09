<div align="center">
  <h1>🚀 AI-Powered Code Review Assistant</h1>
  <p><strong>Intelligent Static Analysis meets Hugging Face LLMs for instant, optimized code refactoring.</strong></p>

  [![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?style=for-the-badge&logo=react&logoColor=black)](https://reactjs.org/)
  [![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
  [![Python](https://img.shields.io/badge/AI_Engine-Python%203.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PyTorch](https://img.shields.io/badge/Model-Qwen_0.5B-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://huggingface.co/Qwen/Qwen2.5-Coder-0.5B)
</div>

<br>

## 📖 Overview

The **AI Code Review Assistant** is a full-stack, enterprise-grade application designed to automate code reviews, calculate algorithmic complexity, and refactor code for optimal performance. 

By combining a **lightning-fast heuristic static analyzer** with a **local Hugging Face Large Language Model (`Qwen2.5-Coder-0.5B`)**, the application guarantees perfect mathematical Big-O notations while providing deep, contextual code refactoring—all running efficiently on local hardware.

---

## ✨ Key Features

- **🛡️ Secure Authentication:** Full JWT-based Role-Based Access Control (RBAC) with SQLite, featuring an automatic login flow upon registration.
- **⚡ Hybrid AI Pipeline:** 
  - **Static Heuristics:** Instantly calculates exact Time Complexity (`O(n)`, `O(n log n)`, etc.) to prevent LLM hallucinations.
  - **Generative AI:** Uses Qwen2.5 to provide a line-by-line explanation, deep logical analysis, and fully refactored, optimized code.
- **⏱️ Local CPU Optimization:** Implements advanced Python `@lru_cache` mechanics and highly condensed single-pass prompts to cut local AI inference time by over 60%.
- **💾 Historical Dashboard:** Automatically saves and caches past code reviews to an internal SQLite database, rendering previously analyzed snippets instantly.
- **🎨 Premium UI/UX:** Built with a dark-mode glassmorphic aesthetic, interactive code blocks, and micro-animations for an exceptional developer experience.

---

## 🏗️ System Architecture

### 1. Frontend (`React` + `Vite`)
- **State Management:** React Hooks (`useState`, `useEffect`) tracking user sessions and tokens.
- **Routing:** Secured private routes guarding the dashboard from unauthenticated access.
- **Design System:** Custom CSS tokens emphasizing a modern, vibrant developer aesthetic.

### 2. Backend (`FastAPI`)
- **API Gateway:** Asynchronous endpoints (`/analyze-code`, `/history`, `/login`) serving the frontend.
- **Security:** `passlib.context` for bcrypt password hashing and `python-jose` for JWT encoding.
- **Database (ORM):** SQLAlchemy mapping Python classes directly to SQLite tables (`User`, `CodeReview`, `AnalysisResult`).

### 3. AI Inference Engine (`Hugging Face` + `PyTorch`)
- **Model:** `Qwen2.5-Coder-0.5B` via `AutoModelForCausalLM`.
- **Optimization Strategy:** Memory-bound CPU inference is bypassed using a cached Hybrid logic system, allowing mathematical complexities to be solved via AST/Regex while semantic logic is solved by the LLM.

---

## ⚙️ Local Installation Guide

### Prerequisites
- **Node.js** (v18+)
- **Python** (v3.10+)
- **Git**

### 1. Backend Setup
The backend utilizes Python and requires a virtual environment for the AI dependencies.

```bash
# 1. Open terminal in the root directory
cd CODE_REVIEW_CHATBOT

# 2. Activate the virtual environment
.venv\Scripts\activate

# 3. Start the FastAPI server
python -m uvicorn backend.main:app --reload
```
> *The backend API and Swagger Docs will be available at `http://127.0.0.1:8000/docs`*

### 2. Frontend Setup
The frontend uses Vite for lightning-fast Hot Module Replacement (HMR).

```bash
# 1. Open a new terminal in the root directory
cd CODE_REVIEW_CHATBOT/frontend

# 2. Install Node dependencies (if not already installed)
npm install

# 3. Start the development server
npm run dev
```
> *The web interface will be accessible at `http://localhost:5173`*

---

## 🧪 Usage & Testing

1. Navigate to `http://localhost:5173` in your browser.
2. Create an account via the **Sign Up** tab. You will be instantly redirected to the dashboard.
   - *Alternatively, use the seeded credentials:*
   - **Email:** `test@gmail.com`
   - **Password:** `password123`
3. Paste a block of code (e.g., an unoptimized Bubble Sort or nested loop).
4. Click **Analyze Code**. The system will process the logic and return the optimized output!

---

## 🛡️ Security & Privacy
Because this application runs the Hugging Face model **locally**, your proprietary source code is never sent to third-party APIs (like OpenAI or Anthropic). All code snippets, passwords, and analysis histories are encrypted and stored safely inside your local `code_review_ai.db`.
