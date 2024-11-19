from dotenv import load_dotenv
from requests import post, get
from http.server import HTTPServer, BaseHTTPRequestHandler
import base64
import colors
from helpful_functions import *
import json
import os
import urllib.parse

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8888/callback"


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    """
    HTTP server handler to capture the authorization code from Spotify's redirect.
    """

    def do_GET(self):
        # Parse the query parameters
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            # Extract the authorization code
            authCode = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Authorization successful! You can close this window.")
            
            # Store the authorization code for later use
            self.server.authCode = authCode
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed. No code provided.")


def getAuthorizationUrl(clientId: str, redirectUri: str, scope: str) -> str:
    """
    Generate the Spotify authorization URL for user login.
    """
    baseUrl = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": clientId,
        "response_type": "code",
        "redirect_uri": redirectUri,
        "scope": scope,
    }
    return f"{baseUrl}?{urllib.parse.urlencode(params)}"


def getUserAccessToken(clientId: str, clientSecret: str, redirectUri: str, authCode: str) -> dict:
    """
    Exchange the authorization code for an access token.
    """
    url = "https://accounts.spotify.com/api/token"
    authHeader = base64.b64encode(f"{clientId}:{clientSecret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {authHeader}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "authorization_code",
        "code": authCode,
        "redirect_uri": redirectUri,
    }
    response = post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error fetching token: {response.status_code} - {response.text}")


def getCurrentlyPlayingTrack(token: str) -> None:
    """
    Fetch the currently playing track for the authenticated user.
    """
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {"Authorization": f"Bearer {token}"}
    response = get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        if data.get("is_playing"):
            track = data["item"]["name"]
            artist = ", ".join(artist["name"] for artist in data["item"]["artists"])
            album = data["item"]["album"]["name"]
            progress = data["progress_ms"] / 1000
            duration = data["item"]["duration_ms"] / 1000
            print(f"Currently playing: {track} by {artist} from the album '{album}'")
            print(
                f"Progress: {progress:.2f}s / {duration:.2f}s  -  {progressBar(progress/duration, 20)}"
            )
        else:
            print("No track is currently playing.")
    elif response.status_code == 204:
        print("No content: Nothing is playing right now.")
    else:
        print(f"Error fetching currently playing track: {response.status_code} - {response.text}")


def main():
    """
    Main function to demonstrate the Spotify Authorization Code Flow.
    """
    # Step 1: Generate authorization URL
    scope = "user-read-currently-playing"
    print("Go to the following URL to authorize the app:")
    authUrl = getAuthorizationUrl(CLIENT_ID, REDIRECT_URI, scope)
    print(f"{colors.blue}{authUrl}{colors.clear}")

    # Step 2: Start HTTP server to handle the redirect
    server = HTTPServer(("localhost", 8888), SpotifyAuthHandler)
    server.handle_request()  # Handle a single request

    # Step 3: Get authorization code from server
    authCode = getattr(server, "authCode", None)
    if not authCode:
        print("Failed to get authorization code.")
        return

    # Step 4: Exchange authorization code for access token
    try:
        tokens = getUserAccessToken(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, authCode)
        accessToken = tokens["access_token"]

        # Step 5: Fetch and display the currently playing track
        while not keyboard.KEY_DOWN('space'):
            getCurrentlyPlayingTrack(accessToken)
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
