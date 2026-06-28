@echo off
title 3D Map Server Launcher
cd /d "%~dp0"

echo ==========================================
echo       TAMU 3D Map Auto Launcher
echo ==========================================
echo.
echo This window is the local server for the map.
echo Keep it open while using the project.
echo Close this window to stop the server.
echo.

where node >nul 2>nul
if errorlevel 1 (
  echo ERROR: Node.js was not found on this computer.
  echo Please install the LTS version from https://nodejs.org/
  echo Then double-click this file again.
  echo.
  pause
  exit /b 1
)

echo [1/2] Launching browser to http://127.0.0.1:8765/index.html ...
start "" cmd /c "timeout /t 2 /nobreak >nul & rundll32 url.dll,FileProtocolHandler http://127.0.0.1:8765/index.html"

echo.
echo [2/2] Starting local Node.js static server...
echo ------------------------------------------
node static_server.js

echo.
echo The server has stopped.
pause