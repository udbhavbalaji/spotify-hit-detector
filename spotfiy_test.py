import requests

# SpotifyClient is the class that interacts with the Spotify API endpoint to retrieve the 
# data we need to make the necessary predictions
class SpotifyClient(object):
    def __init__(self, api_key, song_id, features):
        '''Initializing the class variables for the instance
        '''
        self.api_key = api_key
        self.song_id = song_id
        self.features = features

    def get_track_features(self):
        '''Method that will retrieve the audio features of the track and retuen it in a list.
        '''

        # Formatting the URL of the API endpoint we want to interact with
        url = f'https://api.spotify.com/v1/audio-features/{self.song_id}'

        # Making a request to the URL and recieving the response
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.api_key}'
            }
        )

        # Converting the response into a python dict
        response_json = response.json()

        value_list = []

        # Adding each of the features to the list
        for feature in self.features:
            try:
                value_list.append(response_json[feature])
            except:
                # Handling error where the access token is expired
                if 'error' in response_json.keys():
                    return None
                value_list.append(None)
        
        return value_list

    def get_track_analysis(self):
        '''Method that will retrieve the audio analysis and extract the necessary data
        '''
        
        # Formatting the URL of the API endpoint we want to interact with
        url = f'https://api.spotify.com/v1/audio-analysis/{self.song_id}'

        # Making a request to the URL and recieving the response
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.api_key}'
            }
        )

        # Converting the response into a python dict
        response_json = response.json()

        try:
            sections = response_json['sections']
            section = sections[2]
            chorus_hit = section['start']
        except:
            # Handling error where the access token is expired
            if 'error' in response_json.keys():
                return None
            sections = []
            chorus_hit = None
        
        return [chorus_hit, len(sections)]

    
    def get_track_artists(self):
        '''Method that will retrieve the artist of the track
        '''

        # Formatting the URL of the API endpoint that we want to interact with
        url = f'https://api.spotify.com/v1/tracks/{self.song_id}'

        # Making a request to the endpoint and recieving a response
        response = requests.get(
            url,
            headers={
                "Content-Type": "application/json",
                "Authorization": f'Bearer {self.api_key}'
            }
        )

        # Converting the response to a python dict
        response_json = response.json()

        try:
            artists = response_json['artists']
            artist = artists[0]
            artist_name = artist['name']
        except:
            # Handling error where the access token has expired
            if 'error' in response_json.keys():
                return None
            artist_name = None

        return [artist_name]


