import { useState } from "react";
import axios from "axios";

import VideoCard from "./components/VideoCard";
import ChatPanel from "./components/ChatPanel";

function App() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [instagramUrl, setInstagramUrl] = useState("");

  const [videoA, setVideoA] = useState(null);
  const [videoB, setVideoB] = useState(null);

  const [loading, setLoading] = useState(false);

  const analyzeVideos = async () => {
    try {
      setLoading(true);

      const response = await axios.post(
        "http://localhost:8000/analyze",
        {
          youtube_url: youtubeUrl,
          instagram_url: instagramUrl,
        }
      );

      console.log(response.data);
const meta =
  response.data.videoA.metadata;

setVideoA({
  title: meta.title,
  creator: meta.creator,
  views: meta.views,
  likes: meta.likes,
  comments: meta.comments,
  engagementRate: (
    ((meta.likes + meta.comments) / meta.views) *
    100
  ).toFixed(2),
  thumbnail: meta.thumbnail,
});
if (response.data.videoB) {

  const metaB =
    response.data.videoB.metadata;

  setVideoB({
    title: metaB.title,
    creator: metaB.creator,
    views: metaB.views,
    likes: metaB.likes,
    comments: metaB.comments,
    engagementRate: (
      ((metaB.likes + metaB.comments) /
        metaB.views) *
      100
    ).toFixed(2),
    thumbnail: metaB.thumbnail,
  });
}

    } catch (error) {
      console.error(error);
      alert("Analysis Failed");
    } finally {
      setLoading(false);
    }
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

            <button
              onClick={analyzeVideos}
              className="w-full bg-black text-white p-3 rounded-lg"
            >
              {loading
                ? "Analyzing..."
                : "Analyze Videos"}
            </button>
          </div>
        </div>

       <div className="grid md:grid-cols-2 gap-6 mb-6">

  {videoA && (
    <VideoCard video={videoA} />
  )}

  {videoB && (
    <VideoCard video={videoB} />
  )}

</div>

        <ChatPanel />
      </div>
    </div>
  );
}

export default App;