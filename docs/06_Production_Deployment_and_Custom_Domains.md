# MatDataHub: Production Deployment & Custom Domains

This document explains the "magic" behind how your code actually gets onto the internet. It covers how Vercel and Render are connected to your GitHub, how to set them up from scratch if you ever create a new account, and how to attach a professional `.com` domain name in the future.

---

## 1. The CI/CD Pipeline (How Auto-Deploy Works)
Right now, when you type `git push origin main`, your website updates automatically. This is called **CI/CD** (Continuous Integration / Continuous Deployment). 

It works because Vercel (your frontend host) and Render (your backend host) are both granted permission to "listen" to your GitHub account. The moment GitHub receives new code, it sends a webhook (a digital text message) to Vercel and Render saying *"Hey, new code is here!"* They immediately download it, build it, and swap out the old live website for the new one.

---

## 2. Setting Up Vercel From Scratch (Frontend)
If you ever lose your Vercel account and need to host the frontend on a brand new account, follow these steps:

1. Go to [Vercel.com](https://vercel.com) and create an account using your GitHub login.
2. Click **"Add New Project"**.
3. Vercel will show a list of your GitHub repositories. Find `MatDataHub` and click **"Import"**.
4. **CRITICAL STEP - Configure the Project:**
   - **Framework Preset:** Next.js
   - **Root Directory:** Click "Edit" and select `next-frontend` (because your frontend is not in the root folder, it's inside `next-frontend/`).
5. **Environment Variables:**
   - Add your variables here (e.g., Name: `NEXT_PUBLIC_API_URL`, Value: `https://your-render-backend-url.onrender.com`).
6. Click **Deploy**. Vercel will now automatically build and host the frontend every time you push to GitHub!

---

## 3. Setting Up Render From Scratch (Backend)
If you ever need to set up your FastAPI backend on a new Render account:

1. Go to [Dashboard.Render.com](https://dashboard.render.com) and log in with GitHub.
2. Click **"New +"** and select **"Blueprint"** (This is the easiest way because we already wrote a `render.yaml` file that tells Render exactly how to build your app).
3. Connect your `MatDataHub` repository.
4. Render will read the `render.yaml` file in your code and automatically configure the Python environment, install `requirements.txt`, and set the start command to `python -m app.main`.
5. **Environment Variables:**
   - Go to your new Web Service on Render, click **"Environment"** on the left menu.
   - You **must** manually add all your secrets here (e.g., `DATABASE_URL`, `GROQ_API_KEY`, etc.) because they are not saved in GitHub.
6. Click **Save Changes**. Render will now automatically host your API!

---

## 4. How to Attach a Custom Domain Name (e.g., matdatahub.com)

Right now, your app lives on a free subdomain (like `matdatahub.vercel.app`). When you are ready to launch to the public, you will want a real `.com` domain.

### Step 1: Buy the Domain
Go to a domain registrar like **Namecheap**, **GoDaddy**, or **Cloudflare** and purchase your domain (e.g., `matdatahub.com`).

### Step 2: Connect it to Vercel (The Frontend)
Since the frontend is the actual website users visit, you will attach the domain to Vercel.
1. Log into Vercel and click on your MatDataHub project.
2. Go to **Settings -> Domains**.
3. Type in your new domain (e.g., `matdatahub.com`) and click **Add**.
4. Vercel will give you **DNS Records** (usually an `A Record` pointing to an IP address like `76.76.21.21` and a `CNAME Record`).

### Step 3: Update your Registrar's DNS Settings
1. Log into the website where you bought the domain (e.g., GoDaddy).
2. Find the **"DNS Management"** or **"Advanced DNS"** page for your domain.
3. Delete any default "Parked" records.
4. Add the records exactly as Vercel provided them:
   - **Type:** `A` | **Name/Host:** `@` | **Value:** `76.76.21.21`
   - **Type:** `CNAME` | **Name/Host:** `www` | **Value:** `cname.vercel-dns.com`
5. Save the changes. 

*(Note: It can take anywhere from 10 minutes to 24 hours for DNS changes to propagate globally across the internet. Vercel will automatically generate a free SSL/HTTPS certificate for you once it connects).*

### Step 4: Update the API URLs (Important!)
Once your domain is live, you must tell your Backend to allow requests from your new domain, and tell your Frontend to talk to the correct API.

1. **Update Backend CORS:** Open `app/main.py` in your code and add your new domain to the `allow_origins` list:
   ```python
   origins = [
       "http://localhost:3000",
       "https://matdatahub.vercel.app",
       "https://matdatahub.com",
       "https://www.matdatahub.com"
   ]
   ```
   *Push this change to GitHub so Render updates.*
2. **Update Frontend Environment:** If you ever attach a custom domain to your API backend on Render (e.g., `api.matdatahub.com`), you must go into Vercel's Environment Variables settings and change `NEXT_PUBLIC_API_URL` to point to the new backend address.
