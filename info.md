## Setup

1. Create a Genius.com access token:
	1. Sign up for a free account at [genius.com](https://genius.com) if you don't have one.
	2. Open the [New API Client](https://genius.com/api-clients/new) page and fill in App Name, App Website URL,
	   and Redirect URL (this won't be used).
	3. Once you've saved the new client, click the button to generate a `Client Access Token` (record this somewhere safe).
2. Install this integration
3. Enable Genius Lyrics in `configuration.yaml` by adding the following (*substitute your access token from step 1*):

	```yaml
	genius_lyrics:
	  access_token: "3SxSxqZJOtz5fYlkFXv-12E-mgripD0XM7v0L091P3Kz22wT9ReCRNg0qmrYeveG"
	```

4. Create a template sensor named `lyrics`:

	```yaml
	sensors:
	  - platform: template
	    sensors:
	      lyrics:
	        friendly_name: "Lyrics"
	        value_template: ""
	```

5. Create markdown card in lovelace:

    ```yaml
      - type: markdown
        content: >
          ## {{ states.sensor.lyrics.attributes.artist }} - {{ states.sensor.lyrics.attributes.title }}

          {{ states.sensor.lyrics.attributes.lyrics }}
    ```

6. Create an automation to call service `genius_lyrics.search_lyrics` upon media_player state change, providing "Artist", "Title".


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
      - service: genius_lyrics.search_lyrics
        data:
          entity_id: sensor.lyrics
        data_template:
          artist_name: "{{ states.media_player.spotify.attributes.media_artist }}"
          song_title: "{{ states.media_player.spotify.attributes.media_title }}"
```
