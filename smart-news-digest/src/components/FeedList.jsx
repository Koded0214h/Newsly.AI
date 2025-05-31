import React from 'react';
import FeedItem from './FeedItem';

const dummyData = [
  {
    id: 1,
    title: "AI is Revolutionizing Global Finance",
    description: "Here's how artificial intelligence is transforming how money moves around the world.",
    source: "Bloomberg",
    image: "https://source.unsplash.com/600x400/?ai,finance",
    publishedAt: "2025-05-27T08:00:00Z"
  },
  {
    id: 2,
    title: "Breaking News: Currency Shifts in West Africa",
    description: "The CFA franc may soon be replaced by a new regional currency.",
    source: "Al Jazeera",
    image: "https://source.unsplash.com/600x400/?money,africa",
    publishedAt: "2025-05-26T18:30:00Z"
  },
  {
    id: 3,
    title: "Breaking News: Currency Shifts in West Africa",
    description: "The CFA franc may soon be replaced by a new regional currency.",
    source: "Al Jazeera",
    image: "https://source.unsplash.com/600x400/?money,africa",
    publishedAt: "2025-05-26T18:30:00Z"
  }
];

const FeedList = () => {
  return (
    <div className="grid gap-6">
      {dummyData.map(item => (
        <FeedItem key={item.id} article={item} />
      ))}
    </div>
  );
};

export default FeedList;