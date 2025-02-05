import React, { useState } from "react";
import axios from "axios";

function App() {
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // Call API to check for new jobs immediately
  const checkNewJobs = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await axios.get("http://localhost:5000/check_new_job");
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error checking for new jobs");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  // Call API to schedule periodic job checks
  const scheduleJobChecks = async () => {
    setLoading(true);
    setMessage("");

    try {
      const response = await axios.get("http://localhost:5000/main");
      setMessage(response.data.message);
    } catch (error) {
      setMessage("Error scheduling job checks");
      console.error(error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1>Job Crawler Dashboard</h1>
      <button onClick={checkNewJobs} disabled={loading} style={styles.button}>
        {loading ? "Checking..." : "Check for New Jobs"}
      </button>
      <button onClick={scheduleJobChecks} disabled={loading} style={styles.button}>
        {loading ? "Scheduling..." : "Schedule Job Checks"}
      </button>
      {message && <p style={styles.message}>{message}</p>}
    </div>
  );
}

const styles = {
  container: {
    textAlign: "center",
    marginTop: "50px",
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
