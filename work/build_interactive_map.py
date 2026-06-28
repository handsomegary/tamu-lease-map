from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
SVG_SOURCE = ROOT / "work" / "blank-us-map.svg"
OUTPUT = ROOT / "outputs" / "index.html"


def prepare_svg(raw_svg: str) -> str:
    svg = raw_svg.replace('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n', "")
    svg = re.sub(r"<defs>.*?</defs>\s*", "", svg, flags=re.S)
    svg = svg.replace(
        '<svg xmlns="http://www.w3.org/2000/svg" width="959" height="593">',
        '<svg id="usa-map" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 959 593" role="img" aria-labelledby="mapTitle mapDesc" preserveAspectRatio="xMidYMid meet">',
    )
    svg = re.sub(
        r"\s*<title>Blank map of the United States, territories not included</title>\s*",
        "\n  <title id=\"mapTitle\">Interactive U.S. map</title>\n"
        "  <desc id=\"mapDesc\">Fifty U.S. states plus the District of Columbia.</desc>\n",
        svg,
        count=1,
    )
    return svg


def build_html(svg: str) -> str:
    return f"""<!doctype html>
<html lang="zh-Hant">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>互動式美國地圖</title>
  <style>
    :root {{
      color-scheme: light;
      --page: #f5f1ea;
      --ink: #1f2d36;
      --muted: #65727c;
      --line: #d8cfc2;
      --panel: #fffdf8;
      --state: #d9e1e6;
      --state-alt: #ccd7dd;
      --hover: #ff8a5c;
      --active: #1f9d8a;
      --focus: #f2c94c;
      --border: #ffffff;
      --shadow: 0 22px 50px rgba(31, 45, 54, 0.16);
    }}

    * {{
      box-sizing: border-box;
    }}

    body {{
      margin: 0;
      min-height: 100vh;
      background:
        linear-gradient(180deg, rgba(31, 157, 138, 0.08), transparent 42%),
        var(--page);
      color: var(--ink);
      font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    main {{
      min-height: 100vh;
      display: flex;
      flex-direction: column;
      gap: 18px;
      padding: 28px;
    }}

    .topbar {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 18px;
      max-width: 1180px;
      width: 100%;
      margin: 0 auto;
    }}

    h1 {{
      margin: 0;
      font-size: 2.25rem;
      line-height: 1.05;
      letter-spacing: 0;
    }}

    .subtitle {{
      margin: 8px 0 0;
      color: var(--muted);
      font-size: 1rem;
      line-height: 1.45;
    }}

    .readout {{
      min-width: 210px;
      padding: 12px 14px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background: rgba(255, 253, 248, 0.86);
      box-shadow: 0 12px 30px rgba(31, 45, 54, 0.08);
    }}

    .readout-label {{
      display: block;
      color: var(--muted);
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0;
    }}

    .readout-state {{
      display: flex;
      align-items: baseline;
      gap: 10px;
      margin-top: 5px;
      white-space: nowrap;
    }}

    .readout-name {{
      font-size: 1.15rem;
      font-weight: 800;
    }}

    .readout-code {{
      color: var(--active);
      font-size: 0.95rem;
      font-weight: 800;
    }}

    .map-board {{
      position: relative;
      flex: 1;
      display: grid;
      place-items: center;
      max-width: 1180px;
      width: 100%;
      margin: 0 auto;
      padding: 18px;
      border: 1px solid var(--line);
      border-radius: 8px;
      background:
        radial-gradient(circle at 18% 12%, rgba(242, 201, 76, 0.18), transparent 30%),
        linear-gradient(135deg, rgba(255, 255, 255, 0.86), rgba(255, 253, 248, 0.72));
      box-shadow: var(--shadow);
      overflow: visible;
    }}

    .map-frame {{
      width: min(100%, 1080px);
      overflow: visible;
    }}

    #usa-map {{
      display: block;
      width: 100%;
      height: auto;
      max-height: 72vh;
      overflow: visible;
      filter: drop-shadow(0 12px 18px rgba(31, 45, 54, 0.08));
    }}

    #usa-map g.state > path,
    #usa-map circle.dc {{
      fill: var(--state);
      stroke: rgba(31, 45, 54, 0.16);
      stroke-width: 0.8;
      cursor: pointer;
      transition: fill 160ms ease, filter 160ms ease, transform 160ms ease, stroke 160ms ease;
      transform-box: fill-box;
      transform-origin: center;
      outline: none;
    }}

    #usa-map g.state > path:nth-child(3n) {{
      fill: var(--state-alt);
    }}

    #usa-map g.state > path.dc {{
      pointer-events: none;
    }}

    #usa-map g.state > path:hover,
    #usa-map g.state > path.is-active,
    #usa-map g.state > path:focus-visible,
    #usa-map circle.dc:hover,
    #usa-map circle.dc.is-active,
    #usa-map circle.dc:focus-visible {{
      fill: var(--hover);
      stroke: rgba(31, 45, 54, 0.42);
      transform: translateY(-4px);
      filter: drop-shadow(0 12px 10px rgba(31, 45, 54, 0.23));
    }}

    #usa-map g.state > path:focus-visible,
    #usa-map circle.dc:focus-visible {{
      stroke: var(--focus);
      stroke-width: 2.4;
    }}

    #usa-map g.borders,
    #usa-map .separator1 {{
      pointer-events: none;
    }}

    #usa-map g.borders path {{
      stroke: var(--border);
      stroke-width: 1.15;
      stroke-linecap: round;
      stroke-linejoin: round;
    }}

    #usa-map .separator1 {{
      stroke: rgba(101, 114, 124, 0.54);
      stroke-width: 2;
      fill: none;
    }}

    .tooltip {{
      position: fixed;
      z-index: 20;
      left: 0;
      top: 0;
      max-width: min(280px, calc(100vw - 24px));
      padding: 9px 11px;
      border: 1px solid rgba(31, 45, 54, 0.14);
      border-radius: 8px;
      background: rgba(31, 45, 54, 0.95);
      color: white;
      font-size: 0.92rem;
      font-weight: 800;
      pointer-events: none;
      transform: translate(-50%, calc(-100% - 14px));
      box-shadow: 0 16px 32px rgba(31, 45, 54, 0.24);
    }}

    .tooltip small {{
      display: block;
      margin-top: 2px;
      color: rgba(255, 255, 255, 0.68);
      font-size: 0.72rem;
      font-weight: 700;
    }}

    .credit {{
      max-width: 1180px;
      width: 100%;
      margin: 0 auto;
      color: var(--muted);
      font-size: 0.82rem;
      line-height: 1.5;
    }}

    .credit a {{
      color: var(--ink);
      font-weight: 700;
      text-decoration-thickness: 1px;
      text-underline-offset: 3px;
    }}

    @media (max-width: 760px) {{
      main {{
        padding: 16px;
        gap: 14px;
      }}

      .topbar {{
        align-items: stretch;
        flex-direction: column;
      }}

      h1 {{
        font-size: 1.8rem;
        line-height: 1.1;
      }}

      .subtitle {{
        font-size: 0.95rem;
      }}

      .readout {{
        min-width: 0;
        width: 100%;
      }}

      .readout-state {{
        white-space: normal;
      }}

      .map-board {{
        padding: 10px;
      }}

      #usa-map {{
        max-height: 64vh;
      }}
    }}
  </style>
</head>
<body>
  <main>
    <header class="topbar">
      <div>
        <h1>互動式美國地圖</h1>
        <p class="subtitle">50 州 + 華盛頓 DC，共 51 個互動區域。</p>
      </div>
      <aside class="readout" aria-live="polite">
        <span class="readout-label">目前區域</span>
        <div class="readout-state">
          <span class="readout-name" data-state-name>United States</span>
          <span class="readout-code" data-state-code>51</span>
        </div>
      </aside>
    </header>

    <section class="map-board" aria-label="Interactive map area">
      <div class="map-frame">
{svg}
      </div>
      <div class="tooltip" role="status" hidden></div>
    </section>

    <p class="credit">
      Map outline derived from
      <a href="https://commons.wikimedia.org/wiki/File:Blank_US_Map_(states_only).svg">Wikimedia Commons</a>
      CC0 state SVG.
    </p>
  </main>

  <script>
    const map = document.querySelector("#usa-map");
    const tooltip = document.querySelector(".tooltip");
    const stateName = document.querySelector("[data-state-name]");
    const stateCode = document.querySelector("[data-state-code]");
    const interactiveStates = Array.from(map.querySelectorAll("g.state > path:not(.dc), circle.dc"));
    let activeState = null;

    function getStateCode(element) {{
      return Array.from(element.classList)
        .find((name) => /^[a-z]{{2}}$/.test(name))
        ?.toUpperCase() || "DC";
    }}

    function clamp(value, min, max) {{
      return Math.max(min, Math.min(max, value));
    }}

    function moveTooltip(x, y) {{
      const margin = 12;
      tooltip.style.left = `${{clamp(x, margin, window.innerWidth - margin)}}px`;
      tooltip.style.top = `${{clamp(y, margin + 40, window.innerHeight - margin)}}px`;
    }}

    function showState(element, position) {{
      const name = element.dataset.stateName;
      const code = element.dataset.stateCode;

      if (activeState && activeState !== element) {{
        activeState.classList.remove("is-active");
      }}

      activeState = element;
      element.classList.add("is-active");
      stateName.textContent = name;
      stateCode.textContent = code;
      tooltip.innerHTML = `${{name}}<small>${{code}}</small>`;
      tooltip.hidden = false;

      if (position) {{
        moveTooltip(position.x, position.y);
      }} else {{
        const box = element.getBoundingClientRect();
        moveTooltip(box.left + box.width / 2, box.top);
      }}
    }}

    function resetState(element) {{
      element.classList.remove("is-active");
      if (activeState === element) {{
        activeState = null;
        stateName.textContent = "United States";
        stateCode.textContent = "51";
        tooltip.hidden = true;
      }}
    }}

    interactiveStates.forEach((element) => {{
      const title = element.querySelector("title");
      const name = title?.textContent.trim() || "District of Columbia";
      const code = getStateCode(element);

      element.dataset.stateName = name;
      element.dataset.stateCode = code;
      element.setAttribute("tabindex", "0");
      element.setAttribute("role", "button");
      element.setAttribute("aria-label", `${{name}} (${{code}})`);
      title?.remove();

      element.addEventListener("pointerenter", (event) => showState(element, event));
      element.addEventListener("pointermove", (event) => moveTooltip(event.clientX, event.clientY));
      element.addEventListener("pointerleave", () => resetState(element));
      element.addEventListener("focus", () => showState(element));
      element.addEventListener("blur", () => resetState(element));
    }});
  </script>
</body>
</html>
"""


def main() -> None:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    svg = prepare_svg(SVG_SOURCE.read_text(encoding="utf-8"))
    OUTPUT.write_text(build_html(svg), encoding="utf-8")


if __name__ == "__main__":
    main()
