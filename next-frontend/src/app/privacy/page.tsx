export default function PrivacyPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-600 dark:text-slate-300">
      <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Privacy Policy</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">1. Information We Collect</h2>
          <p>We collect information you provide directly to us, such as when you create or modify your account, or contact customer support. This includes your name, email, and authentication tokens.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. How We Use Information</h2>
          <p>We use the information we collect to provide, maintain, and improve our services, and to process transactions securely.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">3. Data Security</h2>
          <p>We use industry-standard encryption and security measures to protect your engineering workspaces and personal data.</p>
        </section>
      </div>
    </div>
  );
}
