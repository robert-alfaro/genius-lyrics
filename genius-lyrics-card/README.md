# Genius Lyrics Card for Home Assistant

A built-in Lovelace card for displaying song lyrics from the Genius Lyrics custom integration.

![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)
![Home Assistant](https://img.shields.io/badge/home%20assistant-2023.1%2B-blue.svg)

## Features

✨ **Smart Display**
- Automatically collapses when no lyrics are available
- Clean, modern design that follows Home Assistant themes
- Responsive layout for mobile and desktop

🎨 **Customizable**
- Visual card editor (no YAML required!)
- Toggle album art, artist/title details
- Toggle stats visibility and placement (`header` or `bottom_left`)
- Configurable height limiting with smooth scrolling
- Configurable lyrics font size + optional on-card font controls
- Show/hide "Open in Genius" button

📝 **Annotations Support**
- Highlight annotated lyrics with yellow underline
- Hover tooltips on desktop
- Click/tap to view full annotations on mobile
- Supports multiple annotations per lyric line

🎵 **Rich Metadata**
- Album artwork display
- Artist and song title
- Pyong count and "Hot" status from Genius
- Direct link to song on Genius.com

## Build

- Source: `src/genius-lyrics-card.ts`
- Build output: `dist/genius-lyrics-card.js`
- Bundled integration asset: `../custom_components/genius_lyrics/www/genius-lyrics-card.js`
- Build command:

```bash
npm install
npm run build
cp dist/genius-lyrics-card.js ../custom_components/genius_lyrics/www/genius-lyrics-card.js
```

## Configuration

### Visual Editor (Recommended)

1. Go to your Lovelace dashboard
2. Click "Edit Dashboard" (top-right menu)
3. Click "+ Add Card"
4. Search for "Genius Lyrics Card"
5. Configure using the visual editor

### YAML Configuration

```yaml
type: custom:genius-lyrics-card
entity: sensor.genius_lyrics  # Required: your Genius lyrics sensor
show_image: true              # Optional: show album art (default: true)
show_details: true            # Optional: show artist/title (default: true)
show_stats: true              # Optional: show pyong/hot stats (default: true)
stats_position: header        # Optional: header or bottom_left (default: header)
show_font_controls: true      # Optional: show +/- font buttons (default: true)
font_size: 14                 # Optional: lyrics font size in px (10..30, default: 14)
max_height: 400               # Optional: max height in pixels, 0 for unlimited (default: 400)
show_genius_button: true      # Optional: show Genius link (default: true)
```

## Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `entity` | string | **Required** | The Genius lyrics sensor entity |
| `show_image` | boolean | `true` | Display album artwork |
| `show_details` | boolean | `true` | Show artist name and song title |
| `show_stats` | boolean | `true` | Show pyong count / hot status |
| `stats_position` | string | `header` | Place stats in `header` or `bottom_left` |
| `show_font_controls` | boolean | `true` | Show in-card font +/- controls |
| `font_size` | number | `14` | Lyrics font size in pixels (`10..30`) |
| `max_height` | number | `400` | Maximum height in pixels for lyrics area. Set to `0` for unlimited height (no scrolling) |
| `show_genius_button` | boolean | `true` | Show the "Open in Genius" button |

## Expected Entity Attributes

The card looks for these attributes on your Genius lyrics sensor:

### Required
- `lyrics` or `media_lyrics` - The song lyrics text

### Optional
- `title` or `media_title` - Song title
- `artist` or `media_artist` - Artist name
- `media_image`, `entity_picture`, or `song_art` - Album artwork URL
- `song_url` or `genius_url` - Direct link to Genius page
- `pyong_count` or `media_pyong_count` - Number of Pyongs
- `stats_hot` or `media_stats_hot` - Boolean indicating if song is "hot"
- `annotations` or `media_annotations` - Object with lyrics annotations

### Annotations Format

Annotations should be an object where keys are lyric snippets and values are arrays of annotation strings:

```json
{
  "lyric line to annotate": [
    "First annotation explaining this line",
    "Second annotation with more context"
  ],
  "another lyric phrase": [
    "Explanation for this phrase"
  ]
}
```

## Usage

### Basic Setup

1. Install the [Genius Lyrics integration](https://github.com/robert-alfaro/genius-lyrics) via HACS
2. Configure a lyrics sensor in your integration
3. Add the Genius Lyrics Card to your dashboard
4. Select your lyrics sensor entity

### Annotations

Annotated lyrics are highlighted with a yellow underline:
- **Desktop**: Hover over highlighted text to see tooltip
- **Mobile**: Tap highlighted text to open annotation modal

## Troubleshooting

### Card doesn't appear in card picker
- Make sure you've added the resource correctly
- Clear browser cache (Ctrl+F5)
- Check browser console for errors

### Entity not found
- Verify your Genius lyrics sensor entity ID
- Make sure the integration is loaded and working
- Check that the entity has a state (not "unavailable")

### Lyrics don't display
- Check that your sensor has a `lyrics` or `media_lyrics` attribute
- Verify the attribute contains text
- Try toggling the entity in Developer Tools → States

### Annotations don't work
- Ensure annotations object is properly formatted
- Keys must exactly match lyrics text (case-sensitive)
- Verify annotations are in the entity attributes

## Styling

The card uses Home Assistant's design tokens and will automatically adapt to your theme:

- `--primary-color` - Accent color for buttons
- `--primary-text-color` - Main text color
- `--secondary-text-color` - Dimmed text (artist, stats)
- `--card-background-color` - Card background
- `--secondary-background-color` - Lyrics box background
- `--divider-color` - Borders and dividers
- `--error-color` - Pyonged button color
- `--ha-card-border-radius` - Border radius for rounded corners

## Examples

### Minimal Card (lyrics only)

```yaml
type: custom:genius-lyrics-card
entity: sensor.genius_lyrics
show_details: false
show_genius_button: false
```

### Compact Card with Limited Height

```yaml
type: custom:genius-lyrics-card
entity: sensor.genius_lyrics
show_image: false
max_height: 250
```

### Full-Height Card (no scrolling)

```yaml
type: custom:genius-lyrics-card
entity: sensor.genius_lyrics
max_height: 0
```

## License

MIT License - see LICENSE file for details

---

**Note**: This is a custom card and is not affiliated with or endorsed by Genius.com or Home Assistant.
