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

scope = "user-read-playback-state,user-modify-playback-state"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="88fe685c5ea94e7abf1b015eacd5eace",
                                               client_secret="204df711f1234999b3983024066ccf21",
                                               redirect_uri="http://localhost",
                                               scope="user-read-currently-playing")
                    )

def callSpot(last_trackID, last_albumID):
  # EXTRACT DATA FROM SPOTIFY
  trackDict = sp.current_user_playing_track()

  #Build Variables for Track
  if trackDict != None:
    try:
    	trackID = trackDict['item']['id'].replace("'", "")
    except TypeError:
    	"Whoops! Unable to locate data"
    	pass
    try:
    	trackPlayingBool = trackDict['is_playing']
    except TypeError:
    	pass
    try:
    	trackName = trackDict['item']['name'].replace("'", "")
    except TypeError:
    	pass
    try:
    	albumName = trackDict['item']['album']['name'].replace("'", "")
    except TypeError:
    	pass
    try:
    	albumID = trackDict['item']['album']['id'].replace("'", "")
    except TypeError:
    	pass
    try:
    	trackDuration = trackDict['item']['duration_ms']
    except TypeError:
    	pass
    try:
    	trackProgress = trackDict['progress_ms']
    except TypeError:
    	pass
    try:
    	trackCoverArt = trackDict['item']['album']['images'][0]['url']
    except TypeError:
    	pass

    #Build Variables for Artist
    try:
    	artistDetails = trackDict['item']['artists']
    except TypeError:
    	pass
    try:
    	artistDict = artistDetails[0]
    except TypeError:
    	pass
    try:
    	artistName = artistDict['name']
    except TypeError:
    	pass
    try:
    	artistID = artistDict['id']
    except TypeError:
    	pass

    #Download new album artwork if the album changes.
    if albumID != last_albumID:
    	print("Downloading new album art work!" + "		 " + albumID + " => " + last_albumID)
    	r = urllib.request.urlopen(trackCoverArt)
    	with open("art.jpg", "wb") as f:
    		f.write(r.read())

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

root = Tk()
root.title('Raspberry Spotipy Viewer')
root.configure(bg='black')
root.attributes('-fullscreen', True)
last_albumID = ""
last_trackID = ""

try:
  song = callSpot(last_trackID, last_albumID)

  last_trackID = song['TrackID']
  last_albumID = song['AlbumID']
except requests.exceptions.ReadTimeout:
  print("Request timed out")


kTitle = Label(root, text = song['Name'], font=('Monospace Regular', 20, 'bold'), bg='black', fg='white')
kArtist = Label(root, text = song['Artist'], font=('Monospace Regular', 18), bg='black', fg='white')

if song['Art'] != False:
	kArtwork = Image.open('art.jpg')
else:
	kArtwork = Image.open('spotico.png')
kArtwork_resized = kArtwork.resize((490, 490), Image.ANTIALIAS)
kArtwork_thumbnail = ImageTk.PhotoImage(kArtwork_resized)

kPortrait = Label(image = kArtwork_thumbnail)

kTitle.pack()
kArtist.pack()
kPortrait.pack()



def kUpdate(last_trackID, last_albumID):
  global kArtwork
  global kArtwork_resized
  global kArtwork_thumbnail
  print("updating..")
  try:
    song = callSpot(last_trackID, last_albumID)

    last_trackID = song['TrackID']
    last_albumID = song['AlbumID']
    kTitle['text'] = song['Name']
    kArtist['text'] = song['Artist']
    
    if song['Art'] != False:
    	kArtwork = Image.open('art.jpg')
    else:
    	kArtwork = Image.open('spotico.png')
    kArtwork_resized = kArtwork.resize((490, 490), Image.ANTIALIAS)
    kArtwork_thumbnail = ImageTk.PhotoImage(kArtwork_resized)

    kPortrait['image'] = kArtwork_thumbnail
    root.update_idletasks()
  except requests.exceptions.ReadTimeout:
    print("Request timed out")
  root.after(2000, lambda: kUpdate(last_trackID, last_albumID))  # reschedule event in 2 seconds

def close(event):
    exit() # if you want to exit the entire thing

root.bind('<Escape>', close)
root.after(2000, lambda: kUpdate(last_trackID, last_albumID))  # reschedule event in 2 seconds
root.mainloop()