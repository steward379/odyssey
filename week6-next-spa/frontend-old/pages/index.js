import { useEffect, useState } from "react";

const HomePage = () => {
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetch("/api/hello")
      .then((response) => response.json())
      .then((data) => setMessage(data.message));
  }, []);

  return (
    <div>
      <h1>Next.js Frontend</h1>
      <p>{message}</p>
    </div>
  );
};

export default HomePage;
