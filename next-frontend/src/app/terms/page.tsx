export default function TermsPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-300">
      <h1 className="text-4xl font-bold text-white mb-6">Terms and Conditions</h1>
      <p className="mb-4">Last updated: {new Date().toLocaleDateString()}</p>
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-white mb-3">1. Acceptance of Terms</h2>
          <p>By accessing and using MatDataHub, you accept and agree to be bound by the terms and provision of this agreement.</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-white mb-3">2. Description of Service</h2>
          <p>MatDataHub provides users with access to a rich collection of engineering materials data, tools, and analytics. You understand and agree that the service is provided "AS-IS".</p>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-white mb-3">3. Pricing and Data Reliability</h2>
          <p>All macroeconomic pricing and CBAM calculations are derived from proxy indices for trend analysis. They do not constitute live commercial quotes.</p>
        </section>
      </div>
    </div>
  );
}
