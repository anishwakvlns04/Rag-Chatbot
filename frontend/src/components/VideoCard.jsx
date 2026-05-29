function VideoCard({ video }) {
  return (
    <div className="bg-white rounded-xl shadow-md p-4">
      <img
        src={video.thumbnail}
        alt={video.title}
        className="w-full h-35 object-cover rounded-lg"
      />

      <h2 className="text-xl font-semibold mt-3">
        {video.title}
      </h2>

      <p className="text-gray-600">
        Creator: {video.creator}
      </p>

      <div className="mt-3 space-y-1 text-sm">
        <p>Views: {video.views}</p>
        <p>Likes: {video.likes}</p>
        <p>Comments: {video.comments}</p>
        <p>
          Engagement Rate: {video.engagementRate}%
        </p>
      </div>
    </div>
  );
}

export default VideoCard;