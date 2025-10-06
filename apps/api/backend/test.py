from groundlight import Groundlight

gl = Groundlight()
detectors = gl.list_detectors()

print("API Response:", detectors.__dict__)  # Print the full response
