# Interactive U.S. and TAMU Lease Map

This project is a local interactive web map. The first screen is an SVG map of the United States. Clicking the Texas A&M University pin opens a College Station Leaflet map with road data and rental housing pins.

## How to Run

The main page should be opened through the included local Node static server, not by double-clicking `index.html`.

This is needed because the College Station map uses `fetch("college_station.geojson")`. Browsers usually block local file reads when a page is opened with `file://`, while `http://127.0.0.1:8765/` lets the page and GeoJSON file be served from the same local origin.

### Easy Mode: Download ZIP

Use this path if you only want to download the project and see the same effect locally.

Requirements:

- Node.js installed on your computer. Download and install the LTS version from [nodejs.org](https://nodejs.org/).
- This repository downloaded locally. Click the green **Code** button on the GitHub page, choose **Download ZIP**, then extract the ZIP file onto your computer.

Steps:

1. Open your terminal, command prompt, or PowerShell inside the extracted project folder.
2. Run:

```bash
cd outputs
node static_server.js
```

Keep this terminal window open. Closing it will stop the local server.

Then open this address in your browser:

```text
http://127.0.0.1:8765/index.html
```

### Expert Mode: Git Clone

Use this path if you are comfortable with Git and want to keep the project connected to GitHub.

```bash
git clone https://github.com/handsomegary/tamu-lease-map.git
cd tamu-lease-map/outputs
node static_server.js
```

Then open:

```text
http://127.0.0.1:8765/index.html
```

On Windows, `cd tamu-lease-map\outputs` also works.

## Project Structure

```text
.
|-- README.md
|-- .gitignore
|-- outputs/
|   |-- index.html
|   |-- static_server.js
|   |-- college_station.geojson
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

The main application. It contains:

- The full interactive U.S. SVG map.
- State hover and zoom behavior.
- The Texas A&M pin at the College Station campus coordinate.
- The TAMU secondary zoom into the College Station Leaflet panel.
- The hard-coded `leaseData` rental list.
- The Leaflet setup for rental markers, popups, and road overlay.

`outputs/static_server.js`

A small local Node HTTP server. It serves files from `outputs/` on:

```text
http://127.0.0.1:8765/
```

It is local only. It is used so the browser can load `college_station.geojson` through `fetch()`.

`outputs/college_station.geojson`

The OpenStreetMap-derived road data for College Station. The current map renders LineString and MultiLineString features from this file as dark gray roads:

- Color: `#7a7a7a`
- Weight: `2.5`
- Opacity: `0.6`
- `lineCap: "round"`
- `lineJoin: "round"`

`outputs/export.geojson`

Earlier raw OpenStreetMap-style export kept as a source/reference copy.

`outputs/leases.geojson`

Earlier Google My Maps / converted lease point data. The current main map does not depend on this file anymore because the active rental data is hard-coded in `leaseData` inside `outputs/index.html`.

`outputs/tamu-geojson.js`

Earlier generated JavaScript wrapper for GeoJSON. The current main map does not depend on this file anymore.

`outputs/tamu_leaflet_rentals.html`

Standalone Leaflet rental-map prototype kept for reference. The active user flow is now integrated into `outputs/index.html`.

`work/`

Development/source helpers used while building the SVG U.S. map:

- `blank-us-map.svg`: original working SVG map source.
- `build_interactive_map.py`: helper script used to build the interactive map output.
- `map_projection_check.py`: helper script for checking TAMU coordinate placement.
- `states-10m.json`: map/geographic source data used during development.

## Online Sources and External Dependencies

The project is mostly local, but the College Station Leaflet map currently uses online resources.

### Leaflet.js

Used by: `outputs/index.html`

Source:

```html
https://unpkg.com/leaflet@1.9.4/dist/leaflet.css
https://unpkg.com/leaflet@1.9.4/dist/leaflet.js
```

Purpose:

- Provides the interactive slippy map engine.
- Provides pan, zoom, tile rendering, `L.map`, `L.tileLayer`, `L.geoJSON`, `L.marker`, popups, layer controls, and marker icons.

Network requirement:

- Required unless Leaflet CSS/JS is downloaded and served locally.

### CartoDB Positron Light No Labels Tile Layer

Used by: the TAMU College Station Leaflet view inside `outputs/index.html`

Tile URL:

```js
https://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}{r}.png
```

Attribution used in code:

```html
&copy; OpenStreetMap contributors &copy; CARTO
```

Purpose:

- Provides the light gray minimalist base map.
- The "No Labels" version keeps the custom rental markers and local road overlay visually clear.

Network requirement:

- Required for the online base-map tiles.
- If offline, the Leaflet panel can still render local roads and markers only if Leaflet is available locally, but the CartoDB base tiles will not appear.

### OpenStreetMap Data

Used by:

- `outputs/college_station.geojson`
- CartoDB tile attribution

Purpose:

- `college_station.geojson` contains local road geometry from OpenStreetMap-derived data.
- The CartoDB tile layer is also based on OpenStreetMap data.

Current use:

- Road geometry is stored locally in `outputs/college_station.geojson`.
- The browser loads it from the local Node server using `fetch("college_station.geojson")`.

Network requirement:

- The road overlay itself does not require the internet after the GeoJSON file exists locally.
- It does require the local HTTP server because the page uses `fetch()`.

### Wikimedia Commons / U.S. SVG Map Source

Used by: original U.S. map outline in `outputs/index.html`

Source noted during development:

```text
Blank US Map (states only).svg, Wikimedia Commons, CC0
```

Purpose:

- Base geometry for the U.S. states SVG map.
- The page customizes this SVG into interactive states with hover and zoom behavior.

Network requirement:

- None at runtime. The SVG geometry is embedded in `outputs/index.html`.

### Texas A&M Coordinate

Used by: TAMU pin and zoom target

Coordinate:

```text
30.6099 N, 96.3405 W
```

Purpose:

- Places the TAMU pin on the U.S. SVG map.
- Clicking this pin opens the College Station Leaflet rental map.

Network requirement:

- None.

## Runtime Behavior

1. User opens `http://127.0.0.1:8765/index.html`.
2. The U.S. SVG map appears.
3. Hovering states creates the raised state effect.
4. Clicking a state zooms into that state.
5. Clicking the TAMU pin opens the full-screen College Station Leaflet panel.
6. Leaflet loads from Unpkg.
7. CartoDB Positron Light No Labels tiles load from Carto.
8. `college_station.geojson` is fetched locally from the Node server.
9. Rental markers are generated from the hard-coded `leaseData` array.
10. Clicking a rental pin opens a `.tamu-popup` with:
    - Apartment name
    - Address
    - Rent in red bold text
    - Bus stop
    - Bus route badge

## Offline Notes

The U.S. SVG map is embedded and can display offline.

The current College Station Leaflet map needs online access for:

- Leaflet JS/CSS from Unpkg
- CartoDB map tiles

To make the College Station map more offline-friendly:

1. Download Leaflet JS/CSS into `outputs/vendor/leaflet/`.
2. Change `index.html` to reference those local files.
3. Replace `fetch("college_station.geojson")` with an embedded JS variable or keep using the local Node server.
4. Accept a blank/minimal background, or prepare offline map tiles.

## Git Notes

The public GitHub repository is:

```text
https://github.com/handsomegary/tamu-lease-map
```

The default branch is `main`.

