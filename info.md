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
      entities:
        - media_player.foobar
	```
    The above configuration will create a sensor entity `sensor.foobar_lyrics`.

4. Create markdown card in lovelace:

    ```yaml
    card:
      type: markdown
      content: >-
        ## {{ states.sensor.foobar_lyrics.attributes.media_artist }} - {{ states.sensor.foobar_lyrics.attributes.media_title }}
    
        {{ states.sensor.foobar_lyrics.attributes.media_lyrics }}
    conditions:
      - entity: sensor.foobar_lyrics
        state: 'on'
    type: conditional
    ```

    The above conditional lovelace card will hide when media_player is off.


### Example service call
##### JSON
```json
{
 "media_artist":"Protoje",
 "media_title":"Mind of a King",
 "entity_id":"sensor.foobar_lyrics"
}
```

##### YAML
```yaml
media_artist: "Protoje"
media_title: "Mind of a King"
entity_id: sensor.foobar_lyrics
```
