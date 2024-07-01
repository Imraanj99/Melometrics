
# Melometrics spotify app (www.melometrics.co.uk)

This project allows spotify users to view analytics of their favourite songs on spotify and can generate playlists based on these tracks. 

## Features

- Top Tracks: this allows users to view their top tracks over 3 different time scales
- Top artists: this allows users to view their top artists over 3 different time scales
- Song analysis: this allows users to view the audio features of their top tracks and liked songs (measured features include: Danceability, Energy, speechiness, acousticness, instrumentalness, Positivity, length and BPM)
- Playlist generation: This allows users to generate custom playlists based on their top songs

## Set Up

### Downloading the code

First, you need to clone this repository:

```bash
git clone git@github.com/imraanj99/Melometrics
```


### Spotify API

- For this app to work you will need to register the app via the spotify developer dashboard.
- Please follow this link: 
- Log in with your spotify account and follow the steps to create a new app

### Adding Client ID, Client Secret and app secret key

- Create a python file within the "website folder" (I have named mine secret_info.py)
- Once you have created the app, go into your app and click on settings and copy the ClientID and ClientSecret
- If you wish to create a playlist, please include the encoded_logo lins, or remove the parameter from  
- Your secret key can be any string of your choice
- the file should have the below format

```bash
secret_key = (enter a string of you choice here)
ClientID = "(paste in your ClientID from the dashboard)"
ClientSecret = "(paste in your ClientSecret from the dashboard)"
encoded_logo = '(enter the Base64 jepg format of the image)'
```

## Extended quota mode
- this app uses Oauth, and the spotify api. To make full use of this for your own purposes you will need to submit an extended quote request in the spotify developer site
- You app will initial be in developer mode and will only allow account which you have manually permitted on the spotify developer dashboard
- Submitting an extended quota request will give you the ability to let any spotify account use the app provided the form is accepted

## Running the code

- to run the code, simply run the app.py
- The applications will always running on http://localhost:5000 unless specified otherwise
