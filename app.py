import uuid

import flask
import requests
from flask import Flask
from flask_oauthlib.client import OAuth
import  config
from rclone_client import Rclone

APP = Flask(__name__)

APP.debug = True
APP.secret_key = 'development'
OAUTH = OAuth(APP)
MSGRAPH = OAUTH.remote_app(
    'microsoft', consumer_key=config.CLIENT_ID, consumer_secret=config.CLIENT_SECRET,
    request_token_params={'scope': config.SCOPES},
    base_url=config.RESOURCE + config.API_VERSION + '/',
    request_token_url=None, access_token_method='POST',
    access_token_url=config.AUTHORITY_URL + config.TOKEN_ENDPOINT,
    authorize_url=config.AUTHORITY_URL + config.AUTH_ENDPOINT)



@APP.route('/')
def hello_world():
    return 'Hello World!'


@APP.route('/onedrive/login')
def onedrive_login():
    flask.session['state'] = str(uuid.uuid4())
    result = MSGRAPH.authorize(callback=config.REDIRECT_URI, state=flask.session['state'])

    return result

@APP.route('/onedrive/auth_callback')
def onedrive_auth_callback():
    response = MSGRAPH.authorized_response()
    flask.session['access_token'] = response['access_token']
    data = get_drive_id(response['access_token'])
    token = {
        "access_token": response['access_token']
    }
    name = 'my-conf'
    drive_id = data["drive_id"]
    drive_type = data["drive_type"]
    cloud_type = "onedrive"

    rclone = Rclone()
    config_path = rclone.create_config(name, cloud_type, token, drive_type, drive_id)
    rclone.copy(config_path, "test_client", "backup")

    return 'Hello World!'


def get_drive_id(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    url = "https://graph.microsoft.com/v1.0/me/drive"
    response = requests.get(url, headers=headers)

    response = response.json()

    result = {
        'drive_id': response['id'],
        'drive_type': response['driveType']
    }
    return result



if __name__ == '__main__':
    APP.run()
