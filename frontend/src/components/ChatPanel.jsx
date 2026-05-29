import Message from "./Message";

function ChatPanel() {
  const messages = [
    {
      role: "assistant",
      text: "Ask me anything about the videos.",
    },
  ];

  return (
    <div className="bg-white rounded-xl shadow-md p-4">
      <h2 className="text-xl font-semibold mb-4">
        Chat
      </h2>

      {messages.map((msg, index) => (
        <Message
          key={index}
          role={msg.role}
          text={msg.text}
        />
      ))}

      <input
        type="text"
        placeholder="Ask a question..."
        className="w-full mt-4 border rounded-lg p-3"
      />
    </div>
  );
}

export default ChatPanel;