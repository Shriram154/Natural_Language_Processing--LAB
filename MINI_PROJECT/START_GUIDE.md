# Code Review Chatbot - Quick Start Guide

Follow these simple steps to run the application locally on your machine.

---

## 1. Start the Backend Server

You must start the backend from the **root project folder** so it can find the virtual environment and all the packages.

1. Open a new terminal in `D:\PROJECTS\CODE_REVIEW_CHATBOT`
2. Activate the virtual environment:
   ```powershell
   .venv\Scripts\activate
   ```
3. Start the FastAPI server:
   ```powershell
   python -m uvicorn backend.main:app --reload
   ```
*(The backend will now be running at `http://127.0.0.1:8000`)*

---

## 2. Start the Frontend Application

Open a **second** terminal window to run the React frontend.

1. Open a new terminal in `D:\PROJECTS\CODE_REVIEW_CHATBOT`
2. Navigate into the frontend folder:
   ```powershell
   cd frontend
   ```
3. Start the Vite development server:
   ```powershell
   npm run dev
   ```
*(The frontend will now be running at `http://localhost:5173`)*

---

## 3. Login / Usage Instructions

1. Open your browser and go to `http://localhost:5173`
2. Click **Sign Up** to create a new account.
3. Because we added an **auto-login feature**, as soon as you sign up, you will be instantly logged into the dashboard! 

**(Optional) Test Credentials you can use:**
- **Email:** `test@gmail.com`
- **Username:** `test`
- **Password:** `password123` 
*(Or you can just create a brand new account and it will work perfectly).*
