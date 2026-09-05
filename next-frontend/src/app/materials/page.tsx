export default function MaterialsPage() {
  return (
    <main className="flex flex-col p-8 lg:p-12">
      <div className="w-full max-w-7xl flex flex-col gap-6">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-white">Browse Materials</h1>
          <p className="text-neutral-400">Search, filter, and compare thousands of engineering materials in our database.</p>
        </div>
        
        <div className="mt-8 p-12 border-2 border-dashed border-neutral-800 rounded-2xl flex flex-col items-center justify-center text-center">
          <div className="w-16 h-16 rounded-full bg-neutral-900 flex items-center justify-center mb-4">
            <svg className="w-8 h-8 text-neutral-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
            </svg>
          </div>
          <h3 className="text-xl font-medium text-neutral-200">Material Database UI Coming Soon</h3>
          <p className="text-neutral-500 mt-2 max-w-md">
            This page will connect to the /api/v1/materials endpoint from the FastAPI backend to display the full searchable material catalog.
          </p>
        </div>
      </div>
    </main>
  );
}
