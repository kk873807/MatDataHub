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

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">5. EU CBAM & Regulatory Disclaimer (No Reliance)</h2>
          <p>The CBAM analytics and reporting tools provided by MatDataHub are designed for preliminary evaluation, informational modeling, and cost estimation purposes only.</p>
          <ul className="list-disc pl-6 mt-3 space-y-2">
            <li><strong>Not Legal or Customs Advice:</strong> Our calculations, reports, and data outputs do not constitute professional compliance, tax, customs, or legal advice.</li>
            <li><strong>No Reliance for Official Filings:</strong> You acknowledge and agree not to rely on any outputs from this service for the purpose of official customs declarations, registry filings, or statutory compliance under Regulation (EU) 2023/956. Importers must independently verify all Combined Nomenclature (CN) codes, country-of-origin rules, and carbon factor defaults with a licensed customs broker or qualified trade legal counsel.</li>
            <li><strong>Adjustment Scope:</strong> Estimates use published Commission default factors and simplified phase-in calculations; the tool does not yet apply the definitive free-allocation benchmark adjustment under Implementing Regulation (EU) 2025/2620. Actual regulatory liabilities may differ materially.</li>
            <li><strong>Liability Limitation:</strong> To the maximum extent permitted by law, MatDataHub disclaims all liability for customs fines, surcharges, penalties, or compliance disputes resulting from your reliance on our preliminary estimates.</li>
          </ul>
        </section>
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">6. Liability Cap</h2>
          <p>To the maximum extent permitted by applicable law, MatDataHub’s total liability for any claims arising under these Terms shall not exceed the total amount paid by you to MatDataHub in the twelve (12) months preceding the claim. We are not liable for indirect, incidental, or consequential damages, including loss of profits or customs fines.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">7. Enterprise Data Processing Agreement (DPA)</h2>
          <p>For Enterprise customers processing personal data on behalf of EU citizens, a standard Data Processing Agreement (DPA) is available upon request. Please contact enterprise@matdatahub.com to execute a DPA.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">8. Governing Law and Jurisdiction</h2>
          <p>These terms are governed by the laws of Germany. Any disputes arising out of or in connection with these terms shall be subject to the exclusive jurisdiction of the courts of Berlin, Germany.</p>
        </section>
      </div>
    </div>
  );
}
