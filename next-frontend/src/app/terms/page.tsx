import { LEGAL_VERSION, LEGAL_LAST_UPDATED } from "@/lib/legal";

export default function TermsPage() {
  return (
    <div className="max-w-4xl mx-auto p-12 text-slate-600 dark:text-slate-300">
      <h1 className="text-4xl font-bold text-slate-900 dark:text-white font-heading mb-6">Terms and Conditions</h1>
      <p className="mb-4">Last updated: {LEGAL_LAST_UPDATED} &middot; Version {LEGAL_VERSION}</p>
      
      <div className="space-y-6">
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">1. Acceptance of Terms</h2>
          <p>By accessing and using MatDataHub, you accept and agree to be bound by the terms and provision of this agreement.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">2. Intellectual Property &amp; Anti-Scraping</h2>
          <p>
            All content, database schemas, material datasets, proprietary algorithms (including the Rule of Mixtures and CBAM equations), and user interfaces on MatDataHub are the exclusive intellectual property of MatDataHub and are protected by international copyright laws. 
          </p>
          <ul className="list-disc pl-6 mt-3 space-y-2">
            <li><strong>No Data Scraping:</strong> Automated scraping, crawling, or mass-downloading of our material database is strictly prohibited. Violators will face immediate permanent IP bans and legal action.</li>
            <li><strong>No Derivative Works:</strong> You may not copy, reverse-engineer, or resell our datasets, calculators, or platform features to build a competing product.</li>
          </ul>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">3. Description of Service &amp; Free Beta Status</h2>
          <p>MatDataHub provides users with access to a rich collection of engineering materials data, tools, and analytics. You understand and agree that the service is provided &quot;AS-IS&quot;.</p>
          <p className="mt-3"><strong>Free Beta:</strong> The EU CBAM cost estimator and related platform tools are currently offered as a free beta, with no uptime or availability commitment and features that may change, be suspended, or be withdrawn at any time without notice.</p>
        </section>
        
        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">4. Pricing and Regulatory Factor Reliability</h2>
          <p>Material pricing is derived from market proxy indices for trend analysis and does not constitute live commercial quotes. CBAM carbon factor defaults are mapped from Commission Implementing Regulation (EU) 2025/2621 (as amended by (EU) 2026/1740). Outputs are preliminary estimates and not live commercial or customs quotes.</p>
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
          <p>For Enterprise customers processing personal data on behalf of EU citizens, a standard Data Processing Agreement (DPA) is available upon request. Please contact <a href="mailto:matdatahub.support@gmail.com" className="text-indigo-600 dark:text-indigo-400 underline font-medium">matdatahub.support@gmail.com</a> (Subject: Enterprise DPA) to execute a DPA.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">8. Governing Law and Jurisdiction</h2>
          <p>These Terms and any disputes arising out of or related to the service are governed by and construed in accordance with the laws of India, without giving effect to any choice or conflict of law principles. Any legal suit, action, or proceeding arising out of or related to these Terms shall be instituted exclusively in the competent courts of New Delhi, India.</p>
        </section>

        <section>
          <h2 className="text-2xl font-bold text-slate-900 dark:text-white font-heading mb-3">9. Changes to These Terms</h2>
          <p>Each version of these Terms and of our Privacy Policy carries the version identifier shown at the top of the page. When we change the wording, we publish a new version and ask signed-in users to accept it before continuing to use the service. We keep a record of which version each account accepted and when.</p>
        </section>
      </div>
    </div>
  );
}
