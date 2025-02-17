import { useState, useEffect } from "react";
import { io } from "socket.io-client";
import {
  Dialog,
  DialogTrigger,
  DialogContent,
  DialogTitle,
  DialogClose,
} from "@radix-ui/react-dialog";
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL || "http://localhost:8000/socket.io";
const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || "IntelliOptics Dashboard";

export default function Home() {
  const [detectors, setDetectors] = useState([]);
  const [search, setSearch] = useState("");
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedDetector, setSelectedDetector] = useState(null);

  useEffect(() => {
    const fetchDetectors = async () => {
      setLoading(true);
      setError(null);

      try {
        const res = await fetch(`${BACKEND_URL}/api/detectors`);
        if (!res.ok) {
          const errorData = await res.json();
          throw new Error(errorData.error || `HTTP error! status: ${res.status}`);
        }

        const data = await res.json();
        console.log("Full API Response:", data);

        if (data.results && Array.isArray(data.results)) {
          setDetectors(data.results);
        } else {
          console.error("API Error:", data.error);
          setError(data.error || "Unexpected API response format");
        }
      } catch (err) {
        console.error("Error fetching detectors:", err);
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchDetectors();

    const socket = io(SOCKET_URL, { transports: ["websocket", "polling"] });

    socket.on("connect", () => console.log("Connected to WebSocket server"));
    socket.on("update", (data) => {
      if (data.results && Array.isArray(data.results)) {
        setDetectors(data.results);
      } else {
        console.error("Unexpected update data format:", data);
      }
    });
    socket.on("disconnect", () => console.log("Disconnected from WebSocket server"));

    return () => socket.disconnect();
  }, []);

  const filteredDetectors = detectors.filter((detector) =>
    detector.name.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) return <div className="text-center text-xl mt-6">Loading detectors...</div>;
  if (error) return <div className="text-center text-red-500 mt-6">Error: {error}</div>;

  return (
    <div className="p-6 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-4">{APP_NAME}</h1>

      <input
        type="text"
        placeholder="Search detectors..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        className="mt-4 p-3 border rounded-md w-full text-lg shadow-md"
      />

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
        {filteredDetectors.length > 0 ? (
          filteredDetectors.map((detector) => (
            <div key={detector.id} className="p-6 bg-white shadow-lg rounded-xl border border-gray-200">
              <h2 className="text-xl font-semibold text-blue-700">{detector.name}</h2>
              <p className="text-gray-600">ID: {detector.id}</p>
              <p className="text-gray-600">Query: {detector.query || "N/A"}</p>
              <p className="text-gray-600">Group: {detector.group_name || "Default"}</p>
              <p className="text-gray-600">
                Confidence:{" "}
                <span className="font-bold">{(detector.confidence_threshold * 100 || 0).toFixed(2)}%</span>
              </p>
              <p className={`font-bold ${detector.status === "ON" ? "text-green-500" : "text-red-500"}`}>
                Status: {detector.status}
              </p>

              {/* Accuracy Details Button */}
              <Dialog>
                <DialogTrigger asChild>
                  <button
                    className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md w-full hover:bg-blue-700 transition"
                    onClick={() => setSelectedDetector(detector)}
                  >
                    View Accuracy Details
                  </button>
                </DialogTrigger>
                {selectedDetector && (
                  <DialogContent className="p-6 bg-white shadow-2xl rounded-lg max-w-2xl mx-auto">
                    <DialogTitle className="text-xl font-semibold text-gray-900">
                      {selectedDetector.name} - Accuracy Details
                    </DialogTitle>

                    <div className="mt-4 border-t pt-4">
                      <p className="text-gray-700 text-lg">
                        <strong>Projected Accuracy:</strong> 80%
                      </p>
                      <p className="text-green-500 text-lg">
                        <strong>ML Accuracy for "YES":</strong> 94%
                      </p>
                      <p className="text-red-500 text-lg">
                        <strong>ML Accuracy for "NO":</strong> 67%
                      </p>
                    </div>

                    {/* Accuracy Chart */}
                    <ResponsiveContainer width="100%" height={300}>
                      <BarChart data={[{ yes: 94, no: 67, projected: 80 }]}>
                        <XAxis dataKey="name" />
                        <YAxis />
                        <Tooltip />
                        <Bar dataKey="yes" fill="#34D399" name="ML Accuracy YES" />
                        <Bar dataKey="no" fill="#F87171" name="ML Accuracy NO" />
                        <Bar dataKey="projected" fill="#3B82F6" name="Projected Accuracy" />
                      </BarChart>
                    </ResponsiveContainer>

                    <DialogClose asChild>
                      <button className="mt-6 bg-gray-500 text-white px-4 py-2 rounded-md w-full hover:bg-gray-600 transition">
                        Close
                      </button>
                    </DialogClose>
                  </DialogContent>
                )}
              </Dialog>
            </div>
          ))
        ) : (
          <p className="text-gray-600 mt-4 text-lg text-center">No detectors found.</p>
        )}
      </div>
    </div>
  );
}
