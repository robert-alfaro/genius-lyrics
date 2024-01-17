## Setup

1. Install this integration via HACS or manually and reboot Home Assistant.
2. Configure `Genius Lyrics` via integrations page  or press the blue button below. 

    [![Open your Home Assistant instance and start setting up a new integration.](https://my.home-assistant.io/badges/config_flow_start.svg)](https://my.home-assistant.io/redirect/config_flow_start/?domain=genius_lyrics)

3. Create markdown card in lovelace. All created sensors are named after the media player and appended with `_lyrics`.

    >*Below, media player `foobar` is just an example. Replace it with your media player's entity name.*
   
   ```yaml
   type: vertical-stack
   cards:
     - type: media-control
       entity: media_player.foobar
     - type: conditional
       conditions:
         - entity: sensor.foobar_lyrics
           state: "on"
       card:
         type: markdown
         content: >-
           ![image]({{
           states.sensor.foobar_lyrics.attributes.media_image }})
   
           ## {{ states.sensor.foobar_lyrics.attributes.media_artist }} - {{ states.sensor.foobar_lyrics.attributes.media_title }}
   
           {{ states.sensor.foobar_lyrics.attributes.media_lyrics }}
   ```

   The above lovelace card groups the media player and lyrics sensor together.
   The conditional portion will hide the lyrics sensor when the media player is off.


### Example service call

Service optionally accepts `entity_id`. Returns response when omitted, otherwise updates sensor entity attributes.

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
