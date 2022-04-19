from flask import Flask, request, render_template, jsonify
import numpy as np
import pickle
from spotfiy_test import SpotifyClient
import pandas as pd


# Creating the Flask app and loading the model from the pickle file
app = Flask(__name__)
model = pickle.load(open('model.pkl', 'rb'))

# Routing the app to this method when the url ends with /
@app.route('/', methods=['GET','POST'])
def index():
    # Displaying index.html as the landing page for the app
    return render_template('index.html')

# Routing the app to this method when the url ends with /predict/
@app.route('/predict/', methods=['GET'])
def predict():
    # For npw, the api_key has to be manually retrieved from the spotify developers website but in the future, 
    # it will be automated by a script that does it every hour
    api_key = 'BQBv07_-6MFFDmHpU6U5-2PfJlULGFndOtI7TFXoLWlTYjk-jvknDE74w5ErGDFcmdAb-rs1Wfgbd57_IUqi0HUAYY8dkklD72GI5b8YTg9rHjQFWy-lKshn9RgUhRrMpB6C8R8YyL7g9mTPInoc4gSqOaJGuOJ4K01MLmk'
    
    # Retrieving the song_url from the webpage
    song_url = request.args.get('song_url')
    # Processing the URL to obtain the song_id
    song_url = song_url.strip()
    song_id = song_url.split('/')[4]
    song_id = song_id.split('?')[0]

    # Defining the features that we are getting from the get_track_features() method
    features = ['danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature']

    # Initializing an object instance of the SpotifyClient with the api_key, song_id and features
    spotify_client = SpotifyClient(api_key, song_id, features)

    # Getting the track features of the required song
    track_features = spotify_client.get_track_features()

    # Defining a list with all attributes to order the inputs correctly 
    key_features = ['artist','danceability', 'energy', 'key', 'loudness', 'mode', 'speechiness', 'acousticness',
    'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms', 'time_signature', 'chorus_hit','sections']

    test_in = {}

    artist = spotify_client.get_track_artists()

    section_values = spotify_client.get_track_analysis()

    if (track_features is None) or (artist is None) or (section_values is None):
        return render_template('after.html', prediction_text='The access token has expired! Please generate a new access token and try again!')

    # Creating a list with all the inputs in the right order
    test = artist + track_features + section_values

    # Creating a dictionary to create the input
    for i, feature in enumerate(key_features):
        test_in[feature] = test[i]

    # Creating the input dataframe 
    test_df = pd.DataFrame(test_in, index=[0])

    # Predicting the target for the given song
    pred = model.predict(test_df)

    # Generating the output based on the predicted target
    if pred == 1:
        output = 'Congrats! Your song is/has the potential to be a hit!'
    else:
        output = 'Unfortunately, your song has a very low chance of succeeding. Better luck next time!'

    # Returning the webpage with the output
    return render_template('after.html', prediction_text=output)


if __name__ == "__main__":
    app.run(debug=True)