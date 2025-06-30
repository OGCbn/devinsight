import CommitsPerDay from "./CommitsPerDay";
import TopAuthors from "./TopAuthors";
import ProductivityTrend from "./ProductivityTrend";

export default function Dashboard() {
  return (
    <div className="p-6 max-w-5xl mx-auto">
      <CommitsPerDay />
      <TopAuthors />
      <ProductivityTrend />
    </div>
  );
}
