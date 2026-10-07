export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-600 dark:text-slate-300">
      <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Privacy Policy</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">1. Information We Collect</h2>
          <p className="mb-2">We collect information you provide directly to us, such as when you create or modify your account, use our API, or contact customer support. This includes your name, email, authentication tokens, and billing information.</p>
          <p><strong>Engineering & Compliance Data:</strong> When you use our BOM processor and CBAM tools, we process the contents of the files you upload (e.g., supplier names, weights, origins, CN codes). Uploaded files are temporarily stored for processing and may be retained in your account history if you are a registered user. You can delete this history at any time.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. How We Use Information</h2>
          <p className="mb-2">We use the information we collect to provide, maintain, and improve our services, process transactions securely, and generate accurate environmental compliance estimates (like CBAM reports).</p>
          <p>We do <strong>not</strong> sell your engineering data, BOMs, or supplier lists to third parties.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">3. Cookies and Tracking</h2>
          <p>We use essential cookies to maintain your session and security tokens. We also use analytics cookies (which you can opt out of) to understand how users interact with our platform.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">4. Data Security</h2>
          <p>We use industry-standard encryption (TLS/SSL in transit, AES-256 at rest) to protect your engineering workspaces, CBAM compliance data, and personal information.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">5. Your GDPR Rights</h2>
          <p>If you are located in the EEA, UK, or Switzerland, you have the right to access, correct, delete, or restrict processing of your personal data. You can delete your BOM history directly from the dashboard or contact us at privacy@matdatahub.com to exercise your rights.</p>
        </section>
      </div>
    </div>
  );
}
