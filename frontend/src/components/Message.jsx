function Message({ role, text }) {
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

      <p>{text}</p>
    </div>
  );
}

export default Message;