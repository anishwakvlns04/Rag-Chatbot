import { useState } from "react";
import VideoCard from "./components/VideoCard";
import ChatPanel from "./components/ChatPanel";

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [instagramUrl, setInstagramUrl] = useState("");

  const videoA = {
    title: "YouTube Video",
    creator: "Creator A",
    views: 10000,
    likes: 800,
    comments: 50,
    engagementRate: 8.5,
    thumbnail:
      "https://via.placeholder.com/400x200",
  };

  const videoB = {
    title: "Instagram Reel",
    creator: "Creator B",
    views: 15000,
    likes: 900,
    comments: 60,
    engagementRate: 6.4,
    thumbnail:
      "https://via.placeholder.com/400x200",
  };

  return (
    <div className="min-h-screen bg-gray-100 p-6">
      <div className="max-w-7xl mx-auto">
        <h1 className="text-4xl font-bold text-center mb-8">
          Video Engagement Analyzer
        </h1>

        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="space-y-4">
            <input
              type="text"
              placeholder="YouTube URL"
              value={youtubeUrl}
              onChange={(e) =>
                setYoutubeUrl(e.target.value)
              }
              className="w-full border p-3 rounded-lg"
            />

            <input
              type="text"
              placeholder="Instagram Reel URL"
              value={instagramUrl}
              onChange={(e) =>
                setInstagramUrl(e.target.value)
              }
              className="w-full border p-3 rounded-lg"
            />

            <button className="w-full bg-black text-white p-3 rounded-lg">
              Analyze Videos
            </button>
          </div>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <VideoCard video={videoA} />
          <VideoCard video={videoB} />
        </div>

        <ChatPanel />
      </div>
    </div>
  );
}

export default App;