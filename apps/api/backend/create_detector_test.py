from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_socketio import SocketManager
from pydantic import BaseModel
from groundlight import Groundlight
import uvicorn
import os
import json

app = FastAPI()
socket_manager = SocketManager(app=app, mount_location="/socket.io")

origins = [
    "http://localhost",  # Or your frontend's URL
    "http://localhost:3000",  # If using port 3000
    "*"  # Be more specific in production
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_token = os.getenv("GROUNDLIGHT_API_TOKEN")
if not api_token:
    print("❌ GROUNDLIGHT_API_TOKEN is not set! Please check your environment variables.")
    exit()

try:
    gl = Groundlight(api_token=api_token)
    print("✅ Successfully connected to Groundlight API.")
except Exception as e:
    print(f"❌ Error initializing Groundlight API: {e}")
    gl = None

class DetectorResponse(BaseModel):
    id: str
    name: str
    status: str
    result: str | None

@app.get("/api/detectors")
def get_detectors():
    print("🔄 Entering get_detectors() function...")

    if gl is None:
        print("❌ Groundlight client is not initialized.")
        return {"error": "Groundlight API initialization failed."}

    try:
        print("🔄 Calling gl.list_detectors()...")
        detectors_response = gl.list_detectors()

        print("🔍 Debug: Raw API Response from Groundlight:")
        print(json.dumps(detectors_response.__dict__, indent=4, default=str))

        if not detectors_response.results:  # Check if the 'results' list is empty
            print("⚠️ No detectors found from Groundlight API! Creating a new one...")
            try:
                # Create a new detector (replace with your desired name and query)
                new_detector = gl.create_detector(
                    name="My New Detector",  # Replace with a unique name
                    query="Is there a person in the image?", #Replace with your query
                )
                print(f"✅ Created new detector: {new_detector.name} (ID: {new_detector.id})")
                detectors_response = gl.list_detectors() #Retrieve the updated list of detectors
            except Exception as e:
                print(f"❌ Error creating detector: {e}")
                return {"error": f"Failed to create detector: {e}"}


        parsed_detectors = []
        for d in detectors_response.results:
            status = d.status.value if hasattr(d.status, "value") else str(d.status)
            parsed_detectors.append({
                "id": d.id,
                "name": d.name,
                "status": status,
                "result": None
            })

        print("✅ Successfully retrieved detectors:", json.dumps(parsed_detectors, indent=4))
        return {"results": parsed_detectors}

    except Exception as e:
        print(f"❌ Error retrieving detectors: {e}")
        return {"error": f"Failed to fetch detectors: {e}"}

# ... (rest of your code: WebSocket events, etc.)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)