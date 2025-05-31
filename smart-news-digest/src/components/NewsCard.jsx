export default function NewsCard({ title, summary, source, category }) {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4 text-gray-800">
      <div className="flex justify-between items-center mb-2">
        <span className="text-sm bg-blue-100 text-blue-800 px-2 py-1 rounded">{category}</span>
        <span className="text-xs text-gray-500 italic">{source}</span>
      </div>
      <h2 className="text-lg font-bold mb-2">{title}</h2>
      <p className="text-sm">{summary}</p>
    </div>
  );
}