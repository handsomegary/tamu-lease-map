const http = require("http");
const fs = require("fs");
const path = require("path");
const root = __dirname;
const port = 8765;
const types = new Map([
  [".html", "text/html; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".json", "application/json; charset=utf-8"],
  [".geojson", "application/geo+json; charset=utf-8"]
]);

http.createServer((req, res) => {
  const url = new URL(req.url, "http://127.0.0.1");
  const cleanPath = path.normalize(decodeURIComponent(url.pathname)).replace(/^([/\\])+/, "");
  const filePath = path.resolve(root, cleanPath || "tamu_leaflet_rentals.html");

  if (!filePath.startsWith(root)) {
    res.writeHead(403);
    res.end("Forbidden");
    return;
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404);
      res.end("Not found");
      return;
    }

    res.writeHead(200, { "Content-Type": types.get(path.extname(filePath)) || "application/octet-stream" });
    res.end(data);
  });
}).listen(port, "127.0.0.1");