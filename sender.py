import requests

# URL of the Django view
url = "http://127.0.0.1:8000/database/add_measurement/"

# The data to send to the API
data = {
    'HR': '10',
    'saturation': '88',
    'temperature': '36',
    'patient': '2'
}

# Send the POST request
response = requests.post(url, data=data)

# Print response status and content
print(response.status_code)
print(response.json())