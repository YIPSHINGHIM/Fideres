import json
import os

import requests
from dotenv import load_dotenv

# Define the API endpoint URLs
msft_url = "https://api.polygon.io/v2/aggs/ticker/MSFT/range/1/day/2022-01-01/2022-01-31"
aapl_url = "https://api.polygon.io/v2/aggs/ticker/AAPL/range/5/minute/2022-01-20/2022-01-30"
ibm_url = "https://api.polygon.io/v2/aggs/ticker/IBM/range/2/hour/2022-02-05/2022-02-10"



# Define the API key for authentication
load_dotenv()
api_key = os.getenv('API_KEY')


if api_key == None:
    raise ValueError("Please enter your API key to the api_key variable !")


# Define headers for API authentication
headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {api_key}"
}

# Define a function to retrieve data from the API and save it to a file
def retrieve_data(url, filename):
    # Send a GET request to the API endpoint
    response = requests.get(url, headers=headers)
    
    # If the response status code is not 200, raise an exception
    if response.status_code != 200:
        raise Exception(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
    
    # Parse the response JSON data
    data = json.loads(response.text)
    
    # Save the JSON data to a file
    with open(filename, "w") as f:
        json.dump(data, f)
    
    print(f"Data retrieved from {url} and saved to {filename}.")

# Retrieve data for MSFT and save it to a file
retrieve_data(msft_url, "data/msft_data.json")

# Retrieve data for AAPL and save it to a file
retrieve_data(aapl_url, "data/aapl_data.json")

# Retrieve data for IBM and save it to a file
retrieve_data(ibm_url, "data/ibm_data.json")

