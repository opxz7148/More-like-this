# More like this

## Description: 

More like this is an application for learn more about your favourite artist. By utillizing Spotify Web API via spotipy library, This application able to show information about every artist that available on Spotify along with their related artist and data analytics about their discography popularity.

## Application screenshot

### Before select artist to display (Incomplete yet)
![Link Name](screenshot/artist_not_select.png) 

### After select artist to display (Incomplete yet)
![Link Name](screenshot/artist_selected.png) 

## How to install

### Install requirement package
```pip install -r requirements.txt```

### Get API keys
Obtain Spotify API client ID and client secret from [This link](https://developer.spotify.com/dashboard) 
by follow instruction 1-3 in [This link](https://stevesie.com/docs/pages/spotify-client-id-secret-developer-api) 

### Set API keys

Create a file call .env by run `echo .env`

Paste this message into [.env](.env) file
```
SPOTIPY_CLIENT_ID="*Your client id*"
SPOTIPY_CLIENT_SECRET="*Youe client secret key*"
```

## How to run program
Run `python main.py`