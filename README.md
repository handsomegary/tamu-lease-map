# TAMU and Surrounding Cities Map

A local interactive map centered on Texas A&M University and surrounding Texas city areas. The app starts from a Texas-focused SVG view, then opens a unified Leaflet map for TAMU, TX-6, Houston/IAH, and related pins using one combined road file: `export.geojson`.

## How to Run

The main page should be opened through the included local Node static server, not by double-clicking `index.html`.

This is needed because the Leaflet map uses `fetch("export.geojson")`. Browsers usually block local file reads when a page is opened with `file://`, while `http://127.0.0.1:8765/` lets the page and GeoJSON file be served from the same local origin.

### Easy Mode: Download ZIP

Requirements:

- Node.js installed on your computer. Download the LTS version from [nodejs.org](https://nodejs.org/).
- This repository downloaded locally. Click **Code**, choose **Download ZIP**, then extract it.

Windows one-click option:

1. Open the `outputs` folder.
2. Double-click `click_to_open_the_whole_project.bat`.
3. Keep the server window open while using the map.

Manual terminal option:

```bash
cd outputs
node static_server.js
```

Then open:

```text
http://127.0.0.1:8765/index.html
```

### Expert Mode: Git Clone

```bash
git clone https://github.com/handsomegary/tamu-lease-map.git
cd tamu-lease-map/outputs
node static_server.js
```

If the repository has been renamed, use the new repository URL and folder name instead.

## Current Features

- Texas-focused SVG entry view.
- TAMU pin that opens a Leaflet view centered near Wisenbaker Engineering Building.
- Houston / IAH pin that opens the Houston Leaflet view.
- One shared Leaflet map for TAMU and Houston, with animated `flyToBounds()` transitions.
- One combined road source: `outputs/export.geojson` for TAMU, TX-6, and Houston road lines.
- TAMU rental pins from the hard-coded `leaseData` array in `outputs/index.html`.
- TAMU campus building pins, including Wisenbaker, Sterling C. Evans Library, Sbisa Dining Hall, and Commons Dining Hall.
- Houston pins for George Bush Intercontinental Airport (IAH) and the Taipei Economic & Cultural Office in Houston.
- Leaflet layer control for Roads, Leases, Campus buildings, and IAH / TECO.

## Project Structure

```text
.
|-- README.md
|-- .gitignore
|-- outputs/
|   |-- index.html
|   |-- static_server.js
|   |-- click_to_open_the_whole_project.bat
|   |-- export.geojson
|   |-- leases.geojson
|   |-- tamu-geojson.js
|   `-- tamu_leaflet_rentals.html
`-- work/
    |-- blank-us-map.svg
    |-- build_interactive_map.py
    |-- map_projection_check.py
    `-- states-10m.json
```

## Main Files

`outputs/index.html`

The main application. It contains the Texas SVG entry view, TAMU/Houston pin behavior, the unified Leaflet map, hard-coded lease/building/place pin data, popups, layer controls, and road rendering from `export.geojson`.

`outputs/export.geojson`

The combined OpenStreetMap-derived road data for TAMU, TX-6, and Houston. The current map renders LineString and MultiLineString features from this file as dark gray road lines.

`outputs/static_server.js`

A small local Node HTTP server that serves files from `outputs/` on:

```text
http://127.0.0.1:8765/
```

`outputs/click_to_open_the_whole_project.bat`

Windows one-click launcher. It opens the local map URL, starts `node static_server.js`, and keeps the server window open.

`outputs/leases.geojson`

Older converted lease point data kept for reference. The active main page uses the hard-coded `leaseData` array inside `outputs/index.html`.

`outputs/tamu_leaflet_rentals.html`

Standalone Leaflet rental-map prototype kept for reference. The active user flow is integrated into `outputs/index.html`.

## Online Sources and External Dependencies

### Leaflet.js

Used by `outputs/index.html`:

```html
https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
```

Leaflet provides the interactive map engine, markers, popups, layer controls, and GeoJSON rendering.

### CartoDB Positron Light No Labels

Tile URL:

```js
https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png
```

This provides the light basemap behind the custom road overlay and pins.

### OpenStreetMap-Derived Road Data

`outputs/export.geojson` stores the combined local road geometry. The road overlay does not need internet once the file exists locally, but the page must be served through the local HTTP server so `fetch("export.geojson")` works.

### SVG Map Source

The original U.S. state outline came from Wikimedia Commons `Blank US Map (states only).svg`, CC0. Runtime SVG geometry is embedded in `outputs/index.html`.

## Runtime Behavior

1. Open `http://127.0.0.1:8765/index.html`.
2. The Texas-focused SVG entry view appears.
3. Click the TAMU pin to open the unified Leaflet map at the TAMU view.
4. Click the Houston / IAH pin to open the same Leaflet map at the Houston view.
5. Leaflet loads from Unpkg.
6. CartoDB Positron tiles load from Carto.
7. `export.geojson` is fetched locally and rendered as the road overlay.
8. TAMU lease/building pins and Houston place pins are generated from data inside `outputs/index.html`.

## Offline Notes

The SVG entry view is embedded and can display offline.

The Leaflet map currently needs online access for:

- Leaflet JS/CSS from Unpkg
- CartoDB map tiles

To make the Leaflet map more offline-friendly:

1. Download Leaflet JS/CSS into `outputs/vendor/leaflet/`.
2. Change `index.html` to reference those local files.
3. Keep serving the project through the local Node server, or embed the GeoJSON directly into JavaScript.
4. Accept a blank/minimal background, or prepare offline map tiles.

## Git Notes

Current public repository:

```text
https://github.com/handsomegary/tamu-lease-map
```

Suggested repository name if renamed:

```text
tamu-surrounding-cities-map
```

The default branch is `main`.