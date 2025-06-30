import RepoSelect from "./RepoSelect";
export default function FilterBar({
  repos = [],
  authors = [],
  selectedRepo = "",
  selectedAuthor = "",
  onChange,
}) {
  const handleRepoChange = (e) => {
    onChange({ repo: e.target.value, author: selectedAuthor });
  };

  const handleAuthorChange = (e) => {
    onChange({ repo: selectedRepo, author: e.target.value });
  };

  return (
    <div className="mb-4 flex gap-4">
      <RepoSelect
        repos={repos}
        selectedRepo={selectedRepo}
        onChange={(repo) => onChange({ repo, author: selectedAuthor })}
      />

      {authors.length > 0 && (
        <div>
          <label className="text-sm text-gray-700 mr-2">Author:</label>
          <select
            className="border rounded px-2 py-1"
            value={selectedAuthor}
            onChange={handleAuthorChange}
          >
            <option value="">All</option>
            {authors.map((a) => (
              <option key={a.author} value={a.author}>
                {a.author}
              </option>
            ))}
          </select>
        </div>
      )}
    </div>
  );
}