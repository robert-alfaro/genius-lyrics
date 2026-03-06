import { LitElement, css, html } from "lit";
import { unsafeHTML } from "lit/directives/unsafe-html.js";

const CARD_VERSION = "1.0.0";
const ENABLE_PYONG_UI = false;

type Hass = {
  states: Record<string, any>;
  connection: { sendMessage: (message: any) => void };
};

declare global {
  interface Window {
    customCards: any[];
  }
}

console.info(
  `%c GENIUS-LYRICS-CARD %c ${CARD_VERSION} `,
  "color: white; background: #1db954; font-weight: 700;",
  "color: #1db954; background: white; font-weight: 700;"
);

class GeniusLyricsCard extends LitElement {
  public hass?: Hass;
  private config: Record<string, any> = {};
  private _stateObj?: any;

  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
      _stateObj: { type: Object },
    };
  }

  private _renderPyongIcon() {
    return html`<svg class="pyong-icon" viewBox="0 0 11.37 22" aria-hidden="true"><path d="M0 7l6.16-7 3.3 7H6.89S5.5 12.1 5.5 12.17h5.87L6.09 22l.66-7H.88l2.89-8z"></path></svg>`;
  }

  private _isPyongUiEnabled() {
    return ENABLE_PYONG_UI;
  }

  static getConfigElement() {
    return document.createElement("genius-lyrics-card-editor");
  }

  static getStubConfig() {
    return {
      entity: "",
      show_image: true,
      show_details: true,
      show_stats: true,
      stats_position: "header",
      show_font_controls: true,
      font_size: 14,
      max_height: 400,
      show_pyong_button: true,
      show_genius_button: true,
    };
  }

  setConfig(config: Record<string, any>) {
    if (!config.entity) {
      throw new Error("You must specify an entity (Genius Lyrics sensor)");
    }

    this.config = {
      show_image: true,
      show_details: true,
      show_stats: true,
      stats_position: "header",
      show_font_controls: true,
      font_size: 14,
      max_height: 400,
      show_pyong_button: true,
      show_genius_button: true,
      ...config,
    };
  }

  private _getFontSize() {
    const value = parseInt(this.config.font_size, 10);
    if (Number.isNaN(value)) return 14;
    return Math.min(30, Math.max(10, value));
  }

  private _updateCardConfig(newConfig: Record<string, any>) {
    this.config = newConfig;
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: newConfig },
        bubbles: true,
        composed: true,
      })
    );
    this.requestUpdate();
  }

  private _changeFontSize(delta: number) {
    const next = Math.min(30, Math.max(10, this._getFontSize() + delta));
    if (next === this._getFontSize()) return;
    this._updateCardConfig({
      ...this.config,
      font_size: next,
    });
  }

  private _decreaseFontSize() {
    this._changeFontSize(-1);
  }

  private _increaseFontSize() {
    this._changeFontSize(1);
  }

  shouldUpdate() {
    return Boolean(this.config);
  }

  updated(changedProps: Map<string, any>) {
    if (changedProps.has("hass") && this.hass && this.config) {
      const oldHass = changedProps.get("hass");
      const oldState = oldHass?.states?.[this.config.entity];
      const newState = this.hass.states[this.config.entity];

      if (oldState !== newState) {
        this._stateObj = newState;
      }
    }
  }

  getCardSize() {
    return this._hasLyrics() ? 4 : 1;
  }

  private _hasLyrics() {
    if (!this._stateObj) return false;
    const lyrics = this._getLyrics();
    return !!(lyrics && lyrics.trim());
  }

  private _getLyrics() {
    const lyrics =
      this._stateObj?.attributes?.lyrics ||
      this._stateObj?.attributes?.media_lyrics ||
      this._stateObj?.state ||
      "";
    return typeof lyrics === "string" ? lyrics.trimStart().trimEnd() : "";
  }

  private _getArtist() {
    return this._stateObj?.attributes?.artist || this._stateObj?.attributes?.media_artist || "";
  }

  private _getTitle() {
    return this._stateObj?.attributes?.title || this._stateObj?.attributes?.media_title || "";
  }

  private _getImage() {
    return (
      this._stateObj?.attributes?.media_image ||
      this._stateObj?.attributes?.entity_picture ||
      this._stateObj?.attributes?.song_art ||
      ""
    );
  }

  private _getPyongs() {
    return this._stateObj?.attributes?.pyong_count ?? this._stateObj?.attributes?.media_pyong_count ?? null;
  }

  private _getHot() {
    return this._stateObj?.attributes?.stats_hot ?? this._stateObj?.attributes?.media_stats_hot ?? null;
  }

  private _getGeniusUrl() {
    return this._stateObj?.attributes?.song_url || this._stateObj?.attributes?.genius_url || null;
  }

  private _getAnnotations() {
    const annotations = this._stateObj?.attributes?.annotations || this._stateObj?.attributes?.media_annotations;

    if (annotations && typeof annotations === "object") {
      return this._normalizeAnnotations(annotations);
    }

    if (this.config.annotations && typeof this.config.annotations === "object") {
      return this._normalizeAnnotations(this.config.annotations);
    }

    if (this.config.annotations_entity && this.hass) {
      const annoState = this.hass.states[this.config.annotations_entity];
      if (annoState) {
        let data = this.config.annotations_attribute
          ? annoState.attributes?.[this.config.annotations_attribute]
          : annoState.state;

        if (typeof data === "string") {
          try {
            data = JSON.parse(data);
          } catch {
            data = null;
          }
        }

        if (data && typeof data === "object") {
          return this._normalizeAnnotations(data);
        }
      }
    }

    return {};
  }

  private _normalizeAnnotations(obj: Record<string, unknown>) {
    const result: Record<string, string[]> = {};
    for (const [key, value] of Object.entries(obj)) {
      if (Array.isArray(value)) {
        result[key] = value.map(String);
      } else if (value != null) {
        result[key] = [String(value)];
      }
    }
    return result;
  }

  private _handlePyong() {
    if (!this.hass) return;

    const artist = this._getArtist();
    const title = this._getTitle();
    const key = `glc-pyong:${artist}::${title}`;
    const current = localStorage.getItem(key) === "1";
    const next = !current;

    localStorage.setItem(key, next ? "1" : "0");

    this.hass.connection.sendMessage({
      type: "fire_event",
      event_type: "genius_lyrics_pyong",
      event_data: { artist, title, pyonged: next },
    });

    this.requestUpdate();
  }

  private _isPyonged() {
    const artist = this._getArtist();
    const title = this._getTitle();
    const key = `glc-pyong:${artist}::${title}`;
    return localStorage.getItem(key) === "1";
  }

  private _handleOpenGenius() {
    const url = this._getGeniusUrl();
    if (url) {
      window.open(url, "_blank", "noopener,noreferrer");
      return;
    }

    const artist = this._getArtist();
    const title = this._getTitle();
    if (!artist && !title) return;

    const q = encodeURIComponent(`${artist} ${title}`.trim());
    window.open(`https://genius.com/search?q=${q}`, "_blank", "noopener,noreferrer");
  }

  private _applyAnnotations(lyrics: string) {
    const annotations = this._getAnnotations();
    if (!lyrics || !annotations || Object.keys(annotations).length === 0) {
      return this._escapeHtml(lyrics);
    }

    let text = lyrics;
    const used = new Set<string>();
    const keys = Object.keys(annotations).sort((a, b) => b.length - a.length);

    for (const key of keys) {
      if (used.has(key) || !key.trim()) continue;

      const regex = new RegExp(this._escapeRegExp(key), "m");
      const match = text.match(regex);
      if (!match) continue;

      const annoArray = annotations[key] || [];
      const annoText = annoArray.join("\n\n");
      const jsonRaw = JSON.stringify(annoArray).replace(/</g, "\\u003c").replace(/>/g, "\\u003e");

      const span = `<span class="annotated" data-line="${this._escapeHtml(key)}" data-anno="${this._escapeHtml(
        annoText
      )}" data-anno-raw='${jsonRaw}'>${this._escapeHtml(key)}</span>`;

      text = text.replace(regex, span);
      used.add(key);
    }

    return text.replace(/\n/g, "<br>");
  }

  private _escapeRegExp(str: string) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
  }

  private _escapeHtml(str: string) {
    return String(str || "")
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/\"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  private _handleAnnotationClick(e: Event) {
    const target = e.target as HTMLElement | null;
    const node = target?.closest(".annotated") as HTMLElement | null;
    if (!node) return;

    const line = node.getAttribute("data-line") || "";
    const rawJson = node.getAttribute("data-anno-raw") || "[]";
    let annotations: string[] = [];
    try {
      annotations = JSON.parse(rawJson);
    } catch {
      annotations = [];
    }

    this._openAnnotationModal(line, annotations);
  }

  private _openAnnotationModal(line: string, annotations: string[]) {
    const event = new CustomEvent("show-dialog", {
      detail: {
        dialogTag: "genius-lyrics-annotation-dialog",
        dialogImport: () => Promise.resolve(),
        dialogParams: {
          line,
          annotations,
        },
      },
      bubbles: true,
      composed: true,
    });
    this.dispatchEvent(event);

    const text = annotations.join("\n\n");
    if (text) {
      setTimeout(() => alert(`"${line}"\n\n${text}`), 100);
    }
  }

  render() {
    if (!this.hass || !this.config) {
      return html``;
    }

    const stateObj = this.hass.states[this.config.entity];
    if (!stateObj) {
      return html`
        <ha-card>
          <div class="warning">Entity ${this.config.entity} not found</div>
        </ha-card>
      `;
    }

    this._stateObj = stateObj;

    const state = stateObj.state?.toLowerCase();
    const mediaLyrics = stateObj.attributes?.media_lyrics;
    const lyricsNotFound =
      typeof mediaLyrics === "string" &&
      mediaLyrics.trim().toLowerCase() === "lyrics not found";

    if (state === "off" && lyricsNotFound) {
      return this._renderLyricsNotFound();
    }

    if (state === "off" || state === "unavailable" || state === "unknown") {
      return this._renderOffState();
    }

    if (!this._hasLyrics()) {
      return this._renderNoLyrics();
    }

    return this._renderWithLyrics();
  }

  private _renderOffState() {
    return html`
      <ha-card>
        <div class="no-lyrics">
          <ha-icon icon="mdi:power-off"></ha-icon>
          <div class="no-lyrics-text">No media playing</div>
        </div>
      </ha-card>
    `;
  }

  private _renderNoLyrics() {
    return html`
      <ha-card>
        <div class="no-lyrics">
          <ha-icon icon="mdi:music-note-off"></ha-icon>
          <div class="no-lyrics-text">No lyrics available</div>
        </div>
      </ha-card>
    `;
  }

  private _renderLyricsNotFound() {
    return html`
      <ha-card>
        <div class="no-lyrics">
          <ha-icon icon="mdi:file-search-outline"></ha-icon>
          <div class="no-lyrics-text">No lyrics found</div>
        </div>
      </ha-card>
    `;
  }

  private _renderWithLyrics() {
    const artist = this._getArtist();
    const title = this._getTitle();
    const image = this._getImage();
    const lyrics = this._getLyrics();
    const pyongs = this._getPyongs();
    const hot = this._getHot();
    const showImage = this.config.show_image && image;
    const showDetails = this.config.show_details;
    const showStats = this.config.show_stats !== false;
    const statsInBottomLeft = showStats && this.config.stats_position === "bottom_left";
    const statsInHeader = showStats && !statsInBottomLeft;
    const showFontControls = this.config.show_font_controls !== false;
    const isPyonged = this._isPyonged();
    const fontSize = this._getFontSize();

    const processedLyrics = this._applyAnnotations(lyrics);
    const maxHeight = parseInt(this.config.max_height, 10);
    const lyricsStyle =
      maxHeight > 0
        ? `max-height: ${maxHeight}px; overflow-y: auto; font-size: ${fontSize}px;`
        : `font-size: ${fontSize}px;`;

    return html`
      <ha-card>
        <div class="card-content">
          <div class="header">
            ${showImage
              ? html`
                  <img class="cover" src="${image}" alt="${title}" />
                `
              : ""}
            ${showDetails || statsInHeader
              ? html`
                  <div class="meta">
                    ${showDetails ? html`<div class="title" title="${title || "-"}">${title || "-"}</div>` : ""}
                    ${showDetails && artist ? html`<div class="artist">${artist}</div>` : ""}
                    ${statsInHeader && (pyongs !== null || hot === true)
                      ? html`
                          <div class="stats">
                            ${pyongs !== null
                              ? html`<span title="Pyong count">${this._renderPyongIcon()}${pyongs}</span>`
                              : ""}
                            ${hot === true ? html`<span title="Hot on Genius">🔥 Hot</span>` : ""}
                          </div>
                        `
                      : ""}
                  </div>
                `
              : ""}
          </div>

          <div class="lyrics" style="${lyricsStyle}" @click="${this._handleAnnotationClick}">${processedLyrics ? unsafeHTML(processedLyrics) : ""}</div>

          ${statsInBottomLeft ||
          showFontControls ||
          (this._isPyongUiEnabled() && this.config.show_pyong_button) ||
          this.config.show_genius_button
            ? html`
                <div class="actions">
                  ${statsInBottomLeft || showFontControls
                    ? html`
                        <div class="left-controls">
                          ${statsInBottomLeft && (pyongs !== null || hot === true)
                            ? html`
                                <div class="stats bottom-stats">
                                  ${pyongs !== null
                                    ? html`<span title="Pyong count">${this._renderPyongIcon()}${pyongs}</span>`
                                    : ""}
                                  ${hot === true ? html`<span title="Hot on Genius">🔥 Hot</span>` : ""}
                                </div>
                              `
                            : ""}
                          ${showFontControls
                            ? html`
                                <div class="font-controls">
                                  <mwc-button dense outlined @click="${this._increaseFontSize}" class="font-btn" title="Increase font size">
                                    <ha-icon icon="mdi:format-font-size-increase"></ha-icon>
                                  </mwc-button>
                                  <mwc-button dense outlined @click="${this._decreaseFontSize}" class="font-btn" title="Decrease font size">
                                    <ha-icon icon="mdi:format-font-size-decrease"></ha-icon>
                                  </mwc-button>
                                </div>
                              `
                            : ""}
                        </div>
                      `
                    : ""}
                  ${this._isPyongUiEnabled() && this.config.show_pyong_button
                    ? html`
                        <mwc-button
                          dense
                          outlined
                          @click="${this._handlePyong}"
                          class="pyong-btn ${isPyonged ? "pyonged" : ""}"
                        >
                          ${this._renderPyongIcon()}
                          ${isPyonged ? "Pyonged" : "Pyong"}
                        </mwc-button>
                      `
                    : ""}
                  ${this.config.show_genius_button
                    ? html`
                        <mwc-button dense outlined @click="${this._handleOpenGenius}" class="genius-btn">
                          <ha-icon icon="mdi:open-in-new"></ha-icon>
                          Open in Genius
                        </mwc-button>
                      `
                    : ""}
                </div>
              `
            : ""}
        </div>
      </ha-card>
    `;
  }

  static get styles() {
    return css`
      :host {
        display: block;
      }

      ha-card {
        height: 100%;
      }

      .card-content {
        padding: 16px;
      }

      .warning {
        padding: 16px;
        color: var(--error-color, #db4437);
        font-weight: 500;
      }

      .no-lyrics {
        padding: 24px;
        text-align: center;
        opacity: 0.6;
      }

      .no-lyrics ha-icon {
        --mdc-icon-size: 48px;
        color: var(--secondary-text-color);
      }

      .no-lyrics-text {
        margin-top: 8px;
        font-size: 14px;
        color: var(--secondary-text-color);
      }

      .header {
        display: grid;
        grid-template-columns: auto 1fr;
        gap: 16px;
        margin-bottom: 16px;
        align-items: start;
      }

      .cover {
        width: 80px;
        height: 80px;
        border-radius: var(--ha-card-border-radius, 12px);
        object-fit: cover;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
      }

      .meta {
        display: flex;
        flex-direction: column;
        gap: 4px;
        min-width: 0;
      }

      .title {
        font-size: 18px;
        font-weight: 600;
        color: var(--primary-text-color);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .artist {
        font-size: 14px;
        color: var(--secondary-text-color);
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      .stats {
        display: flex;
        gap: 12px;
        font-size: 12px;
        color: var(--secondary-text-color);
        margin-top: 4px;
      }

      .stats span {
        display: inline-flex;
        align-items: center;
        gap: 4px;
      }

      .stats .pyong-icon {
        color: var(--primary-text-color);
      }

      .bottom-stats {
        margin-top: 0;
      }

      .lyrics {
        background: var(--secondary-background-color);
        border-radius: var(--ha-card-border-radius, 12px);
        padding: 16px;
        line-height: 1.6;
        white-space: pre-wrap;
        word-wrap: break-word;
        font-size: 14px;
        color: var(--primary-text-color);
        margin-bottom: 12px;
        user-select: text;
        -webkit-user-select: text;
        -moz-user-select: text;
        -ms-user-select: text;
        cursor: text;
      }

      .lyrics::-webkit-scrollbar {
        width: 8px;
      }

      .lyrics::-webkit-scrollbar-track {
        background: transparent;
      }

      .lyrics::-webkit-scrollbar-thumb {
        background: var(--divider-color);
        border-radius: 4px;
      }

      .lyrics::-webkit-scrollbar-thumb:hover {
        background: var(--secondary-text-color);
      }

      .annotated {
        background: linear-gradient(transparent 65%, rgba(255, 193, 7, 0.3) 0);
        cursor: help;
        position: relative;
        padding: 0 2px;
      }

      .annotated:hover {
        background: linear-gradient(transparent 65%, rgba(255, 193, 7, 0.5) 0);
      }

      @media (hover: hover) {
        .annotated[data-anno]:hover::after {
          content: attr(data-anno);
          position: absolute;
          left: 0;
          top: 100%;
          z-index: 1000;
          min-width: 200px;
          max-width: 400px;
          white-space: pre-wrap;
          padding: 12px;
          margin-top: 8px;
          background: var(--card-background-color);
          border: 1px solid var(--divider-color);
          border-radius: 8px;
          box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
          color: var(--primary-text-color);
          font-size: 13px;
          line-height: 1.5;
          pointer-events: none;
        }
      }

      .actions {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 8px;
        flex-wrap: wrap;
      }

      .actions .pyong-btn {
        margin-right: auto;
      }

      .left-controls {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        margin-right: auto;
      }

      .font-controls {
        display: inline-flex;
        align-items: center;
        gap: 6px;
      }

      .font-btn {
        min-width: 0;
      }

      .actions .genius-btn {
        margin-left: auto;
      }

      mwc-button {
        --mdc-theme-primary: var(--primary-color);
        --mdc-typography-button-font-size: 13px;
        --mdc-button-horizontal-padding: 14px;
        transition: background-color 140ms ease, box-shadow 140ms ease, transform 140ms ease;
        border-radius: 10px;
        padding: 3px;
      }

      mwc-button ha-icon {
        --mdc-icon-size: 18px;
        margin-right: 4px;
      }

      .pyong-icon {
        display: inline-block;
        width: 18px;
        height: 18px;
        fill: currentColor;
        vertical-align: text-bottom;
      }

      mwc-button.pyonged {
        --mdc-theme-primary: var(--error-color, #db4437);
      }

      .pyong-btn:hover,
      .genius-btn:hover,
      .font-btn:hover,
      .pyong-btn:focus-within,
      .genius-btn:focus-within,
      .font-btn:focus-within {
        background-color: rgba(203, 203, 203, 0.1);
        box-shadow: 0 1px 8px rgba(0, 0, 0, 0.12);
        transform: translateY(-1px);
      }

      .pyong-btn.pyonged:hover,
      .pyong-btn.pyonged:focus-within {
        background-color: rgba(203, 203, 203, 0.1);
      }

      @media (max-width: 600px) {
        .header {
          grid-template-columns: 60px 1fr;
          gap: 12px;
        }

        .cover {
          width: 60px;
          height: 60px;
        }

        .title {
          font-size: 16px;
        }

        .artist {
          font-size: 13px;
        }
      }
    `;
  }
}

customElements.define("genius-lyrics-card", GeniusLyricsCard);

class GeniusLyricsCardEditor extends LitElement {
  public hass?: Hass;
  private config: Record<string, any> = {};

  static get properties() {
    return {
      hass: { type: Object },
      config: { type: Object },
    };
  }

  setConfig(config: Record<string, any>) {
    this.config = {
      show_image: true,
      show_details: true,
      show_stats: true,
      stats_position: "header",
      show_font_controls: true,
      font_size: 14,
      max_height: 400,
      show_pyong_button: true,
      show_genius_button: true,
      ...config,
    };
  }

  private configChanged(newConfig: Record<string, any>) {
    this.dispatchEvent(
      new CustomEvent("config-changed", {
        detail: { config: newConfig },
        bubbles: true,
        composed: true,
      })
    );
  }

  private _valueChanged(ev: Event & { detail?: { value?: any } }) {
    if (!this.config || !this.hass) return;

    const target = ev.target as any;
    const configValue = target.configValue;
    if (!configValue) return;

    let value = ev.detail?.value ?? target.value;

    if (target.type === "checkbox" || target.tagName === "HA-SWITCH") {
      value = target.checked;
    } else if (target.type === "number") {
      value = parseInt(target.value, 10);
    }

    if (this.config[configValue] === value) return;

    const newConfig = {
      ...this.config,
      [configValue]: value,
    };

    this.config = newConfig;
    this.configChanged(newConfig);
    this.requestUpdate();
  }

  private _statsPositionChanged(ev: Event) {
    if (!this.config || !this.hass) return;
    const target = ev.target as any;
    const newConfig = {
      ...this.config,
      stats_position: target.checked ? "bottom_left" : "header",
    };
    this.config = newConfig;
    this.configChanged(newConfig);
    this.requestUpdate();
  }

  render() {
    if (!this.hass || !this.config) {
      return html``;
    }

    return html`
      <div class="card-config">
        <ha-entity-picker
          .hass="${this.hass}"
          .value="${this.config.entity || ""}"
          .configValue="${"entity"}"
          .label="${"Entity (Required)"}"
          .required="${true}"
          allow-custom-entity
          @value-changed="${this._valueChanged}"
        ></ha-entity-picker>

        <div class="side-by-side">
          <ha-formfield label="Show Album Art">
            <ha-switch
              .checked="${this.config.show_image !== false}"
              .configValue="${"show_image"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>

          <ha-formfield label="Show Details (Artist/Title)">
            <ha-switch
              .checked="${this.config.show_details !== false}"
              .configValue="${"show_details"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="side-by-side">
          <ha-formfield label="Show Stats (Pyongs/Hot)">
            <ha-switch
              .checked="${this.config.show_stats !== false}"
              .configValue="${"show_stats"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>

          <ha-formfield label="Show Font Size Buttons">
            <ha-switch
              .checked="${this.config.show_font_controls !== false}"
              .configValue="${"show_font_controls"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>

        <div class="side-by-side">
          <ha-formfield label="Place Stats in Lower Left">
            <ha-switch
              .checked="${this.config.stats_position === "bottom_left"}"
              @change="${this._statsPositionChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>

        <ha-textfield
          label="Max Height (px) - Set to 0 for unlimited"
          type="number"
          min="0"
          max="2000"
          step="1"
          .value="${String(this.config.max_height ?? 400)}"
          .configValue="${"max_height"}"
          @change="${this._valueChanged}"
        ></ha-textfield>

        <ha-textfield
          label="Lyrics Font Size (px)"
          type="number"
          min="10"
          max="30"
          step="1"
          .value="${String(this.config.font_size ?? 14)}"
          .configValue="${"font_size"}"
          @change="${this._valueChanged}"
        ></ha-textfield>

        <div class="side-by-side">
          <ha-formfield label="Show Genius Button">
            <ha-switch
              .checked="${this.config.show_genius_button !== false}"
              .configValue="${"show_genius_button"}"
              @change="${this._valueChanged}"
            ></ha-switch>
          </ha-formfield>
        </div>
      </div>
    `;
  }

  static get styles() {
    return css`
      .card-config {
        display: flex;
        flex-direction: column;
        gap: 16px;
      }

      .side-by-side {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
      }

      ha-formfield {
        display: flex;
        align-items: center;
        padding: 8px 0;
      }
    `;
  }
}

customElements.define("genius-lyrics-card-editor", GeniusLyricsCardEditor);

window.customCards = window.customCards || [];
window.customCards.push({
  type: "genius-lyrics-card",
  name: "Genius Lyrics Card",
  description: "Display song lyrics from Genius with annotations support",
  preview: true,
  documentationURL: "https://github.com/robert-alfaro/genius-lyrics",
});
