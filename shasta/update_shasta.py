#This first chunk of code will grab the latest results from the website, save them to a seperate file,
#and then override the existing CSV files with the latest results.

# request the required databases
import requests, time, datetime, json, csv, pandas as pd, os

from datawrapper import Datawrapper

DATAWRAPPER_API_KEY = os.environ['DATAWRAPPER_API_KEY']

#Define the dw variable as the Datawrapper command with the API key
dw = Datawrapper(DATAWRAPPER_API_KEY)

#define custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

#set the website request with the custom headers
#IMPORTANT: The URL must be changed to the desired election
r = requests.get("https://results.enr.clarityelections.com/CA/Shasta/120178/332057/json/en/summary.json", headers=headers)

# Import the JSON
print(r.status_code)
r.raise_for_status()
print(r.headers)
print(r.text)
if not r.content:
    print("There's no data available")

#Converts the raw data to a JSON file
data = r.json()

# parses the raw python data into JSON data
json_object = json.dumps(data, indent=4)

# set the current date and time
timenow = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")

#set the name of the file
latest_file_name = f"shasta_results_{timenow}.json"

# write output to file
with open(latest_file_name, "w") as outfile:
    json.dump(data, outfile)

#Print out the name of the latest file
print("Latest filename:", latest_file_name)

# Read the watched contests
with open('watched_contests.txt', 'r') as f:
     watched_contests = [line.strip() for line in f.readlines()]

# Open the JSON file
with open(latest_file_name, 'r') as f:
     data = json.load(f)

# Iterate through the JSON data
for contest in data:
     # If the contest's name is in the watched contests list
     if contest['C'] in watched_contests:
          # Extract the 'C', 'CH', 'PCT', and 'V' values
          c_value = contest.get('C')
          ch_value = contest.get('CH')
          pct_value = contest.get('PCT')
          v_value = contest.get('V')

          # Prepare the data for writing to CSV
          rows = zip(ch_value, v_value, pct_value)

          # Set the name of the CSV file to match the contest
          clean_name = f"{c_value}_results_clean.csv"

          # Write to CSV
          with open(clean_name, 'w', newline='') as f:
               writer = csv.writer(f)
               writer.writerow(["Candidate", "Votes", "Pct."])  # Write header
               for row in rows:
                    writer.writerow(row)  # Write data rows

#This second part takes the updated results and updates the existing charts with the new data

#Open the results_file_names.txt and chart_ids.txt files
with open("results_file_names.txt", "r") as f_names, open("chart_ids.txt", "r") as f_ids:
    #Iterate through each line in both files together
    for file_name, chart_id in zip(f_names, f_ids):
        #assign a variable for both the file and the chart ID we're currently working with
        current_file_name = file_name.strip()
        current_id = chart_id.strip()
        #Print them out to double check
        print("Current File Name:", current_file_name)
        print("Current ID:", current_id)
        #assign the data from the current file to a variable
        df = pd.read_csv(
            current_file_name
        )
        #call datawrapper and replace the data in the chart with the updated data from the current file
        dw.add_data(
            chart_id=current_id,
            data=df
        )
        #Grab the latest date and time in the format "DD/MM/YYYY, HH:MM AM/PM"
        latest_time = datetime.datetime.now().strftime("%d/%m/%Y, %I:%M %p")
        
        #Update the chart to include the latest time the chart was updated
        dw.update_metadata(current_id,
            {
                "annotate": {
                    "notes": f"Last updated: {latest_time} PST"
                }
            }                  
        )
        #Republish the chart
        dw.publish_chart(current_id)
