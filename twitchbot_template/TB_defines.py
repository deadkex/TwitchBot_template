import json
from datetime import datetime


# **********************************************************************************************************************
# User defines
# **********************************************************************************************************************
debug = True


class ChannelIDs:
    main = 0


init_channels = [
    ""
]


# **********************************************************************************************************************
# Defines
# **********************************************************************************************************************
class __ClientData:
    client_id = None
    client_secret = None
    authorization_code = None
    user_access_token = None
    refresh_token = None
    app_access_token = None

    def read_config(self):
        with open("TB_secrets/TB_client.json") as file:
            data = json.load(file)
            self.client_id = data["client_id"]
            self.client_secret = data["client_secret"]
            self.authorization_code = data["authorization_code"]

        from TB_fnc.TB_twitch_api import get_auth_refresh_token
        self.user_access_token, self.refresh_token = get_auth_refresh_token(
            self.client_secret, self.client_id, self.authorization_code)

        with open("TB_secrets/TB_app_access_token.json") as file:
            data = json.load(file)
            if datetime.fromisoformat(data["app_access_token_timeout"]) < datetime.now():
                from TB_fnc.TB_twitch_api import get_app_access_token
                self.app_access_token = get_app_access_token(self.client_secret, self.client_id)
            else:
                self.app_access_token = data["access_token"]


# **********************************************************************************************************************
# Singletons
# **********************************************************************************************************************
client_data = __ClientData()
