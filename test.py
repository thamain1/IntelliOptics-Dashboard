import os
from dotenv import load_dotenv
import groundlight

load_dotenv()

GROUNDLIGHT_API_TOKEN = os.getenv("GROUNDLIGHT_API_TOKEN")

try:
    gl = groundlight.Groundlight(api_token=GROUNDLIGHT_API_TOKEN)  # Corrected line
    detectors_response = gl.list_detectors()

    print(detectors_response)
    print(detectors_response.__dict__)
    if detectors_response.results:
        print("Detectors found!")
        for detector in detectors_response.results:
            print(detector.name)
    else:
        print("No detectors found.")
except Exception as e:
    print(f"Error: {e}")