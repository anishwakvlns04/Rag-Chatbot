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
          video_a_url: youtubeUrl,
          video_b_url: instagramUrl,
        }
      );

      console.log(response.data);
const meta =
  response.data.videoA.metadata;

setVideoA({
  title: meta.title || "Video Unavailable",
  creator: meta.creator || "Unknown",
  views: meta.views,
  likes: meta.likes,
  comments: meta.comments,

  engagementRate:
    meta.views > 0
      ? (
          ((meta.likes + meta.comments) /
            meta.views) *
          100
        ).toFixed(2) + "%"
      : "N/A",

  thumbnail: meta.thumbnail || null,
});
if (response.data.videoB) {

  const metaB =
    response.data.videoB.metadata;


 setVideoB({
  title: metaB.title || "Video Unavailable",
  creator: metaB.creator || "Unknown",
  views: metaB.views,
  likes: metaB.likes,
  comments: metaB.comments,

  engagementRate:
    metaB.views > 0
      ? (
          ((metaB.likes + metaB.comments) /
            metaB.views) *
          100
        ).toFixed(2) + "%"
      : "N/A",

  thumbnail: metaB.thumbnail || null,
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
          AI Video Analyzer
        </h1>

        <div className="bg-white rounded-xl shadow-md p-6 mb-6">
          <div className="space-y-4">
            <input
              type="text"
              placeholder="Video A URL (YouTube or Instagram)"
              value={youtubeUrl}
              onChange={(e) =>
                setYoutubeUrl(e.target.value)
              }
              className="w-full border p-3 rounded-lg"
            />

            <input
              type="text"
              placeholder="Video B URL (YouTube or Instagram)"
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

       <div className="grid lg:grid-cols-2 gap-8 mb-8">

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