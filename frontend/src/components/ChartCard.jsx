export default function ChartCard({ title, children }) {
    return (
      <div className="bg-white rounded-2xl shadow p-6 w-full mb-6">
        <h2 className="text-xl font-semibold mb-4">{title}</h2>
        {children}
      </div>
    );
  }
  