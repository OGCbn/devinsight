export default function RepoSelect({ repos = [], selectedRepo, onChange }) {
    return (
      <div>
        <label className="text-sm text-gray-700 mr-2">Repo:</label>
        <div className="relative w-64">
          <select
            className="appearance-none w-full border rounded px-3 py-2 pr-8 shadow-sm focus:outline-none focus:ring focus:border-blue-300"
            value={selectedRepo}
            onChange={(e) => onChange(e.target.value)}
          >
            <option value="">All</option>
            {repos.map((repo) => (
              <option key={repo.full_name} value={repo.full_name}>
                {repo.full_name}
              </option>
            ))}
          </select>
          <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-2 text-gray-500">
            ▼
          </div>
        </div>
  
        {/* Optional: show selected repo with avatar preview */}
        {selectedRepo && (
          <div className="mt-2 flex items-center gap-2 text-sm text-gray-600">
            <img
              src={
                repos.find((r) => r.full_name === selectedRepo)?.owner?.avatar_url
              }
              alt="avatar"
              className="w-5 h-5 rounded-full"
            />
            <span>{selectedRepo}</span>
          </div>
        )}
      </div>
    );
  }