import requests
import json

# Define the URL of the microservice
url = 'http://127.0.0.1/supercut'

# Define the payload with the video URL, timestamps, and output URL
payload = {
    "video_url": "gs://cloud-racer/data/raw_data/yolov8n-car_front-rear-2023_London_Highlights.mp4",
    "timestamps": [[0, 10], [30, 40], [50, 60]],
    "output_url": "gs://cloud-racer/processed/supercut.mp4"
}

# Convert the payload to JSON
data = json.dumps(payload)

# Define headers
headers = {
    'Content-Type': 'application/json'
}

# Send the POST request
response = requests.post(url, headers=headers, data=data)

# Print the response
print("Status Code:", response.status_code)
print("Response JSON:", response.json())