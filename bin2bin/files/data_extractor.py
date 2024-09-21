#lotto dependencies for python programs. 
from importlib.metadata import distribution
from pydoc import pathdirs

import httpx
import json

# Replace this URL with the actual API endpoint you found
url = "https://www.njlottery.com/api/v1/instant-games/games/?size=1000&_=1726803357743"

# Send a GET request to the API
response = httpx.get(url)

# Check if the request was successful
if response.status_code == 200:
    try:
        data = response.json()
        print(json.dumps(data, indent=4))  # Pretty-print the JSON response
        
        # Ensure data is a list
        if isinstance(data, list):
            print("Data is a list.")
        else:
            print("Unexpected data format. Expected a list.")
    except json.JSONDecodeError:
        print("Failed to parse JSON response.")
else:
    print(f"Failed to retrieve data. Status code: {response.status_code}")
cript.
