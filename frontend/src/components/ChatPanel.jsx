import { useState } from "react";
import axios from "axios";
import Message from "./Message";

function ChatPanel() {
  const [question, setQuestion] = useState("");

  const [messages, setMessages] = useState([
    {
      role: "assistant",
      text: "Ask me anything about the video.",
    },
  ]);

  const handleSend = async () => {
    if (!question.trim()) return;

    const userMessage = {
      role: "user",
      text: question,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const response = await axios.post(
        "http://localhost:8000/chat",
        {
          question,
        }
      );

     const aiMessage = {
  role: "assistant",
  text: response.data.answer,
  sources: response.data.sources,
};

      setMessages((prev) => [
        ...prev,
        aiMessage,
      ]);
    } catch (error) {
      console.error(error);

      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Error contacting backend",
        },
      ]);
    }

    setQuestion("");
  };

  return (
    <div className="bg-white rounded-xl shadow-md p-4">
      <h2 className="text-xl font-semibold mb-4">
        Chat
      </h2>

      <div className="h-96 overflow-y-auto">
        {messages.map((msg, index) => (
          <Message
            key={index}
            role={msg.role}
            text={msg.text}
            sources={msg.sources}
          />
        ))}
      </div>

      <div className="flex gap-2 mt-4">
        <input
          type="text"
          value={question}
          onChange={(e) =>
            setQuestion(e.target.value)
          }
          placeholder="Ask a question..."
          className="flex-1 border rounded-lg p-3"
        />

        <button
          onClick={handleSend}
          className="bg-black text-white px-5 rounded-lg"
        >
          Send
        </button>
      </div>
    </div>
  );
}

export default ChatPanel;