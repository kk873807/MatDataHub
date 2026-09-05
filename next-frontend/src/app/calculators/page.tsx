import { Synthesizer } from "@/components/Synthesizer";
import { SafetyFactor } from "@/components/SafetyFactor";
import { ThermalExpansion } from "@/components/ThermalExpansion";
import { BeamDeflection } from "@/components/BeamDeflection";
import { FatigueLife } from "@/components/FatigueLife";
import { RiskAuditor } from "@/components/RiskAuditor";

export default function CalculatorsPage() {
  return (
    <main className="flex flex-col items-center p-8 lg:p-12">
      <div className="w-full max-w-7xl flex flex-col gap-12">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-white">Engineering Calculators</h1>
          <p className="text-neutral-400">Run physics, mathematics, and financial simulations.</p>
        </div>
        
        {/* Risk Auditor (Full Width) */}
        <div className="w-full">
          <RiskAuditor />
        </div>

        {/* Engineering Calculators Grid */}
        <div className="w-full">
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-6 w-full">
            <Synthesizer />
            <BeamDeflection />
            <SafetyFactor />
            <ThermalExpansion />
            <FatigueLife />
          </div>
        </div>
      </div>
    </main>
  );
}
