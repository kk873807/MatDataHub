export default function ProjectsPage() {
  return (
    <main className="flex flex-col p-8 lg:p-12">
      <div className="w-full max-w-7xl flex flex-col gap-6">
        <div className="space-y-2">
          <h1 className="text-4xl font-bold text-white">Workflows & Projects</h1>
          <p className="text-neutral-400">Manage your engineering projects and run advanced AI-driven workflows.</p>
        </div>
        
        <div className="mt-8 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="p-6 rounded-2xl bg-neutral-900 border border-neutral-800 hover:border-neutral-700 transition-colors cursor-pointer">
            <h3 className="text-lg font-bold text-white mb-2">Create New Project</h3>
            <p className="text-sm text-neutral-400">Start a new engineering material selection project with AI assistance.</p>
          </div>
          <div className="p-6 rounded-2xl bg-neutral-900 border border-neutral-800">
            <h3 className="text-lg font-bold text-white mb-2">Recent Project: Aerospace Hull</h3>
            <p className="text-sm text-neutral-400">Last edited: 2 days ago</p>
          </div>
        </div>

        <div className="mt-8 p-12 border-2 border-dashed border-neutral-800 rounded-2xl flex flex-col items-center justify-center text-center">
          <h3 className="text-xl font-medium text-neutral-200">Workflow Canvas Coming Soon</h3>
          <p className="text-neutral-500 mt-2 max-w-md">
            This section will port over the advanced project creation and saved states features from the Streamlit app.
          </p>
        </div>
      </div>
    </main>
  );
}
