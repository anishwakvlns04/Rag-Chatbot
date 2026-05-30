function Message({
  role,
  text,
  sources
}) {
  const uniqueVideos = sources
    ? [...new Set(
        sources.map(
          (source) => source.video_id
        )
      )]
    : [];

  return (
    <div
      className={`p-3 rounded-lg mb-2 ${
        role === "user"
          ? "bg-blue-100"
          : "bg-gray-100"
      }`}
    >
      <p className="font-semibold capitalize">
        {role}
      </p>

      <p className="mt-1 whitespace-pre-wrap">
        {text}
      </p>

      {role === "assistant" &&
        uniqueVideos.length > 0 && (
          <div className="mt-3 border-t pt-2">

            <p className="text-xs font-semibold text-gray-500">
              Sources
            </p>

            <div className="flex gap-2 flex-wrap mt-2">

              {uniqueVideos.map(
                (videoId, index) => (
                  <span
                    key={index}
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      videoId === "A"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-green-100 text-green-700"
                    }`}
                  >
                    Video {videoId}
                  </span>
                )
              )}

            </div>

          </div>
        )}
    </div>
  );
}

export default Message;