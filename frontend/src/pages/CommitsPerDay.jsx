import { useEffect, useState } from "react";
import { getCommitsPerDay, getRepos, getTopAuthors } from "../api";
import ChartCard from "../components/ChartCard";
import { Line } from "react-chartjs-2";
import FilterBar from "../components/FilterBar";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Tooltip,
  Legend,
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Tooltip, Legend);

export default function CommitsPerDay() {
  const [data, setData] = useState([]);
  const [repos, setRepos] = useState([]);
  const [authors, setAuthors] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState("");
  const [selectedAuthor, setSelectedAuthor] = useState("");

  useEffect(() => {
    getRepos().then(res => setRepos(res.data.repos || []));
  }, []);

  useEffect(() => {
    const params = selectedRepo ? { repo: selectedRepo } : {};
    getTopAuthors(params)
      .then(res => setAuthors(res.data || []))
      .catch(err => console.error("Failed to fetch authors", err));
  }, [selectedRepo]);

  useEffect(() => {
    const params = {};
    if (selectedRepo) params.repo = selectedRepo;
    if (selectedAuthor) params.author = selectedAuthor;

    getCommitsPerDay(params).then(res => setData(res.data || []));
  }, [selectedRepo, selectedAuthor]);

  const chartData = {
    labels: data.map(d => d.date),
    datasets: [
      {
        label: "Commits",
        data: data.map(d => d.count),
        borderColor: "rgb(59, 130, 246)",
        backgroundColor: "rgba(59, 130, 246, 0.5)",
        fill: true,
        tension: 0.3,
      },
    ],
  };

  return (
    <ChartCard title="Commits Per Day">
      <FilterBar
        repos={repos}
        authors={authors}
        selectedRepo={selectedRepo}
        selectedAuthor={selectedAuthor}
        onChange={({ repo, author }) => {
          setSelectedRepo(repo);
          setSelectedAuthor(author);
        }}
      />

      {data.length === 0 ? (
        <p className="text-sm text-gray-500">No data available.</p>
      ) : (
        <Line data={chartData} />
      )}
    </ChartCard>
  );
}
