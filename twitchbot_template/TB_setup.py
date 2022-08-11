import json
import os
import sys

from TB_fnc.TB_twitch_api import get_app_access_token, get_auth_refresh_token, get_id_with_name

try:
    import twitchio
    import requests
except ImportError:
    print("Missing packages from requirements.txt - please install all of them!")
    sys.exit(1)


if not os.path.exists("TB_secrets"):
    os.makedirs("TB_secrets")

print(
    "Open this link and create an app:\n"
    "https://dev.twitch.tv/console/apps\n"
    "Use http://localhost as 'OAuth Redirect URL'\n"
    "Select the category 'Chat Bot'")
client_id = input("Enter your client id: ")
client_secret = input("Enter your client secret: ")

app_access_token = get_app_access_token(client_secret=client_secret, client_id=client_id)

channel_id = None
while not channel_id:
    channel_name = input("Enter your channels name: ")
    channel_id = get_id_with_name(name=channel_name, app_access_token=app_access_token, client_id=client_id)
    if not channel_id:
        print("Channel not found!")
print(
    f"Please put '{channel_id}' into TB_defines.py in ChannelIDs.main\n"
    f"Please put the channel's name into TB_defines.py in init_channels plus all channels you want to read chat from\n"
    f"To get channel id's, you can use get_id_with_name() from TB_twitch_api.py")

input("Enter to continue")
print(20 * "-")

url = "https://id.twitch.tv/oauth2/authorize?response_type=code" \
      f"&client_id={client_id}" \
      "&redirect_uri=http://localhost" \
      "&scope=" \
      "chat:read " \
      "chat:edit " \
      "moderator:manage:chat_messages " \
      "moderator:manage:banned_users " \
      "moderator:manage:announcements " \
      "moderation:read " \
      "channel:read:redemptions " \
      "channel:manage:redemptions " \
      "channel:moderate " \
      "channel:read:vips " \
      "channel:manage:vips " \
      "channel:manage:moderators " \
      "channel:read:subscriptions".replace(" ", "%20")
print("To get the access_token you have to:\n"
      "- specify scopes\n"
      "- create/open the url\n"
      "- copy the code from the url\n"
      "You can find all scopes under this link:\n"
      "https://dev.twitch.tv/docs/authentication/scopes\n"
      "An example link (with a lot of scopes) to work with in this step:\n"
      f"{url}")

user_access_token = None
while not user_access_token:
    authorization_code = input("Enter the code from the url: ")
    try:
        user_access_token, _ = get_auth_refresh_token(
            client_secret=client_secret, client_id=client_id, authorization_code=authorization_code, refresh=False)
    except KeyError as exc:
        print(f"Error: Invalid code")

with open("TB_secrets/TB_client.json", "w") as file:
    file.write(
        json.dumps(
            {
                "client_id": client_id,
                "client_secret": client_secret,
                "authorization_code": authorization_code
            },
            indent=4
        )
    )

input("Have fun! (Enter to exit)")
