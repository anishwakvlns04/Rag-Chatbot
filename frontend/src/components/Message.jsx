function Message({
  role,
  text,
  sources
}) {
 const displaySources =
  sources || [];

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
        displaySources.length > 0&& (
          <div className="mt-3 border-t pt-2">

            <p className="text-xs font-semibold text-gray-500">
              Sources
            </p>

            <div className="flex gap-2 flex-wrap mt-2">

              {displaySources.map(
                (source, index) => (
                  <span
                    key={index}
                    className={`px-2 py-1 rounded-full text-xs font-medium ${
                      source.video_id === "A"
                        ? "bg-blue-100 text-blue-700"
                        : "bg-green-100 text-green-700"
                    }`}
                  >
                    Video {source.video_id} - Chunk {source.chunk_index}
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