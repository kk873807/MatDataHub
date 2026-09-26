export default function TermsPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-600 dark:text-slate-300">
      <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Terms and Conditions</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>
      
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">1. Acceptance of Terms</h2>
          <p>By accessing and using MatDataHub, you accept and agree to be bound by the terms and provision of this agreement.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. Intellectual Property & Anti-Scraping</h2>
          <p>
            All content, database schemas, material datasets, proprietary algorithms (including the Rule of Mixtures and CBAM equations), and user interfaces on MatDataHub are the exclusive intellectual property of MatDataHub and are protected by international copyright laws. 
          </p>
          <ul className="list-disc pl-6 mt-3 space-y-2">
            <li><strong>No Data Scraping:</strong> Automated scraping, crawling, or mass-downloading of our material database is strictly prohibited. Violators will face immediate permanent IP bans and legal action.</li>
            <li><strong>No Derivative Works:</strong> You may not copy, reverse-engineer, or resell our datasets, calculators, or platform features to build a competing product.</li>
            <li><strong>Watermarking:</strong> Data exports and generated PDF reports contain cryptographic and visual watermarks to track unauthorized redistribution of our proprietary data.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">3. Description of Service</h2>
          <p>MatDataHub provides users with access to a rich collection of engineering materials data, tools, and analytics. You understand and agree that the service is provided "AS-IS".</p>
        </section>
        
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">4. Pricing and Data Reliability</h2>
          <p>All macroeconomic pricing and CBAM calculations are derived from proxy indices for trend analysis. They do not constitute live commercial quotes.</p>
        </section>
      </div>
    </div>
  );
}
