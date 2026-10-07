export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-600 dark:text-slate-300">
      <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Privacy Policy</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">1. Data Controller</h2>
          <p>MatDataHub GmbH (fictional placeholder for demo), located at Example Street 1, 10115 Berlin, Germany, is the data controller responsible for your personal data. Contact us at privacy@matdatahub.com.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. Information We Collect & Lawful Bases</h2>
          <p className="mb-2">We collect your name, email, authentication tokens, and billing information. We process this data on the lawful basis of <strong>contractual necessity</strong> (to provide our service) and <strong>legitimate interest</strong> (to secure and improve our platform).</p>
          <p><strong>Engineering & Compliance Data:</strong> When you use our BOM processor and CBAM tools, we process your supply chain data (supplier names, origins, CN codes). We do <strong>not</strong> sell your engineering data.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">3. Subprocessors & Data Transfers</h2>
          <p>To provide our services, we use third-party subprocessors under strict data processing agreements. These include:</p>
          <ul className="list-disc pl-6 mt-3 space-y-2 mb-2">
            <li><strong>Hosting:</strong> Vercel and Render (infrastructure).</li>
            <li><strong>Database:</strong> PostgreSQL managed providers.</li>
            <li><strong>AI Features:</strong> OpenAI/Google Cloud (for the AI Material Adviser).</li>
          </ul>
          <p><strong>AI Data Usage:</strong> When using the AI Material Adviser, snippets of your workspace or query are sent to the AI provider solely for generating a response. We have opted out of data sharing for AI model training, meaning your proprietary BOMs are <strong>never</strong> used to train public models.</p>
          <p>Where data is transferred outside the EEA, we rely on Standard Contractual Clauses (SCCs).</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">4. Retention Periods</h2>
          <p>Account data is retained as long as your account is active. CBAM BOM history and uploaded files are retained for a maximum of 12 months after upload unless explicitly deleted by you earlier. You can delete this history at any time from your dashboard.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">5. Cookies and Consent</h2>
          <p>We use essential cookies to maintain your session. Non-essential analytics cookies are only set if you explicitly consent via our cookie banner. You can withdraw your consent at any time in your account settings.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">6. Your GDPR Rights</h2>
          <p>If you are located in the EEA, UK, or Switzerland, you have the right to access, correct, delete, or restrict processing of your personal data. Contact us at privacy@matdatahub.com to exercise your rights.</p>
        </section>
      </div>
    </div>
  );
}
