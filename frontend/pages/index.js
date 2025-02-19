import { useState, useEffect } from "react";
import { AppBar, Toolbar, Typography, Button, Dialog, DialogTitle, DialogContent, IconButton, Card, CardContent, Container } from "@mui/material";
import CloseIcon from "@mui/icons-material/Close";
import { Bar } from "react-chartjs-2";
import "chart.js/auto";

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || "http://localhost:8000";

export default function Home() {
    const [detectors, setDetectors] = useState([]);
    const [openModal, setOpenModal] = useState(false);
    const [selectedDetector, setSelectedDetector] = useState(null);
    
    useEffect(() => {
        const fetchDetectors = async () => {
            try {
                const res = await fetch(`${BACKEND_URL}/api/detectors`);
                if (!res.ok) throw new Error("Failed to fetch detectors");
                const data = await res.json();
                setDetectors(data.results || []);
            } catch (err) {
                console.error("Error fetching detectors:", err);
            }
        };
        fetchDetectors();
    }, []);
    
    const handleOpenModal = (detector) => {
        setSelectedDetector(detector);
        setOpenModal(true);
    };

    const handleCloseModal = () => {
        setOpenModal(false);
        setSelectedDetector(null);
    };

    return (
        <div className="min-h-screen bg-gray-100">
            {/* App Bar with Centered Logo */}
            <AppBar position="static" sx={{ backgroundColor: "#000", padding: 2 }}>
                <Toolbar sx={{ flexDirection: "column", alignItems: "center" }}>
                    <img src="/4ward_logo.jpg" alt="IntelliOptics & 4wardmotion Solutions Logo" className="h-16 mb-2" />
                    <Typography variant="h4" component="div" sx={{ color: "white", fontWeight: "bold", textAlign: "center" }}>
                        IntelliOptics Dashboard
                    </Typography>
                </Toolbar>
            </AppBar>

            {/* Container for Detectors */}
            <Container sx={{ mt: 4 }}>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {detectors.length > 0 ? (
                        detectors.map((detector) => (
                            <Card key={detector.id} className="shadow-lg p-4">
                                <CardContent>
                                    <Typography variant="h6" fontWeight="bold">{detector.name}</Typography>
                                    <Typography>ID: {detector.id}</Typography>
                                    <Typography>Query: {detector.query || "N/A"}</Typography>
                                    <Typography>Group: {detector.group_name || "N/A"}</Typography> {/* Group Added Here */}
                                    <Typography>Confidence: {detector.confidence_threshold * 100}%</Typography>
                                    <Typography>Status: {detector.status}</Typography>
                                    <Button variant="contained" color="primary" sx={{ mt: 2 }} onClick={() => handleOpenModal(detector)}>
                                        View Accuracy Details
                                    </Button>
                                </CardContent>
                            </Card>
                        ))
                    ) : (
                        <Typography variant="h6" sx={{ textAlign: "center", mt: 4 }}>No Detectors Found</Typography>
                    )}
                </div>
            </Container>

            {/* Accuracy Details Modal */}
            {selectedDetector && (
                <Dialog open={openModal} onClose={handleCloseModal} maxWidth="md" fullWidth>
                    <DialogTitle>
                        {selectedDetector.name} - Accuracy Details
                        <IconButton
                            edge="end"
                            color="inherit"
                            onClick={handleCloseModal}
                            aria-label="close"
                            sx={{ position: "absolute", right: 10, top: 10 }}
                        >
                            <CloseIcon />
                        </IconButton>
                    </DialogTitle>
                    <DialogContent>
                        <Typography fontWeight="bold">Group: {selectedDetector.group_name || "N/A"}</Typography> {/* Group Added Here */}
                        <Typography fontWeight="bold">Projected Accuracy: {selectedDetector.projected_accuracy || "N/A"}%</Typography>
                        <Typography fontWeight="bold" color="green">ML Accuracy for "YES": {selectedDetector.accuracy_yes || "N/A"}%</Typography>
                        <Typography fontWeight="bold" color="red">ML Accuracy for "NO": {selectedDetector.accuracy_no || "N/A"}%</Typography>

                        <Bar
                            data={{
                                labels: ["YES", "NO"],
                                datasets: [
                                    {
                                        label: "Accuracy %",
                                        data: [selectedDetector.accuracy_yes, selectedDetector.accuracy_no],
                                        backgroundColor: ["#4CAF50", "#F44336"], // Green for YES, Red for NO
                                    },
                                ],
                            }}
                            options={{
                                responsive: true,
                                scales: {
                                    y: { beginAtZero: true, max: 100 },
                                },
                            }}
                        />
                    </DialogContent>
                </Dialog>
            )}
        </div>
    );
}
