from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from pydantic import BaseModel
from groundlight import Groundlight
import uvicorn
import os
import json

# Initialize FastAPI
app = FastAPI()
socket_manager = SocketManager(app=app, mount_location="/socket.io")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Check if Groundlight API token is set
api_token = os.getenv("GROUNDLIGHT_API_TOKEN")
if not api_token:
    print("❌ GROUNDLIGHT_API_TOKEN is not set! Please check your environment variables.")
    exit()

# Initialize Groundlight Client
try:
    gl = Groundlight(api_token=api_token)
    print("✅ Successfully connected to Groundlight API.")
except Exception as e:
    print(f"❌ Error initializing Groundlight API: {e}")
    gl = None

# Define a response model
class DetectorResponse(BaseModel):
    id: str
    name: str
    status: str
    query: str
    group_name: str
    confidence_threshold: float
    patience_time: float
    mode: str
    escalation_type: str
    created_at: str
    accuracy: float | None
    accuracy_details: dict | None

@app.get("/api/detectors")
def get_detectors():
    if gl is None:
        return {"error": "Groundlight API initialization failed."}

    try:
        detectors_response = gl.list_detectors()
        if not detectors_response.results:
            return {"error": "No detectors found"}

        parsed_detectors = []
        for d in detectors_response.results:
            # Fetch accuracy details dynamically (if available)
            accuracy_data = getattr(d, "accuracy_details", None)
            parsed_detectors.append({
                "id": d.id,
                "name": d.name,
                "status": d.status.value if hasattr(d.status, "value") else str(d.status),
                "query": d.query,
                "group_name": d.group_name,
                "confidence_threshold": d.confidence_threshold,
                "patience_time": d.patience_time,
                "mode": d.mode.value if hasattr(d.mode, "value") else str(d.mode),
                "escalation_type": d.escalation_type.value if hasattr(d.escalation_type, "value") else str(d.escalation_type),
                "created_at": str(d.created_at),
                "accuracy": accuracy_data.get("projected_accuracy") if accuracy_data else None,
                "accuracy_details": accuracy_data if accuracy_data else None,
            })

        return {"results": parsed_detectors}

    except Exception as e:
        return {"error": f"Failed to fetch detectors: {e}"}

# WebSocket for live updates
@socket_manager.on("update_request")
async def send_update(sid, data):
    detectors = get_detectors()
    await socket_manager.emit("update", detectors)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
