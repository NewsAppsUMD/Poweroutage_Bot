import os
from slack import WebClient
from slack.errors import SlackApiError

slack_token = os.environ.get('slack_api_token')
client = WebClient(token=slack_token)

msg = "Fingers crossed for an eventual success, yeah?"
try:
    response = client.chat_postMessage(
        channel="#slack-bots",
        text="Auto-scraping completed successfully!"
    )
    print("Message sent: ", response["ts"])
except SlackApiError as e:
    print("Error sending message: ", e)