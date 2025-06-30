import { useEffect, useState } from "react";
import { getTopAuthors, getRepos } from "../api";
import ChartCard from "../components/ChartCard";
import { Bar } from "react-chartjs-2";
import FilterBar from "../components/Filterbar";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  BarElement,
  Tooltip,
  Legend
} from "chart.js";

ChartJS.register(CategoryScale, LinearScale, BarElement, Tooltip, Legend);

export default function TopAuthors() {
  const [data, setData] = useState([]);
  const [repos, setRepos] = useState([]);
  const [selectedRepo, setSelectedRepo] = useState("");

  useEffect(() => {
    getRepos().then(res => {
      setRepos(res.data.repos || []);
    }).catch(err => {
      console.error("Failed to fetch repos", err);
    });
  }, []);
  

  useEffect(() => {
    const params = selectedRepo ? { repo: selectedRepo } : {};
    getTopAuthors(params).then(res => setData(res.data));
  }, [selectedRepo]);

  const chartData = {
    labels: data.map(a => a.author),
    datasets: [{
      label: "Commits",
      data: data.map(a => a.count),
      backgroundColor: "rgb(59, 130, 246)",
    }]
  };

  return (
    <ChartCard title="Top Commit Authors">
      <FilterBar
        repos={repos}
        authors={[]} // no author filtering here
        selectedRepo={selectedRepo}
        selectedAuthor=""
        onChange={({ repo }) => {
          setSelectedRepo(repo);
        }}
      />

      <Bar data={chartData} />
    </ChartCard>
  );
}
