import requests
from bs4 import BeautifulSoup
import csv
from dateutil import parser
from datetime import datetime, timedelta
import os
from slack import WebClient
from slack.errors import SlackApiError

url = "https://opendata.maryland.gov/resource/nktk-ei6p.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    # Do something with the data
else:
    print("Failed to retrieve data from API")

#How to Loop Over
if response.status_code == 200:
    data = response.json()
    yesterday = datetime.now() - timedelta(days=3)
    filtered_data = []
    for row in data:
        dt_stamp = parser.parse(row['dt_stamp'])
        if dt_stamp > yesterday:
            filtered_data.append(row)
    slack_message = ""
    if len(filtered_data) > 1:
        with open('data.csv', 'w', newline='') as csvfile:
            fieldnames = filtered_data[1].keys()
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in filtered_data:
                writer.writerow(row)
        print("Data successfully written to data.csv")
        slack_message = "Auto-scraping completed successfully! Data has been written to data.csv."
    else:
        print("No data found that meets the filter criteria")
        slack_message = "Auto-scraping completed. No data found that meets the filter criteria."
else:
    print("Failed to retrieve data from API")
    slack_message = "Auto-scraping failed. Unable to retrieve data from API."

slack_token = os.environ.get('slack_api_token')
client = WebClient(token=slack_token)

try:
    try:
    response = client.chat_postMessage(
        channel="#slack-bots",
        text="Hi :wave:, Here's the latest poweroutages data:link: <https://bit.ly/shortened_link|data.csv>")
    print("Message sent: ", response["ts"])
except SlackApiError as e:
    print("Error sending message: ", e)


