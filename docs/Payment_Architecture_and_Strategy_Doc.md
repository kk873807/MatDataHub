# MatDataHub Payment Architecture & Growth Strategy
*Reference Document - Created September 2026*

This document serves as your master reference for the end-to-end payment workflow, the security measures implemented, the administrative tools built, and your initial market growth strategy.

---

## 1. Technical Payment Architecture (Razorpay)

Your platform uses **Razorpay Payment Links** to facilitate a secure, automated checkout process.

### A. Link Generation (`POST /api/v1/payments/create-link`)
- **Location:** `app/routers/payments.py`
- **How it works:** When a user clicks "Upgrade", the frontend sends their requested tier. The backend verifies they don't already own that tier, generates a secure one-time payment link via Razorpay, injects the user's ID into hidden metadata (`notes`), and explicitly sets the checkout merchant name to **"MatDataHub"**.
- **Security Protections:**
  - **Double-Billing Guard:** Blocks the request if the user is already on the requested tier.
  - **Downgrade Firewall:** Blocks an Advanced user from accidentally downgrading themselves to Pro via the automated checkout.
  - **Callback Routing:** Securely redirects the user back to the MatDataHub frontend after they complete the payment.

### B. The Webhook Processor (`POST /api/v1/payments/webhook`)
- **Location:** `app/routers/payments.py`
- **How it works:** The millisecond a payment clears, Razorpay pings this endpoint. It reads the hidden `user_id`, upgrades the user's database profile, and logs the receipt.
- **Security Protections:**
  - **Cryptographic Signatures:** Evaluates the `X-Razorpay-Signature` against your `RAZORPAY_WEBHOOK_SECRET` using HMAC-SHA256. If a hacker tries to fake a webhook, or if your secret is missing from `.env`, the server safely rejects it.
  - **Idempotency (Duplicate Prevention):** Checks the unique Razorpay `payment_id`. If Razorpay accidentally sends the webhook twice due to network lag, the backend catches the duplicate and ignores it.
  - **Delayed Downgrade Protection:** If an Advanced user clicks a 3-month-old "Pro" link in their email inbox, the webhook intercepts the payload and refuses to downgrade their account.
  - **Ghost Account Ledger:** If a user pays but deletes their MatDataHub account a second later, the webhook still permanently logs the financial receipt to ensure your bank deposits always match your database.
  - **Auto-Retries:** If your Supabase database temporarily crashes, the webhook explicitly throws an `HTTP 500` error, instructing Razorpay to place the payment in a queue and automatically retry it later.

---

## 2. Frontend & Administrative UI

### A. User Billing Dashboard
- **Locations:** `next-frontend/src/app/account/page.tsx` & `next-frontend/src/components/AccountModals.tsx`
- **How it works:** The "Transaction & Billing History" tab dynamically fetches `GET /api/v1/account/transactions`. It renders a color-coded ledger of every payment the individual user has made, replacing the old hardcoded UI.

### B. Admin Financial Ledger
- **Location:** `next-frontend/src/app/admin/page.tsx`
- **How it works:** Inside your secure Admin Portal (below User Contributions), there is a **Financial Ledger**. 
- **Features:** It fetches `GET /api/v1/admin/transactions` and maps out every payment ever made on the platform, allowing you to instantly see the Buyer's Email, Tier, Amount Paid, Razorpay Transaction ID, and Status.

---

## 3. Environment Variables (The Launch Checklist)

Before going live, ensure these three variables are added to your **Render Environment Variables** and your local `.env` file:

```env
RAZORPAY_KEY_ID=         # Found in Razorpay Dashboard -> API Keys
RAZORPAY_KEY_SECRET=     # Found in Razorpay Dashboard -> API Keys
RAZORPAY_WEBHOOK_SECRET= # Created by YOU in Razorpay Dashboard -> Webhooks
```
*(Note: If `RAZORPAY_WEBHOOK_SECRET` is missing in production, all incoming payments will safely pause until you add it.)*

---

## 4. The Growth Strategy Playbook

We pivoted your marketing text from monthly subscriptions (e.g., "₹499/mo") to **Lifetime Deals** ("₹499 for Lifetime PRO"). This matches your current backend architecture and provides a massive strategic advantage for a new startup.

### The "500-User" Plan
1. **The Goal:** Use the extreme value of a "Lifetime Deal" to aggressively capture your first 500 paid users. This eliminates buyer hesitation (fear of recurring charges) and gets you fast capital and critical platform feedback.
2. **The Switch:** Once your platform reaches a critical mass of users and feature parity (e.g., 500 users or ₹2.5L revenue), you will upgrade the backend to use the Razorpay Subscriptions API for monthly recurring revenue.
3. **The Grandfather Rule:** To protect your reputation, your first 500 lifetime users will **never** be charged a monthly fee. They are "grandfathered" in. The new monthly fee will only apply to brand-new users. 
4. **The Marketing Event:** You will announce the switch to Monthly Subscriptions 14 days in advance. This creates massive FOMO (Fear Of Missing Out) and traditionally causes a massive spike in sales from free users rushing to secure the Lifetime Deal before it disappears forever.
