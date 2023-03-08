import datetime
import json

# Define the filename of the AAPL data collected by collect_data.py
aapl_data_file = "data/aapl_data.json"

# Load the AAPL data from the file
with open(aapl_data_file, "r") as f:
    data = json.load(f)

# Extract the "results" data from the response
results = data["results"]


# * Q1 
def compute_rolling_avg_close_price():
    # Initialize the rolling average window and sum
    window = []
    window_sum = 0
    rolling_avg_closing_price_20mins = {}

    
    # Loop through each result and compute the rolling average 'close' price
    for i, result in enumerate(results):
        # Parse the timestamp and close price from the result
        timestamp = datetime.datetime.fromtimestamp(result["t"] / 1000)
        close_price = result["c"]
        
        # Add the close price to the rolling average window and sum
        window.append(close_price)
        window_sum += close_price
        
        # If the window size is greater than 20, remove the oldest value from the window and sum
        if len(window) > 20:
            window_sum -= window.pop(0)
        
        # If the window size is 20, compute and print the rolling average 'close' price
        if len(window) == 20:
            rolling_avg_close_price = window_sum / 20
            print(f"{timestamp}: {rolling_avg_close_price}")
            rolling_avg_closing_price_20mins[timestamp] = rolling_avg_close_price
            
    
    return rolling_avg_closing_price_20mins

print("20 mins rolling avg closing price")
rolling_avg_closing_price_20mins =  compute_rolling_avg_close_price()



# *Q2 

def resample_data(granularity):
    # Define a dictionary to store the resampled data
    resampled_data = {}
    
    # Loop through each result and resample the data
    for result in results:
        # Parse the timestamp and the open, high, low, and close prices from the result
        timestamp = datetime.datetime.fromtimestamp(result["t"] / 1000)
        open_price = result["o"]
        high_price = result["h"]
        low_price = result["l"]
        close_price = result["c"]
        
        # Determine the resample key based on the granularity
        if granularity == "hour":
            resample_key = timestamp.replace(minute=0, second=0, microsecond=0)
        elif granularity == "day":
            resample_key = timestamp.replace(hour=0, minute=0, second=0, microsecond=0)
        else:
            raise ValueError("granularity should be hour or day")
        
        # If the resample key is not in the resampled data dictionary, initialize the open, high, low, and close values
        if resample_key not in resampled_data:
            resampled_data[resample_key] = {
                "open": open_price,
                "high": high_price,
                "low": low_price,
                "close": close_price
            }
        # Otherwise, update the open, high, low, and close values if necessary
        else:
            if open_price < resampled_data[resample_key]["open"]:
                resampled_data[resample_key]["open"] = open_price
                
            if high_price > resampled_data[resample_key]["high"]:
                resampled_data[resample_key]["high"] = high_price
                
            if low_price < resampled_data[resample_key]["low"]:
                resampled_data[resample_key]["low"] = low_price
                
            resampled_data[resample_key]["close"] = close_price
    
    # Print the resampled data
    for key in sorted(resampled_data.keys()):
        print(f"{key}: Open={resampled_data[key]['open']}, High={resampled_data[key]['high']}, Low={resampled_data[key]['low']}, Close={resampled_data[key]['close']}")
        
        
    return(resampled_data)

print("resample to 1 hour")
resample_data_to_hour = resample_data("hour")

print("resample to 1 day")
resample_data_to_day = resample_data("day")