# request the required databases
import requests, re, pandas as pd, time, datetime, json, csv

from datawrapper import Datawrapper

dw = Datawrapper(DATAWRAPPER_API_KEY)

#define custom headers
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36'
}

#set the website request with the custom headers
#IMPORTANT: The URL must be changed to the desired election
r = requests.get("https://results.enr.clarityelections.com/CA/Shasta/120178/332057/json/en/summary.json", headers=headers)

# Import the JSON
r.raise_for_status()

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

          # Append the clean name to the results_file_names.txt file
          with open("results_file_names.txt", "a") as f:
               f.write(clean_name + "\n")

          # Print the extracted values
          # print(f"Contest: {contest['C']}")
          # print(f"C: {c_value}")
          # print(f"CH: {ch_value}")
          # print(f"PCT: {pct_value}")
          # print(f"V: {v_value}")
          # print("-------------------------")

#This section is for creating new charts only. NOT for updating existing charts.
with open("results_file_names.txt", "r") as f:
    for line in f:
        current_results_chart = line.strip()
        # Read the CSV file
        df = pd.read_csv(
            current_results_chart
        )
        # Create a chart, the title of the chart is the first part of the filename
        chart_config = dw.create_chart(
            title = re.match(r"^(.*?)_", current_results_chart).group(1),
            chart_type='tables',
            data=df,
            folder_id='233686'
        )
        #Define the chart ID
        chart_id = chart_config["id"]
        #Update the description of the chart to include the source name, source URL, and byline
        dw.update_description(
            chart_id,
            source_name="Shasta County Elections Office",
            source_url="https://results.enr.clarityelections.com/CA/Shasta/120178/332057/json/en/summary.json",
            byline="Roman Battaglia | Jefferson Public Radio",
        )
        #Update the metadata of the chart to include the visualization properties that match what we're looking for
        properties = {
            'visualize': {'dark-mode-invert': True,
          'highlighted-series': [],
          'highlighted-values': [],
          'sharing': {'enabled': False,
            'url': 'https://www.datawrapper.de/_/fWcBt',
            'auto': False},
          'rows': {'row-0': {'style': {'bold': False,
              'color': False,
              'italic': False,
              'fontSize': 1,
              'underline': False,
              'background': False},
            'format': '0,0.[00]',
            'moveTo': 'top',
            'sticky': False,
            'moveRow': False,
            'stickTo': 'top',
            'borderTop': 'none',
            'borderBottom': 'none',
            'borderTopColor': '#333333',
            'overrideFormat': False,
            'borderBottomColor': '#333333'},
            'row--1': {'style': {'bold': False,
              'color': False,
              'italic': False,
              'fontSize': 1,
              'underline': False,
              'background': False},
            'format': '0,0.[00]',
            'moveTo': 'top',
            'sticky': False,
            'moveRow': False,
            'stickTo': 'top',
            'borderTop': 'none',
            'borderBottom': 'none',
            'borderTopColor': '#333333',
            'overrideFormat': False,
            'borderBottomColor': '#333333'}},
          'header': {'style': {'bold': True,
            'color': False,
            'italic': False,
            'fontSize': 1.1,
            'background': False},
            'borderTop': 'none',
            'borderBottom': '2px',
            'borderTopColor': '#333333',
            'borderBottomColor': '#333333'},
          'legend': {'size': 170,
            'title': '',
            'labels': 'ranges',
            'enabled': False,
            'reverse': False,
            'labelMax': 'high',
            'labelMin': 'low',
            'position': 'above',
            'interactive': False,
            'labelCenter': 'medium',
            'labelFormat': '0,0.[00]',
            'customLabels': []},
          'sortBy': 'Candidate',
          'columns': {'Pct.': {'style': {'bold': False,
              'color': False,
              'italic': False,
              'fontSize': 1,
              'underline': False,
              'background': False},
            'width': 0.2,
            'append': '',
            'format': '0.00%',
            'heatmap': {'enabled': False},
            'prepend': '',
            'barColor': '#5e5279',
            'barStyle': 'normal',
            'minWidth': 30,
            'sortable': True,
            'alignment': 'auto',
            'flagStyle': '1x1',
            'showAsBar': True,
            'sparkline': {'area': False,
              'type': 'line',
              'color': 0,
              'title': '',
              'format': '0.[0]a',
              'height': 20,
              'stroke': 2,
              'dotLast': True,
              'enabled': False,
              'colorNeg': 0,
              'dotFirst': True,
              'rangeMax': '',
              'rangeMin': '',
              'labelDiff': False},
            'borderLeft': 'none',
            'fixedWidth': False,
            'barRangeMax': '100',
            'barRangeMin': '',
            'borderRight': 'none',
            'compactMode': False,
            'customColor': False,
            'replaceFlags': False,
            'showOnMobile': True,
            'customColorBy': 0,
            'showOnDesktop': True,
            'customBarColor': False,
            'barNoBackground': False,
            'borderLeftColor': '#333333',
            'customColorText': {'__object': True},
            'barColorNegative': False,
            'customBarColorBy': 0,
            'alignmentVertical': 'middle',
            'customColorBackground': {'__object': True},
            'customColorBarBackground': {'__object': True}},
            'Votes': {'style': {'bold': False,
              'color': False,
              'italic': False,
              'fontSize': 1,
              'underline': False,
              'background': False},
            'width': 0.2,
            'append': '',
            'format': '0,0',
            'heatmap': {'enabled': False},
            'prepend': '',
            'barColor': 0,
            'barStyle': 'normal',
            'minWidth': 30,
            'sortable': True,
            'alignment': 'auto',
            'flagStyle': '1x1',
            'showAsBar': False,
            'sparkline': {'area': False,
              'type': 'line',
              'color': 0,
              'title': '',
              'format': '0.[0]a',
              'height': 20,
              'stroke': 2,
              'dotLast': True,
              'enabled': False,
              'colorNeg': 0,
              'dotFirst': True,
              'rangeMax': '',
              'rangeMin': '',
              'labelDiff': False},
            'borderLeft': 'none',
            'fixedWidth': True,
            'barRangeMax': '',
            'barRangeMin': '',
            'borderRight': 'none',
            'compactMode': False,
            'customColor': False,
            'replaceFlags': False,
            'showOnMobile': True,
            'customColorBy': 'Candidate',
            'showOnDesktop': True,
            'customBarColor': False,
            'barNoBackground': False,
            'borderLeftColor': '#333333',
            'customColorText': {'__object': True},
            'barColorNegative': False,
            'customBarColorBy': 0,
            'alignmentVertical': 'middle',
            'customColorBackground': {'__object': True},
            'customColorBarBackground': {'__object': True}},
            'Candidate': {'style': {'bold': False,
              'color': False,
              'italic': False,
              'fontSize': 1,
              'underline': False,
              'background': False},
            'width': 0.29,
            'append': '',
            'format': '0,0',
            'heatmap': {'enabled': False},
            'prepend': '',
            'barColor': 0,
            'barStyle': 'normal',
            'minWidth': 30,
            'sortable': True,
            'alignment': 'auto',
            'flagStyle': '1x1',
            'showAsBar': False,
            'sparkline': {'area': False,
              'type': 'line',
              'color': 0,
              'title': '',
              'format': '0.[0]a',
              'height': 20,
              'stroke': 2,
              'dotLast': True,
              'enabled': False,
              'colorNeg': 0,
              'dotFirst': True,
              'rangeMax': '',
              'rangeMin': '',
              'labelDiff': False},
            'borderLeft': 'none',
            'fixedWidth': True,
            'barRangeMax': '',
            'barRangeMin': '',
            'borderRight': 'none',
            'compactMode': False,
            'customColor': False,
            'replaceFlags': False,
            'showOnMobile': True,
            'customColorBy': 'Candidate',
            'showOnDesktop': True,
            'customBarColor': False,
            'barNoBackground': False,
            'borderLeftColor': '#333333',
            'customColorText': {'__object': True},
            'barColorNegative': False,
            'customBarColorBy': 0,
            'alignmentVertical': 'middle',
            'customColorBackground': {'__object': True},
            'customColorBarBackground': {'__object': True}}},
          'heatmap': {'map': {},
            'mode': 'continuous',
            'stops': 'equidistant',
            'colors': [{'color': '#f0f9e8', 'position': 0},
            {'color': '#b6e3bb', 'position': 0.16666666666666666},
            {'color': '#75c8c5', 'position': 0.3333333333333333},
            {'color': '#4ba8c9', 'position': 0.5},
            {'color': '#2989bd', 'position': 0.6666666666666666},
            {'color': '#0a6aad', 'position': 0.8333333333333334},
            {'color': '#254b8c', 'position': 1}],
            'palette': 0,
            'rangeMax': '',
            'rangeMin': '',
            'stopCount': 5,
            'hideValues': False,
            'customStops': [],
            'rangeCenter': '',
            'categoryOrder': [],
            'interpolation': 'equidistant',
            'categoryLabels': {}},
          'perPage': 20,
          'striped': False,
          'markdown': False,
          'noHeader': False,
          'showRank': False,
          'sortTable': True,
          'pagination': {'enabled': True, 'position': 'top'},
          'searchable': False,
          'showHeader': True,
          'compactMode': False,
          'sortDirection': 'asc',
          'chart-type-set': True,
          'mobileFallback': False,
          'mergeEmptyCells': False,
          'firstRowIsHeader': False,
          'firstColumnIsSticky': False},
          'axes': {},
          'publish': {'embed-width': 600,
          'embed-height': 192,
          'blocks': {'logo': {'enabled': False},
            'embed': False,
            'download-pdf': False,
            'download-svg': False,
            'get-the-data': True,
            'download-image': False},
          'export-pdf': {},
          'autoDarkMode': False,
          'chart-height': 122,
          'force-attribution': False},
          'annotate': {'notes': ''},
          'custom': {},
        }
        #Update the metadata of the chart
        dw.update_metadata(chart_id, properties)

        #Append the chart ID to the chart_ids.txt file
        with open("chart_ids.txt", "a") as idn:
               idn.write(chart_id + "\n")

        iframe = dw.get_iframe_code(chart_id)

        with open("iframes.txt", "w") as ifr:
               ifr.write(iframe + "\n")
