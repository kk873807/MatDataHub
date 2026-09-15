# MatDataHub: Computer Migration Guide (Windows & Mac)

If you are buying a new laptop or switching between a Windows PC and a Mac, you do **not** need to manually copy your project files using a USB drive! Because your code is hosted on GitHub, GitHub acts as your "cloud save."

This document is an absolute beginner's guide to perfectly recreating your MatDataHub development environment on a brand new computer.

---

## Phase 1: Install Required Software
On your new computer, download and install these four essential developer tools. (These work on both Windows and Mac).

1. **Git:** This allows your computer to talk to GitHub and download your code.
   - Download: [git-scm.com](https://git-scm.com)
   - *Mac Users:* You can also just open the Terminal and type `git`. If it's not installed, your Mac will automatically prompt you to install the "Command Line Tools."

2. **Node.js (v20+):** The engine that runs your Next.js Frontend.
   - Download: [nodejs.org](https://nodejs.org) (Choose the "LTS" version).

3. **Python (v3.10+):** The engine that runs your FastAPI Backend.
   - Download: [python.org](https://python.org)
   - *Windows Users:* **CRITICAL STEP!** During installation, you must check the box at the very bottom that says **"Add Python.exe to PATH"** before clicking Install.

4. **Visual Studio Code (VS Code):** Your code editor.
   - Download: [code.visualstudio.com](https://code.visualstudio.com)

---

## Phase 2: Download Your Code from GitHub
Now that your tools are installed, we will pull your "cloud save" down to your new computer.

1. Open **VS Code**.
2. Open a new Terminal inside VS Code (`Terminal -> New Terminal` at the top menu).
3. Navigate to where you want to save the project (e.g., your Documents folder):
   - *Windows:* `cd Documents`
   - *Mac:* `cd ~/Documents`
4. Download the code:
   ```bash
   git clone https://github.com/kk873807/MatDataHub.git
   ```
5. Open the folder in VS Code (`File -> Open Folder -> Select the MatDataHub folder`).

---

## Phase 3: The Secret Keys (`.env` file)
Because passwords and API keys are highly sensitive, Git purposefully **ignores** your `.env` file so it doesn't get published to the internet. Because of this, it did not download in Phase 2.

You must manually recreate it on your new computer:
1. In VS Code, click the "New File" icon in the root `MatDataHub` folder.
2. Name the file exactly: `.env`
3. Copy and paste your keys into it. If you don't remember them, you can securely copy them from your Render/Vercel dashboards, or from the `.env` file on your old computer:
   ```env
   DATABASE_URL=postgresql://postgres.xxxxx:password@aws-0-ap-south-1.pooler.supabase.com:6543/postgres
   GROQ_API_KEY=gsk_xxxxxxxxxxxx
   ADMIN_SECRET=your_admin_secret
   GOOGLE_CLIENT_ID=xxxxx.apps.googleusercontent.com
   GOOGLE_CLIENT_SECRET=GOCSPX-xxxxx
   FRONTEND_URL=http://localhost:3000
   ```

---

## Phase 4: Set Up the Backend
We need to create a fresh "Virtual Environment" on this new computer to hold your Python libraries.

1. Open a terminal in VS Code (ensure you are in the root `MatDataHub` folder).
2. Create the virtual environment:
   - *Windows & Mac:* `python -m venv .venv` (If `python` doesn't work on Mac, type `python3 -m venv .venv`).
3. **Activate the environment (This is different on Mac vs Windows!)**
   - *Windows:* `.venv\Scripts\Activate`
   - *Mac:* `source .venv/bin/activate`
4. Install the backend libraries:
   - *Windows & Mac:* `pip install -r requirements.txt`

---

## Phase 5: Set Up the Frontend
Now we will install the libraries required for the visual part of the app.

1. Open a terminal and go into the frontend folder:
   - `cd next-frontend`
2. Install the libraries:
   - `npm install`

---

## Phase 6: You are Ready!
Your new computer is now completely set up and identical to your old one. You can test it by starting both servers just like you normally do:

**Start the Backend (Terminal 1):**
- *Windows:* `.venv\Scripts\Activate`
- *Mac:* `source .venv/bin/activate`
- Run: `uvicorn app.main:app --reload --port 8000`

**Start the Frontend (Terminal 2):**
- Run: `cd next-frontend`
- Run: `npm run dev`

Open your browser to `http://localhost:3000` and MatDataHub will be running smoothly on your brand new machine!
