# Raspotify

Python_Tkinter program to display current Spotify Song, Artist and Album Art

### Getting Started

- Follow the [Spotify Developer Web API quick start](https://developer.spotify.com/documentation/web-api/quick-start/)
- Setup a Spotify Client with the [user-read-currently playing scope](https://developer.spotify.com/documentation/general/guides/authorization/scopes/#user-read-currently-playing)
- Place your clientID and client-secret in a .py file to be imported into your script.

```python
from dataclasses import dataclass

@dataclass
class Spotify_Credentials:

	Client_ID: str = "foo"
	Client_Secret: str = "bar"
```

### Run

```bash
python3 Raspoti.py
```


### Running on a Raspberry PI on startup.

I found I needed the [Desktop Version of Raspberry PI OS](https://www.raspberrypi.com/documentation/computers/os.html)
I had the most success placing the following code in my .bashrc file at the bottom.

```bash
sleep 5
cd /absolute/path/to/script
python3 Raspoti.py
```

Then I ensured terminal booted on launch

```bash
cd home/pi/.config/lxsession/LXDE-pi/
echo "@lxterminal" >> autostart
reboot
```

Having terminal open appeared to be "necessary" to make the hotkeys trigger.
I also found that this method ensured that wifi and other auxiliaries would be operation before the loop would run.

### Next steps

I would love some recommendations on how to use curl in place of the browser to handle user login.
If you have thoughts please get in touch.

###### MIT License
