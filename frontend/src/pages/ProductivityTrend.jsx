import { useEffect, useState } from "react";
import { getProductivityTrend, getRepos } from "../api";
import ChartCard from "../components/ChartCard";
import { Line } from "react-chartjs-2";
import FilterBar from "../components/Filterbar";
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

function getColorFromName(name) {
  let hash = 0;
  for (let i = 0; i < name.length; i++) {
    hash = name.charCodeAt(i) + ((hash << 5) - hash);
  }
  const hue = Math.abs(hash % 360);
  return `hsl(${hue}, 70%, 50%)`;
}

export default function ProductivityTrend() {
  const [data, setData] = useState([]);
  const [repos, setRepos] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState("");

  useEffect(() => {
    getRepos()
      .then((res) => setRepos(res.data.repos || []))
      .catch((err) => console.error("Failed to fetch repos", err));
  }, []);

  useEffect(() => {
    const params = selectedRepo ? { repo: selectedRepo } : {};
    getProductivityTrend(params)
      .then((res) => setData(Array.isArray(res.data) ? res.data : []))
      .catch((err) => console.error("Failed to fetch productivity trend", err));
  }, [selectedRepo]);

  const weeks = Array.from(new Set(data.map((d) => d.week))).sort();
  const authors = Array.from(new Set(data.map((d) => d.author)));

  const datasets = authors.map((author) => {
    const dataMap = new Map();
    data.filter((d) => d.author === author).forEach((d) => dataMap.set(d.week, d.count));
    const color = getColorFromName(author);
    return {
      label: author,
      data: weeks.map((w) => dataMap.get(w) || 0),
      fill: false,
      tension: 0.2,
      borderColor: color,
      backgroundColor: color,
    };
  });

  const chartData = {
    labels: weeks,
    datasets,
  };

  return (
    <ChartCard title="Productivity Trend (Commits per Week)">
      <FilterBar
        repos={repos}
        authors={[]} // no author filter for now
        selectedRepo={selectedRepo}
        selectedAuthor=""
        onChange={({ repo }) => setSelectedRepo(repo)}
      />

      {data.length === 0 ? (
        <p className="text-sm text-gray-500">No data available.</p>
      ) : (
        <Line data={chartData} />
      )}
    </ChartCard>
  );
}