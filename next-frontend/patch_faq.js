const fs = require('fs');

let code = fs.readFileSync('src/app/faq/page.tsx', 'utf-8');

const old_faqs = `const FAQS = [
  {
    category: "General",
    questions: [
      { q: "What is MatDataHub?", a: "MatDataHub is an AI-powered materials database and analytics platform designed to help engineers and researchers discover, substitute, and analyze materials." },
      { q: "How accurate is the AI Adviser?", a: "Our AI Adviser is fine-tuned on peer-reviewed materials science literature and real-world supply chain data, achieving over 95% accuracy in property predictions." },
    ]
  },
  {
    category: "Pricing & Accounts",
    questions: [
      { q: "What is the difference between Pro and Advanced?", a: "Pro gives you 25 AI queries per day and access to all basic analytics. Advanced unlocks unlimited AI queries, the composite synthesizer, and API access." },
      { q: "Can I cancel my subscription anytime?", a: "Yes, you can cancel your subscription from your Account dashboard at any time. Your access will remain active until the end of your billing cycle." },
    ]
  },
  {
    category: "Technical",
    questions: [
      { q: "How do I export my workspaces?", a: "Inside any workspace, click the 'Export' button in the top right to download your data as a CSV or PDF report." },
      { q: "Where does the pricing data come from?", a: "We aggregate historical and real-time pricing data from global metal exchanges, supplier catalogs, and trade registries." },
    ]
  }
];`;

const new_faqs = `const FAQS = [
  {
    category: "Technical & Platform Features",
    questions: [
      { q: "What formula does the Composite Synthesizer use?", a: "The synthesizer uses the classical Rule of Mixtures (Voigt model) for upper bounds and the inverse Rule of Mixtures (Reuss model) for lower bounds, blending volumetric fractions of Matrix and Reinforcement materials." },
      { q: "How does the AI Material Substitution engine work?", a: "It converts physical properties into a normalized N-dimensional vector space and calculates the Euclidean Root Mean Square (RMS) distance, weighted by your custom sliders (Cost vs Density vs Strength)." },
      { q: "Can I export my Workflows Bill of Materials?", a: "Yes. Inside any active Project Workspace, click the 'Export CSV' button to instantly download your BOM with calculated mass and pricing." }
    ]
  },
  {
    category: "Accounts & Billing",
    questions: [
      { q: "How do I upgrade to the Enterprise EU-CBAM tier?", a: "Go to your Account settings and click 'Upgrade Plan'. Enterprise plans require contacting sales to provision dedicated ESG APIs." },
      { q: "Why am I getting a '429 Too Many Requests' error?", a: "To protect our verified dataset from automated scraping, free tiers are limited to 50 lookups per day. Next.js local development may hit this quickly. Upgrade to Pro for 1000/day." },
    ]
  }
];`;

code = code.replace(old_faqs, new_faqs);
fs.writeFileSync('src/app/faq/page.tsx', code, 'utf-8');
console.log('Patched FAQ');
