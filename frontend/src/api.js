import axios from "axios";

//to be change when no longer in test mode
const API = "http://localhost:5000";

//can be added more, these connect the frontend to backend starts
//function calls
export const getCommitsPerDay = (params = {}) =>
    axios.get(`${API}/api/stats/commits-per-day`, {params});

export const getTopAuthors = (params = {}) =>
    axios.get(`${API}/api/stats/top-authors`, { params });
  
export const getProductivityTrend = (params = {}) => {
  const pat = import.meta.env.VITE_GITHUB_PAT;

  return axios.get(`${API}/api/stats/productivity-trend`, {
    params,
    headers: {
      Authorization: pat,
    },
  });
};

//filtering
export const getRepos = () => {
  const pat = import.meta.env.VITE_GITHUB_PAT;

  return axios.get("http://localhost:5000/repos", {
    headers: {
      Authorization: pat,
    },
  });
};

