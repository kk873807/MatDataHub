import { Synthesizer } from "@/components/Synthesizer";
import { SafetyFactor } from "@/components/SafetyFactor";
import { ThermalExpansion } from "@/components/ThermalExpansion";
import { BeamDeflection } from "@/components/BeamDeflection";
import { FatigueLife } from "@/components/FatigueLife";
import { RiskAuditor } from "@/components/RiskAuditor";

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center p-8 md:p-24 bg-neutral-950 text-white font-sans">
      <div className="z-10 w-full max-w-7xl items-center flex flex-col gap-12">
        
        {/* Header Section */}
        <div className="text-center space-y-4">
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white via-neutral-200 to-neutral-500">
            MatDataHub
          </h1>
          <p className="text-lg md:text-2xl text-neutral-400 max-w-3xl mx-auto">
            Advanced Engineering Physics, Financial Math, and ESG Analytics.
          </p>
        </div>
        
        {/* Risk Auditor (Full Width) */}
        <div className="w-full">
          <RiskAuditor />
        </div>

        {/* Engineering Calculators Grid */}
        <div className="w-full">
          <h2 className="text-3xl font-bold mb-6 text-neutral-200">Engineering Physics</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-2 gap-6 w-full">
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
