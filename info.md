## Setup

1. Create a Genius.com access token:
	1. Sign up for a free account at genius.com if you don't have one
	2. Open the [New API Client](https://genius.com/api-clients/new) page and fill in App Name, App Website URL, and Redirect URL (this won't be used).
	3. Once you've saved the new client, click the button to generate a `Client Access Token` (record this somewhere safe).
2. Install markdown card mod [lovelace-markdown-mod](https://github.com/thomasloven/lovelace-markdown-mod)
3. Install this integration
4. Enable Genius Lyrics in `configuration.yaml` by adding the following (*substitute your access token from step 1*):

	```yaml
	genius_lyrics:
	  access_token: "3SxSxqZJOtz5fYlkFXv-12E-mgripD0XM7v0L091P3Kz22wT9ReCRNg0qmrYeveG"
	```

5. Create a template sensor named `lyrics`:

	```yaml
	sensors:
	  - platform: template
	    sensors:
	      lyrics:
	        friendly_name: "Lyrics"
	        value_template: ""
	```

6. Create a Markdown card in Lovelace that accesses the attributes of the new `lyrics` sensor:

	```yaml
	  - type: markdown
	    content: >
	      ## [[ sensor.lyrics.attributes.artist ]] - [[ sensor.lyrics.attributes.title ]]
	      
	      [[ sensor.lyrics.attributes.lyrics ]]
	```

7. Create an automation to call service `genius_lyrics.search_lyrics` upon media_player state change, and provide `artist_name` and `song_title`, along with the lyrics sensor `entity_id`.

---

### Example service call JSON

```json
{
 "artist_name":"Protoje",
 "song_title":"Mind of a King",
 "entity_id":"sensor.lyrics"
}
```

### Example automation YAML

```yaml
automation:
  - alias: "Update Genius Lyrics when Spotify song changes."
    trigger:
      platform: template
      value_template: "{{ states.media_player.spotify.attributes.media_title != states.sensor.genius_lyrics.attributes.title }}"
    action:
      - service: genius_lyrics.searchlyrics
        data:
          entity_id: sensor.lyrics
        data_template:
          artist_name: "{{ states.media_player.spotify.attributes.media_artist }}"
          song_title: "{{ states.media_player.spotify.attributes.media_title }}"
```
