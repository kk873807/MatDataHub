import { LEGAL_VERSION, LEGAL_LAST_UPDATED } from "@/lib/legal";

export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-600 dark:text-slate-300">
      <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Privacy Policy</h1>
      <p className="mb-4">Last updated: {LEGAL_LAST_UPDATED} &middot; Version {LEGAL_VERSION}</p>
      
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">1. Data Controller & Contact</h2>
          <p>
            MatDataHub is the data controller responsible for your personal data. For questions about this policy, access requests, or to request permanent deletion of your account and uploaded data, contact our dedicated privacy team at <a href="mailto:matdatahub.support@gmail.com" className="text-indigo-600 dark:text-indigo-400 underline font-medium">matdatahub.support@gmail.com</a>.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. Information We Collect & Lawful Bases</h2>
          <p className="mb-3">
            We collect and process personal data under the lawful bases of <strong>contractual necessity</strong> (Article 6(1)(b) GDPR) to deliver our service and <strong>legitimate interest</strong> (Article 6(1)(f) GDPR) to prevent fraud and ensure platform security:
          </p>
          <ul className="list-disc pl-6 space-y-2 mb-3">
            <li><strong>Account Data:</strong> Name, email address, password hashes, or OAuth profile identifiers when authenticating.</li>
            <li><strong>BOM & Trade Compliance Data:</strong> Material IDs, line item descriptions, quantities, Combined Nomenclature (CN) tariff codes, and country-of-origin names provided in uploaded CSV files or manual entries. We do <strong>not</strong> sell, license, or share your proprietary BOM or supply chain data with third-party advertisers.</li>
            <li><strong>Billing Records:</strong> Transaction IDs, tier status, and payment metadata processed through our payment gateway. We do not store raw payment card numbers.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">3. Infrastructure, Hosting Locations & Subprocessors</h2>
          <p className="mb-3">
            To deliver our platform globally with high availability, your data is processed across the following hosting locations and service providers:
          </p>
          <ul className="list-disc pl-6 space-y-2 mb-3">
            <li><strong>Database Hosting (Japan):</strong> Our primary relational database is hosted on Supabase PostgreSQL located in AWS region <code>ap-northeast-1</code> (Tokyo, Japan). European Commission adequacy decisions and Standard Contractual Clauses (SCCs) govern international transfers.</li>
            <li><strong>Backend API Processing (United States):</strong> Application workflows, parsing engines, and calculation routines run on Render infrastructure located in Oregon, United States (<code>us-west</code>).</li>
            <li><strong>Frontend & Edge Delivery:</strong> Web interfaces, static assets, and edge routing are deployed via Vercel Inc.</li>
            <li><strong>Authentication:</strong> Google Sign-In is provided via Google OAuth (Google LLC, USA) for single sign-on authentication alongside email-based registration.</li>
            <li><strong>Payment Processing:</strong> Transactions and tier subscriptions are processed by Razorpay (Razorpay Software Private Limited).</li>
            <li><strong>AI Material Adviser (Optional):</strong> When you use the AI Material Adviser chat, the text you type, together with matching entries from our public materials catalogue, is sent to Groq, Inc. (USA) to generate the reply. Uploaded BOM files and CBAM analyses are <strong>not</strong> sent to Groq or to any other AI provider; please do not paste confidential BOM data into the chat. Groq&apos;s published data policy states that it does not retain inference inputs by default, but may log inputs and outputs for up to 30 days to troubleshoot errors or investigate abuse, and stores such data in the United States.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">4. Data Retention & User Deletion Control</h2>
          <p className="mb-3">
            Uploaded Bill of Materials (BOM) files, parsed line items, and calculation outputs are stored in full in our database (<code>bom_analyses.results_json</code>) so that you can view your historical analyses, track trends, and export audit sheets.
          </p>
          <ul className="list-disc pl-6 space-y-2 mb-3">
            <li><strong>Stored Until Deleted:</strong> Analyses and BOM records remain stored in full in your account until you choose to delete them.</li>
            <li><strong>Single-Analysis Deletion:</strong> You can delete any individual historical analysis directly at any time from your account history dashboard.</li>
            <li><strong>Full Account & Data Deletion:</strong> You may request complete and permanent deletion of your account, profile, and all associated BOM history by emailing <a href="mailto:matdatahub.support@gmail.com" className="text-indigo-600 dark:text-indigo-400 underline font-medium">matdatahub.support@gmail.com</a>. Deletion requests are processed within 30 days.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">5. Cookies and Authentication Sessions</h2>
          <p>
            We use essential security tokens and cookies to maintain authenticated user sessions and protect against cross-site request forgery. We do not use third-party behavioral advertising cookies.
          </p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">6. Your Data Protection Rights (GDPR, UK GDPR &amp; India DPDP Act)</h2>
          <p>
            Depending on your location—including the European Economic Area (EEA), the United Kingdom, Switzerland, or India (under the Digital Personal Data Protection Act, 2023)—you have the right to access, correct, rectify, export, restrict processing, withdraw consent, or request permanent erasure of your personal data, as well as the right to grievance redressal. To exercise any of these rights, contact our privacy and grievance officer at <a href="mailto:matdatahub.support@gmail.com" className="text-indigo-600 dark:text-indigo-400 underline font-medium">matdatahub.support@gmail.com</a>.
          </p>
        </section>
      </div>
    </div>
  );
}
