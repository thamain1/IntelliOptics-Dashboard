import { useState, useEffect } from "react";
import { io } from "socket.io-client";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";
const SOCKET_URL = process.env.NEXT_PUBLIC_SOCKET_URL || "http://localhost:8000/socket.io";
const APP_NAME = process.env.NEXT_PUBLIC_APP_NAME || "IntelliOptics Dashboard";

export default function Home() {
    const [detectors, setDetectors] = useState([]);
    const [search, setSearch] = useState("");
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(true);

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
                console.log("API Response:", data);

                if (data.results && Array.isArray(data.results)) {
                    setDetectors(data.results);
                } else {
                    setError("Unexpected API response format");
                }
            } catch (err) {
                console.error("Error fetching detectors:", err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchDetectors();

        const socket = io(SOCKET_URL, {
            transports: ["websocket", "polling"],
        });

        socket.on("connect", () => {
            console.log("Connected to WebSocket server");
        });

        socket.on("update", (data) => {
            console.log("Received update:", data);
            if (data.results && Array.isArray(data.results)) {
                setDetectors(data.results);
            }
        });

        socket.on("disconnect", () => {
            console.log("Disconnected from WebSocket server");
        });

        return () => {
            socket.disconnect();
        };
    }, []);

    if (loading) return <div className="text-center mt-10 text-xl">Loading detectors...</div>;
    if (error) return <div className="text-center mt-10 text-xl text-red-500">Error: {error}</div>;

    return (
        <div className="p-6 max-w-6xl mx-auto">
            <h1 className="text-3xl font-bold mb-4">{APP_NAME}</h1>
            <input
                type="text"
                placeholder="Search detectors..."
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                className="w-full p-2 border rounded-lg mb-4"
            />
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
                {detectors.map((detector) => (
                    <div key={detector.id} className="p-4 border rounded-lg shadow-lg bg-white">
                        <h2 className="text-xl font-semibold">{detector.name}</h2>
                        <p className={`text-gray-600 ${detector.status === "ON" ? "text-green-500" : "text-red-500"}`}>
                            Status: {detector.status}
                        </p>
                        <p className="text-gray-600">Confidence Threshold: {detector.confidence_threshold * 100}%</p>
                        <p className="text-gray-600">Query: {detector.query}</p>
                    </div>
                ))}
            </div>
        </div>
    );
}
