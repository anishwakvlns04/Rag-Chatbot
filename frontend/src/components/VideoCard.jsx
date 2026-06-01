import { useState } from "react";

function VideoCard({ video }) {
  const [imageError, setImageError] = useState(false);
  const showThumbnail =
  video.thumbnail &&
  video.thumbnail !== "null" &&
  !imageError;

  return (
    <div className="bg-white rounded-xl shadow-md p-5 hover:shadow-lg transition">

      <div className="overflow-hidden rounded-lg">

        {showThumbnail ? (
          <img
            src={video.thumbnail}
            alt={video.title}
            className="w-full h-56 object-cover rounded-lg"
            onError={() => setImageError(true)}
          />
        ) : (
          <div className="w-full h-56 rounded-lg bg-gradient-to-br from-pink-500 via-purple-500 to-orange-400 flex flex-col items-center justify-center text-white">
            <div className="text-5xl">🎬</div>

            <div className="font-bold mt-2">
              Thumbnail Unavailable
            </div>
          </div>
        )}

      </div>

      <h2 className="text-lg font-bold mt-4 line-clamp-2">
        {video.title || "Video Unavailable"}
      </h2>

      <p className="text-gray-600 mt-1">
        Creator: {video.creator || "Unknown"}
      </p>

      <div className="mt-4 grid grid-cols-2 gap-3 text-sm">

        <div className="bg-gray-50 p-2 rounded">
          <p className="font-medium">Views</p>
          <p>{video.views ?? "N/A"}</p>
        </div>

        <div className="bg-gray-50 p-2 rounded">
          <p className="font-medium">Likes</p>
          <p>{video.likes ?? 0}</p>
        </div>

        <div className="bg-gray-50 p-2 rounded">
          <p className="font-medium">Comments</p>
          <p>{video.comments ?? 0}</p>
        </div>

        <div className="bg-gray-50 p-2 rounded">
          <p className="font-medium">
            Engagement
          </p>
          <p>
            {video.engagementRate || "N/A"}
          </p>
        </div>

      </div>

    </div>
  );
}

export default VideoCard;