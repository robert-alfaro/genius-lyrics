# genius-lyrics

This is a custom component for Home Assistant to allow fetching song lyrics from [Genius](https://genius.com).

*NOTE:* this is a work in progress -- expect changes.

## Setup

1. Sign up for a free account at genius.com and authorize access to the [Genius API](http://genius.com/api-clients) to get your `client_access_token`.
2. Copy directory `genius_lyrics` from "custom_components" directory in this repository, and place inside your Home Assistant installation's `custom_components` directory.
3. Install markdown card mod [lovelace-markdown-mod](https://github.com/thomasloven/lovelace-markdown-mod)
4. Add the following to your `configuration.yaml`
```
genius_lyrics:

sensors:
  - platform: template
    sensors:
      lyrics:
        friendly_name: "Lyrics"
        value_template: ""
```
5. Create markdown card in lovelace.
```
  - type: markdown
    content: >
      ## [[ sensor.lyrics.attributes.artist ]] - [[ sensor.lyrics.attributes.title ]]

      [[ sensor.lyrics.attributes.lyrics ]]
```
6. Create an automation to call service `genius_lyrics.search_lyrics` upon media_player state change, providing "Artist", "Title".

---

## Screenshot

![lyrics-card](/lyrics-card.png)

---

## Example service call JSON

```json
{
 "api_key":"3SxSxqZJOtz5fYlkFXv-12E-mgripD0XM7v0L091P3Kz22wT9ReCRNg0qmrYeveG",
 "artist_name":"Protoje",
 "song_title":"Mind of a King",
 "entity_id":"sensor.lyrics"
}
```

---

Thanks to
 - @johnwmillr for `lyricsgenius` python package!
 - @thomasloven for lovelace `markdown-mod`!
