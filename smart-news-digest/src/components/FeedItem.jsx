import React from 'react';

const FeedItem = ({ article }) => {
  const { title, description, source, image, publishedAt } = article;

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow duration-300">
      <img src={image} alt={title} className="w-full h-56 object-cover" />
      <div className="p-4">
        <h2 className="text-xl font-semibold mb-2">{title}</h2>
        <p className="text-gray-700 text-sm mb-2">{description}</p>
        <div className="text-xs text-gray-500 flex justify-between">
          <span>{source}</span>
          <span>{new Date(publishedAt).toLocaleString()}</span>
        </div>
      </div>
    </div>
  );
};

export default FeedItem;