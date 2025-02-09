import React, { useState } from "react";
import axios from "axios";

function App() {
  const [email, setEmail] = useState("");  // Store user email
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Handle API call to /main with user email
  const startJobScheduler = async () => {
    if (!email) { 
    
      setMessage("Please enter your email.");
      return;
    }

    setLoading(true);
    setMessage("");

    try {
      const response = await axios.post("http://localhost:5000/main", {
        email: email,
      });
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error starting job scheduler.");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Job Crawler Dashboard</h1>
      
      {/* Email Input Field */}
      <input
        type="email"
        placeholder="Enter your email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        style={styles.input}
      />

      {/* Start Job Scheduler Button */}
      <button onClick={startJobScheduler} disabled={loading} style={styles.button}>
        {loading ? "Starting..." : "Start Job Scheduler"}
      </button>

      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

// Styling
const styles = {
  container: {
    textAlign: "center",
    marginTop: "50px",
  },
  input: {
    padding: "10px",
    fontSize: "16px",
    width: "250px",
    marginBottom: "10px",
    borderRadius: "5px",
    border: "1px solid #ccc",
    textAlign: "center",
  },
  button: {
    padding: "10px 20px",
    fontSize: "16px",
    cursor: "pointer",
    border: "none",
    backgroundColor: "#007bff",
    color: "white",
    borderRadius: "5px",
    margin: "10px",
  },
  message: {
    marginTop: "20px",
    fontSize: "18px",
  },
};

export default App;
