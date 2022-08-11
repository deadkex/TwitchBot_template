import json
import os
from datetime import datetime, timedelta

import requests


def write_file(name, data):
    with open(os.path.join(os.path.dirname(__file__), os.pardir, f"TB_secrets/{name}.json"), "w") as file:
        file.write(data)


def read_file(name):
    with open(os.path.join(os.path.dirname(__file__), os.pardir, f"TB_secrets/{name}.json")) as file:
        return json.load(file)


def get_app_access_token(client_secret, client_id):
    # https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#client-credentials-grant-flow
    data = {
        "client_secret": client_secret,
        "client_id": client_id,
        "grant_type": "client_credentials"
    }
    r_json = requests.post("https://id.twitch.tv/oauth2/token", params=data).json()
    r_json["app_access_token_timeout"] = (datetime.now() + timedelta(seconds=r_json["expires_in"])).isoformat()
    r = json.dumps(r_json, indent=4)
    write_file("TB_app_access_token", r)
    return r_json["access_token"]


def get_auth_refresh_token(client_secret, client_id, authorization_code, refresh=True):
    if refresh:
        # https://dev.twitch.tv/docs/authentication/refresh-tokens
        token_data = read_file("TB_auth_code")
        data = {
            "client_secret": client_secret,
            "client_id": client_id,
            "grant_type": "refresh_token",
            "refresh_token": token_data["refresh_token"]
        }
    else:
        # https://dev.twitch.tv/docs/authentication/getting-tokens-oauth#authorization-code-grant-flow
        data = {
            "client_secret": client_secret,
            "client_id": client_id,
            "grant_type": "authorization_code",
            "redirect_uri": "http://localhost",
            "code": authorization_code
        }
    r_json = requests.post("https://id.twitch.tv/oauth2/token", params=data).json()
    r = json.dumps(r_json, indent=4)
    write_file("TB_auth_code", r)
    return r_json["access_token"], r_json["refresh_token"]


def get_id_with_name(name, app_access_token, client_id):
    # https://dev.twitch.tv/docs/api/reference#get-users
    url = f"https://api.twitch.tv/helix/users?login={name}"
    headers = {
        "Authorization": f"Bearer {app_access_token}",
        "Client-ID": client_id
    }
    r = requests.get(url, headers=headers).json()["data"]
    return r[0]["id"] if r else None
