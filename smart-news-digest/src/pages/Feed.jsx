import NewsCard from '../components/NewsCard';

const articles = [
  {
    title: 'AI Breakthrough in Medicine',
    summary: 'Researchers develop an AI that diagnoses diseases faster than doctors.',
    source: 'TechCrunch',
    category: 'Technology',
  },
  {
    title: 'Global Warming Alert',
    summary: 'UN warns about rising sea levels affecting 1.2 billion people by 2050.',
    source: 'BBC News',
    category: 'Environment',
  },
];

export default function Feed() {
  return (
    <div className="min-h-screen bg-gray-100 p-6">
        <h1 className="text-3xl font-bold mb-6 text-center"> News Feed</h1>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
            {articles.map((article, index) => (
                <div
                 key={index}
                 className="bg-black rounded-lg shadow-md p-5 hover:shadow-lg transition">
                    <span className="text-sm text-white-600 font-semibold">
                        {article.category}
                    </span>
                    <h2 className="text-xl font-bold mt-2 text-white">{article.title}</h2>
                    <p className="text-gray-600 mt-2 font-bold">{article.summary}</p>
                    <div className="text-sm text-right text-gray-500 mt-4">
                        {article.source}
                        </div>
                        </div>
            ))}
        </div>

    </div>
    
  );
}