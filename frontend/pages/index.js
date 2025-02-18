import { useState, useEffect } from "react";
import { io } from "socket.io-client";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL || "http://localhost:8000/socket.io";
const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || "IntelliOptics Dashboard";

export default function Home() {
  const [detectors, setDetectors] = useState([]);
  const [search, setSearch] = useState("");
  const [selectedDetector, setSelectedDetector] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchDetectors = async () => {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${BACKEND_URL}/api/detectors`);
        if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
        const data = await res.json();
        setDetectors(data.results || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDetectors();

    const socket = io(SOCKET_URL, { transports: ["websocket", "polling"] });
    socket.on("update", (data) => setDetectors(data.results || []));
    return () => socket.disconnect();
  }, []);

  const filteredDetectors = detectors.filter((detector) =>
    detector.name.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="p-6 bg-gray-100 min-h-screen">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">{APP_NAME}</h1>
      <input
        type="text"
        placeholder="Search detectors..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="w-full p-2 border border-gray-300 rounded-lg mb-4"
      />

      {loading ? (
        <p className="text-center">Loading detectors...</p>
      ) : error ? (
        <p className="text-red-500 text-center">{error}</p>
      ) : (
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDetectors.map((detector) => (
            <div key={detector.id} className="p-6 bg-white shadow-md rounded-lg">
              <h2 className="text-xl font-semibold text-gray-800">{detector.name}</h2>
              <p className="text-gray-600">ID: {detector.id}</p>
              <p className="text-gray-600">Query: {detector.query || "N/A"}</p>
              <p className="text-gray-600">Group: {detector.group_name || "N/A"}</p>
              <p className="text-gray-600">
                Confidence: {detector.confidence_threshold ? `${detector.confidence_threshold * 100}%` : "N/A"}
              </p>
              <p className={`font-semibold ${detector.status === "ON" ? "text-green-500" : "text-red-500"}`}>
                Status: {detector.status}
              </p>

              <button
                className="mt-4 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
                onClick={() => setSelectedDetector(detector)}
              >
                View Accuracy Details
              </button>
            </div>
          ))}
        </div>
      )}

      {selectedDetector && (
        <div className="fixed inset-0 bg-gray-900 bg-opacity-50 flex justify-center items-center">
          <div className="bg-white p-6 rounded-lg shadow-lg w-2/3 max-w-2xl">
            <h2 className="text-xl font-bold mb-2">{selectedDetector.name} - Accuracy Details</h2>
            <p><strong>Projected Accuracy:</strong> 80%</p>
            <p><strong>ML Accuracy for "YES":</strong> 94%</p>
            <p><strong>ML Accuracy for "NO":</strong> 67%</p>

            {/* Fixed Bar Chart with Explicit Colors */}
            <ResponsiveContainer width="100%" height={250}>
              <BarChart
                data={[
                  { name: "YES", accuracy: 94, fill: "#4CAF50" },  // Explicitly assign green
                  { name: "NO", accuracy: 67, fill: "#F44336" },   // Explicitly assign red
                ]}
              >
                <XAxis dataKey="name" stroke="#4A5568" />
                <YAxis domain={[0, 100]} stroke="#4A5568" />
                <Tooltip />
                <Legend />
                <Bar dataKey="accuracy" fillKey="fill" />
              </BarChart>
            </ResponsiveContainer>

            <button
              className="mt-4 px-4 py-2 bg-gray-600 text-white rounded-lg hover:bg-gray-700"
              onClick={() => setSelectedDetector(null)}
            >
              Close
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
