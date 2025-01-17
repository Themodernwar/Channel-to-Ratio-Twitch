#Create the following Python File (Python3, python3(lowercase lol idek))

import os
import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Twitch API Configuration
CLIENT_ID = os.getenv('TWITCH_CLIENT_ID')
CLIENT_SECRET = os.getenv('TWITCH_CLIENT_SECRET')
BASE_URL = 'https://api.twitch.tv/helix'
print("CLIENT_ID:", CLIENT_ID)
print("CLIENT_SECRET:", CLIENT_SECRET)

def get_twitch_token():
    """
    Authenticate with Twitch API using the Client Credentials Grant Flow.
    Returns an app access token.
    """
    url = 'https://id.twitch.tv/oauth2/token'
    params = {
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
        'grant_type': 'client_credentials'
    
        }
    print("Authenticating with Twitch...")
    print("Debug - Sending request with parameters:")
    print(params)  # Print the request parameters for debugging
    try:
        response = requests.post(url, params=params)
        print("Response status:", response.status_code)
        print("Response body:", response.text)
        response.raise_for_status()
        token = response.json()['access_token']
        print(f"Access token: {token}")
        return token
    except requests.exceptions.RequestException as e:
        print(f"Error during authentication: {e}")
        return None

def get_game_data(game_name, token):
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    url = f'{BASE_URL}/games'
    params = {'name': game_name}
    print(f"Fetching game data for {game_name}...")
    try:
        response = requests.get(url, headers=headers, params=params)
        print("Response status:", response.status_code)
        print("Response body:", response.text)
        response.raise_for_status()
        game_data = response.json()['data'][0]
        print(f"Game data retrieved: {game_data}")
        return game_data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game data: {e}")
        return None

def get_viewer_channel_data(game_id, token):
    """
    Retrieve total viewers and channels for a specified game ID.
    """
    headers = {
        'Client-ID': CLIENT_ID,
        'Authorization': f'Bearer {token}'
    }
    url = f'{BASE_URL}/streams'
    params = {
        'game_id': game_id,
        'first': 100
    
        }
    print(f"Fetching viewer and channel data for game_id {game_id}...")
    try:
        response = requests.get(url, headers=headers, params=params)
        print("Response status:", response.status_code)
        print("Response body:", response.text)
        response.raise_for_status()
        streams = response.json()['data']

        total_viewers = sum([stream['viewer_count'] for stream in streams])
        total_channels = len(streams)
        print(f"Viewers: {total_viewers}, Channels: {total_channels}")
        return total_viewers, total_channels
    except requests.exceptions.RequestException as e:
        print(f"Error fetching viewer/channel data: {e}")
        return 0, 0

def plot_ratio(data):
    """
    Plot the viewer-to-channel ratio over time.
    """
    data['Ratio'] = data['Viewers'] / data['Channels']
    plt.figure(figsize=(10, 6))
    plt.bar(data['Hour'], data['Ratio'], color='purple')
    plt.xlabel('Hour')
    plt.ylabel('Viewer-to-Channel Ratio')
    plt.title('Hourly Viewer-to-Channel Ratio')
    plt.show()
def get_real_time_stats(game_names, token):
    """
    Fetch real-time viewers, channels, and ratios for a list of games.
    
    Parameters:
        game_names (list): List of game names to analyze.
        token (str): Twitch API access token.
    
    Returns:
        pd.DataFrame: DataFrame with game stats (Viewers, Channels, Ratio).
    """
    game_stats = []

    for game_name in game_names:
        print(f"Fetching data for {game_name}...")
        
        # Fetch game details
        game_data = get_game_data(game_name, token)
        if game_data:
            game_id = game_data['id']

            # Fetch viewer and channel data
            viewers, channels = get_viewer_channel_data(game_id, token)
            if channels > 0:  # Avoid division by zero
                ratio = viewers / channels
            else:
                ratio = 0  # Handle case where there are no channels

            game_stats.append({
                'Game': game_name,
                'Viewers': viewers,
                'Channels': channels,
                'Ratio': ratio,
                'Timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            })
        else:
            print(f"Game data not found for {game_name}. Skipping...")

    # Convert to DataFrame
    df = pd.DataFrame(game_stats)
    return df

if __name__ == "__main__":
    print("Starting main workflow...")
    
    # Check environment variables
    if not CLIENT_ID or not CLIENT_SECRET:
        print("Error: Environment variables TWITCH_CLIENT_ID or TWITCH_CLIENT_SECRET are not set.")
        exit(1)

    # Authenticate with Twitch API
    token = get_twitch_token()
    if not token:
        print("Failed to authenticate with Twitch API.")
        exit(1)

    # Specify games to analyze
    games = ['War Thunder','Surviving Mars','Spintires','Prison Architect','PC Building Simulator','METAL GEAR SOLID V: THE PHANTOM PAIN','Hitman: Blood Money','Game Dev Tycoon','Delta Force','Arma 3' ,'HELLDIVERS 2', 'Valorant', 'League of Legends']
    
    # Fetch real-time stats
    real_time_data = get_real_time_stats(games, token)
    print(real_time_data)

    # Save data to CSV with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    file_path = f'real_time_game_stats_{timestamp}.csv'
    real_time_data.to_csv(file_path, index=False)
    print(f"Data saved to {file_path}")

#RUN THE FOLLOWING COMMANDS IN YOUR LINUX TERMINAL (dont put in the hashtags No#'s NO HASHTAGS)
#export TWITCH_CLIENT_ID='YOUR_TWITCH_CLIENT_ID'   # <----- Fill this in with your own TWITCH client ID from the Twitch Developer Console Page on your own account. (Make an application and just name the organization pretty much anything...)
#export TWITCH_CLIENT_SECRET='YOUR_TWITCH_CLIENT_SECRET'       # <----- Fill this in
#python3 python3 channel_2_VIEW-RATIO.py

















