# MatDataHub: Absolute Beginner Setup Guide

Welcome to **MatDataHub**! If you are an absolute beginner, this document is your complete roadmap. It will teach you how the app works, how to set it up from scratch on your own computer, and how to push it to the live internet.

---

## 1. How the App Works (The Big Picture)

Modern web apps are split into three pieces. MatDataHub uses this exact structure:

1. **The Database (Memory):** Where data is stored.
   - **Technology:** PostgreSQL (hosted on a service called Supabase).
   - **What it does:** Remembers user accounts, material properties, and saved projects.
2. **The Backend (The Brain):** Processes logic, math, and talks to the database.
   - **Technology:** Python & FastAPI.
   - **Where it lives:** The `app/` folder.
   - **Where it's hosted:** Render.com
3. **The Frontend (The Face):** The buttons, menus, and pages the user sees.
   - **Technology:** React & Next.js (using Tailwind CSS for styling).
   - **Where it lives:** The `next-frontend/` folder.
   - **Where it's hosted:** Vercel.com

---

## 2. Prerequisites (What you need installed)

Before you can build or run the app, you need to download and install these four tools on your Windows computer:

1. **Node.js (v20 or higher):** Runs the frontend. Download from [nodejs.org](https://nodejs.org).
2. **Python (v3.10 or higher):** Runs the backend. Download from [python.org](https://python.org) (Make sure to check "Add Python to PATH" during installation).
3. **Git:** Downloads the code from GitHub. Download from [git-scm.com](https://git-scm.com).
4. **VS Code:** The text editor we use to write code. Download from [code.visualstudio.com](https://code.visualstudio.com).

---

## 3. Setting Up the Code on Your Computer

### Step 1: Download the Code
Open your terminal (PowerShell) and type:
```bash
cd C:\Users\KISHAN\Documents
git clone https://github.com/kk873807/MatDataHub.git
cd MatDataHub
```

### Step 2: Set Up the Backend (Python)
The backend needs a "Virtual Environment" (an isolated box) so its dependencies don't mess up your computer.
```bash
# 1. Create the virtual environment
python -m venv .venv

# 2. Activate it (You must do this every time you open a new terminal!)
.venv\Scripts\Activate

# 3. Install the required Python libraries
pip install -r requirements.txt
```

### Step 3: Set Up the Frontend (Next.js)
The frontend needs its own libraries (NPM packages).
```bash
# 1. Go into the frontend folder
cd next-frontend

# 2. Install the required NPM libraries
npm install
```

### Step 4: The Secret Keys (.env file)
Create a file named `.env` in the root `MatDataHub/` folder. This file holds your database passwords and API keys. **Never share this file or upload it to GitHub.**
```env
DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
GROQ_API_KEY=gsk_xxxxxxxxxxxx
ADMIN_SECRET=your_admin_secret
GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
FRONTEND_URL=http://localhost:3000
```

---

## 4. Running the App Locally (Testing)

To test the app on your computer, you must run **both** the backend and the frontend at the same time in two separate terminal windows.

### Terminal 1: Start the Backend
```bash
cd C:\Users\KISHAN\Documents\MatDataHub
.venv\Scripts\Activate
uvicorn app.main:app --reload --port 8000
```
*The backend is now listening at `http://localhost:8000`*

### Terminal 2: Start the Frontend
```bash
cd C:\Users\KISHAN\Documents\MatDataHub\next-frontend
npm run dev
```
*The frontend is now visible at `http://localhost:3000`*

Open Google Chrome and go to `http://localhost:3000` to see your app!

---

## 5. How to Deploy to the Internet

MatDataHub is set up with **Continuous Deployment**. This means the moment you upload code to GitHub, it automatically updates the live website.

### Step 1: Check for Errors
Before uploading, always build the frontend to catch typos:
```bash
cd next-frontend
npm run build
```
If you see a green checkmark (`✓ Compiled successfully`), you are safe to proceed.

### Step 2: Upload to GitHub
```bash
git add .
git commit -m "Added a new feature"
git push origin main
```

### Step 3: Watch it go Live
1. **Frontend:** Vercel automatically detects the push and deploys the frontend in ~60 seconds.
2. **Backend:** Render automatically detects the push and deploys the backend in ~3 minutes.

You are now a full-stack developer capable of running MatDataHub from scratch!
