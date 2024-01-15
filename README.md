# genius-lyrics

Custom component for Home Assistant to fetch song lyrics from [Genius](https://genius.com)
by tracking media player entities. Component allows service calls for custom automations.

## Installation

### With HACS

1. Open HACS Settings and add this repository (https://github.com/robert-alfaro/genius-lyrics)
   as a Custom Repository (use **Integration** as the category).
2. The `Genius Lyrics` page should automatically load (or find it in the HACS Store).
3. Click `Install`

### Manual

Copy the `genius_lyrics` directory from `custom_components` in this repository, and place inside your
Home Assistant installation's `custom_components` directory.

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

##### JSON

```json
{
  "media_artist": "Protoje",
  "media_title": "Mind of a King",
  "entity_id": "sensor.foobar_lyrics"
}
```

##### YAML

```yaml
media_artist: "Protoje"
media_title: "Mind of a King"
entity_id: sensor.foobar_lyrics
```

## Screenshot

![lyrics-card](images/lyrics-card.png)

---

Thanks to

- @johnwmillr for `lyricsgenius` python package!
