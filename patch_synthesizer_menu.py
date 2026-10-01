import os
import re

file_path = 'next-frontend/src/app/analytics/synthesizer/page.tsx'
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace fetch for /materials?per_page=2000 with /materials/menu
content = content.replace('`${API}/materials?per_page=2000`', '`${API}/materials/menu`')
content = content.replace('.then(data => setAllMaterials(data.materials || []));', '.then(data => setAllMaterials(data || []));')

# Modify handleSynthesize to fetch properties
handle_syn = """  const handleSynthesize = async () => {
    if (!matA || !matB) return;
    setLoading(true);

    try {
      // Securely fetch properties on-demand to prevent bulk scraping
      const [resA, resB] = await Promise.all([
        fetch(`${API}/materials/${matA}`),
        fetch(`${API}/materials/${matB}`)
      ]);
      
      const objA = await resA.json();
      const objB = await resB.json();

      if (objA && objB) {
        const vA = volFractionA / 100;
        const vB = 1 - vA;

        // Rule of Mixtures (Upper Bound)
        const density = ((objA.density || 0) * vA) + ((objB.density || 0) * vB);
        const elastic_modulus = ((objA.elastic_modulus || 0) * vA) + ((objB.elastic_modulus || 0) * vB);
        const tensile = ((objA.tensile_strength_min || 0) * vA) + ((objB.tensile_strength_min || 0) * vB);
        
        // Economics Correct Physics: Cost per kg must scale by MASS fraction, not VOLUME fraction
        const massFracA = density > 0 ? ((objA.density || 0) * vA) / density : 0.5;
        const massFracB = density > 0 ? ((objB.density || 0) * vB) / density : 0.5;
        const cost = ((objA.cost_per_kg_min || 0) * massFracA) + ((objB.cost_per_kg_min || 0) * massFracB);

        setResult({
          name: `Composite: ${vA*100}% ${objA.name} / ${vB*100}% ${objB.name}`,
          density: density.toFixed(2),
          elastic_modulus: elastic_modulus.toFixed(1),
          tensile: tensile.toFixed(0),
          cost: cost.toFixed(2)
        });
      }
    } catch (e) {
      console.error("Failed to fetch material properties", e);
    } finally {
      setLoading(false);
    }
  };"""

# Use regex to replace the old handleSynthesize function
content = re.sub(
    r'const handleSynthesize = \(\) => \{.*?setLoading\(false\);\n\s{4}\};\n\s{2}\};',
    handle_syn,
    content,
    flags=re.DOTALL
)

# Alternative regex just in case (the above might fail due to setTimeout structure)
content = re.sub(
    r'const handleSynthesize = \(\) => \{.*?\}\,\s*600\);\n\s{2}\};',
    handle_syn,
    content,
    flags=re.DOTALL
)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(content)
