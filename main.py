import time
from dotenv import load_dotenv, set_key
from requests import post, get
from http.server import HTTPServer, BaseHTTPRequestHandler
import webbrowser
import base64
import os
import colors as cls
import urllib.parse

# Load environment variables
load_dotenv()

CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
REDIRECT_URI = "http://localhost:8888/callback"


def progressBar(percentage: float | int, length: int, empty: str = "-", filled: str = "#", braces: str = "[]"):
    if braces == " " or braces == "":
        braces = "  "
    filled_length = int(length * percentage)
    return braces[0] + (filled * filled_length) + (empty * (length - filled_length - 1)) + braces[1]


class SpotifyAuthHandler(BaseHTTPRequestHandler):
    """
    HTTP server handler to capture the authorization code from Spotify's redirect.
    """

    def do_GET(self):
        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        if "code" in params:
            authCode = params["code"][0]
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"<script>window.close();</script>Authorization successful! You can close this window.")
            self.server.authCode = authCode
        else:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Authorization failed. No code provided.")


def getAuthorizationUrl(clientId: str, redirectUri: str, scope: str) -> str:
    baseUrl = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": clientId,
        "response_type": "code",
        "redirect_uri": redirectUri,
        "scope": scope,
    }
    return f"{baseUrl}?{urllib.parse.urlencode(params)}"


def getUserAccessToken(clientId: str, clientSecret: str, redirectUri: str, authCode: str) -> dict:
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


def refreshAccessToken(clientId: str, clientSecret: str, refreshToken: str) -> dict:
    url = "https://accounts.spotify.com/api/token"
    authHeader = base64.b64encode(f"{clientId}:{clientSecret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {authHeader}",
        "Content-Type": "application/x-www-form-urlencoded",
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": refreshToken,
    }
    response = post(url, headers=headers, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error refreshing token: {response.status_code} - {response.text}")


def saveTokenToEnv(accessToken: str, refreshToken: str):
    set_key(".env", "SPOTIFY_ACCESS_TOKEN", accessToken)
    set_key(".env", "SPOTIFY_REFRESH_TOKEN", refreshToken)


def loadTokensFromEnv():
    accessToken = os.getenv("SPOTIFY_ACCESS_TOKEN")
    refreshToken = os.getenv("SPOTIFY_REFRESH_TOKEN")
    return accessToken, refreshToken


def requestAccessToken(scope: str):
    print("Go to the following URL to authorize the app:")
    authUrl = getAuthorizationUrl(CLIENT_ID, REDIRECT_URI, scope)
    webbrowser.open(authUrl)

    server = HTTPServer(("localhost", 8888), SpotifyAuthHandler)
    server.handle_request()

    authCode = getattr(server, "authCode", None)
    if not authCode:
        raise Exception("Failed to get authorization code.")

    tokens = getUserAccessToken(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, authCode)
    saveTokenToEnv(tokens["access_token"], tokens["refresh_token"])
    return tokens


def ensureAccessToken():
    accessToken, refreshToken = loadTokensFromEnv()
    if not accessToken or not refreshToken:
        print("No tokens found, requesting new access token...")
        tokens = requestAccessToken("user-read-currently-playing")
        accessToken = tokens["access_token"]
        refreshToken = tokens["refresh_token"]

    try:
        response = get("https://api.spotify.com/v1/me", headers={"Authorization": f"Bearer {accessToken}"})
        if response.status_code != 200:
            raise Exception("Access token is invalid or expired.")
    except:
        print("Access token expired, refreshing...")
        tokens = refreshAccessToken(CLIENT_ID, CLIENT_SECRET, refreshToken)
        accessToken = tokens["access_token"]
        if "refresh_token" in tokens:
            refreshToken = tokens["refresh_token"]
        saveTokenToEnv(accessToken, refreshToken)

    return accessToken


def fetchCurrentTrack(accessToken):
    response = get(
        "https://api.spotify.com/v1/me/player/currently-playing",
        headers={"Authorization": f"Bearer {accessToken}"}
    )
    if response.status_code == 200 and response.json():
        return response.json()
    return None


def displayCurrentTrack(trackData, elapsed):
    os.system("cls" if os.name == "nt" else "clear")
    if trackData:
        track = trackData.get("item", {})
        progressMs = trackData.get("progress_ms", 0)
        durationMs = track.get("duration_ms", 1)
        releaseDate = track.get("album", {}).get("release_date", "Unknown")
        updatedProgressMs = progressMs + elapsed * 1000
        if updatedProgressMs > durationMs:
            updatedProgressMs = durationMs

        # Calculate progress
        percentage = updatedProgressMs / durationMs
        progress = progressBar(percentage, 30)

        # Fetch additional track details
        name = track.get("name", "Unknown")
        album = track.get("album", {}).get("name", "Unknown")
        artists = ', '.join(artist['name'] for artist in track.get("artists", []))
        explicit = "Yes" if track.get("explicit", False) else "No"
        popularity = track.get("popularity", "Unknown")
        is_local = "Yes" if track.get("is_local", False) else "No"
        track_number = track.get("track_number", "Unknown")
        disc_number = track.get("disc_number", "Unknown")
        external_url = track.get("external_urls", {}).get("spotify", "N/A")
        preview_url = track.get("preview_url", "N/A")

        # Display statistics
        print(f"Track: {name}")
        print(f"Artists: {artists}")
        print(f"Album: {album}")
        print(f"Release Date: {releaseDate}")
        print(f"Duration: {int(durationMs // 60000)}:{int((durationMs % 60000) // 1000):02}")
        print(f"Spotify URL: {cls.blue}{cls.UNDERLINE}{external_url}{cls.clear}")
        print(f"Explicit: {explicit}")
        print(f"Popularity: {progressBar(popularity/100, 30)} ({popularity}/100)")
        print(f"\nProgress:   {progress} ({int(updatedProgressMs // 60000)}:{int((updatedProgressMs % 60000) // 1000):02})")
        #print(f"Elapsed:    {progressBar(elapsed / 15, 30, empty='#', filled='-')}")


    else:
        print("No track is currently playing.")




def runPeriodicUpdates(interval=15):
    lastFetch = time.time() - interval
    trackData = None

    while True:
        elapsed = int(time.time() - lastFetch)
        if elapsed >= interval:
            accessToken = ensureAccessToken()
            trackData = fetchCurrentTrack(accessToken)
            lastFetch = time.time()

        displayCurrentTrack(trackData, elapsed)
        time.sleep(1)


if __name__ == "__main__":
    runPeriodicUpdates(15)
