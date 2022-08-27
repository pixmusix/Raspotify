import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
from time import sleep
import re
import urllib.request
from tkinter import *
from PIL import ImageTk, Image
import requests
import time
from datetime import date, datetime
from creds import Spotify_Credentials

#Create Spotify API
credentials = Spotify_Credentials()
scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=credentials.Client_ID,
                                               client_secret=credentials.Client_Secret,
                                               redirect_uri="http://localhost",
                                               scope="user-read-currently-playing")
                    )

def callSpot(last_trackID, last_albumID):
  # EXTRACT DATA FROM SPOTIFY
  trackDict = sp.current_user_playing_track()
  
  if trackDict != None:
    try:
      #Build Variables for Track
    	trackID = trackDict['item']['id'].replace("'", "")
    	trackPlayingBool = trackDict['is_playing']
    	trackName = trackDict['item']['name'].replace("'", "")
    	albumName = trackDict['item']['album']['name'].replace("'", "")
    	albumID = trackDict['item']['album']['id'].replace("'", "")
    	trackDuration = trackDict['item']['duration_ms']
    	trackProgress = trackDict['progress_ms']
    	trackCoverArt = trackDict['item']['album']['images'][0]['url']

      #Build Variables for Artist
    	artistDetails = trackDict['item']['artists']
    	artistDict = artistDetails[0]
    	artistName = artistDict['name']
    	artistID = artistDict['id']
    except TypeError:
      pass

    #Download new album artwork if the album changes.
    if albumID != last_albumID:
      print("Downloading new album art work!" + "    " + albumID + " => " + last_albumID)
      r = urllib.request.urlopen(trackCoverArt)
      with open("art.jpg", "wb") as f:
        f.write(r.read())

    #Construct dictionary reprosenting current song
    spod = {
          'PlayingNow' : trackPlayingBool,
          'TrackID' : trackID,
          'Name' : trackName,
          'Album' : albumName,
          'AlbumID' : albumID,
          'Artist' : artistName,
          'Art' : trackCoverArt[:-10]
          }
    if trackID != last_trackID:
      pprint(spod)
    return spod

  else:
    #When no song is playing this code puts the Date and Time on Screen
    today = date.today()
    current_date = today.strftime("%d/%m/%Y")
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    print("Spotify isn't making noise" + "		Current Time =", current_time + "		Today's date:", today) 
    spod = {
          'PlayingNow' : False,
          'TrackID' : "XXXXXXXXXXXXXXXXXXXXXX",
          'Name' : current_time,
          'Album' : "XXXXXXXXXXXXXXXXXXXXXX",
          'AlbumID' : "",
          'Artist' : current_date,
          'Art' : False
          }
    return spod

def kUpdate(last_trackID, last_albumID):
  global kArtwork
  global kArtwork_resized
  global kArtwork_thumbnail
  print("updating..")

  try:
    #Get this song as dictionary
    song = callSpot(last_trackID, last_albumID)

    #Reset SongID to this song
    last_trackID = song['TrackID']
    last_albumID = song['AlbumID']

    #Change text on screen to this song
    kTitle['text'] = song['Name']
    kArtist['text'] = song['Artist']
    
    #Select art style
    if song['Art'] != False:
      kArtwork = Image.open('art.jpg')
    else:
      kArtwork = Image.open('spotico.png')

    #Format Artwork and put it on screen
    kArtwork_resized = kArtwork.resize((490, 490), Image.ANTIALIAS)
    kArtwork_thumbnail = ImageTk.PhotoImage(kArtwork_resized)
    kPortrait['image'] = kArtwork_thumbnail

    #Update all vars in mainloop()
    root.update_idletasks()

  except requests.exceptions.ReadTimeout:
    print("Request timed out")

  #Reschedule event in 2 seconds
  root.after(2000, lambda: kUpdate(last_trackID, last_albumID))  

def close(event):
    exit()

if __name__ == "__main__":
  #Init Tkinter
  root = Tk()
  root.title('Raspberry Spotipy Viewer')
  root.configure(bg='black')
  root.attributes('-fullscreen', True)

  #Init current SongID
  last_albumID = ""
  last_trackID = ""

  #Get this song as dictionary
  try:
    song = callSpot(last_trackID, last_albumID)

    last_trackID = song['TrackID']
    last_albumID = song['AlbumID']
  except requests.exceptions.ReadTimeout:
    print("Request timed out")

  #Set Text
  kTitle = Label(root, text = song['Name'], font=('Monospace Regular', 20, 'bold'), bg='black', fg='white')
  kArtist = Label(root, text = song['Artist'], font=('Monospace Regular', 18), bg='black', fg='white')

  #Select art style
  if song['Art'] != False:
  	kArtwork = Image.open('art.jpg')
  else:
  	kArtwork = Image.open('spotico.png')

  #Format Artwork and put it on screen
  kArtwork_resized = kArtwork.resize((490, 490), Image.ANTIALIAS)
  kArtwork_thumbnail = ImageTk.PhotoImage(kArtwork_resized)
  kPortrait = Label(image = kArtwork_thumbnail)

  #Pack Elements
  kTitle.pack()
  kArtist.pack()
  kPortrait.pack()

  #Give user a way to exit
  root.bind('<Escape>', close)
  #Reschedule event in 2 seconds
  root.after(2000, lambda: kUpdate(last_trackID, last_albumID))
  #DO IT!
  root.mainloop()