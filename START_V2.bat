@echo off
setlocal

echo Starting FairMatch AI Version 2...
echo API: http://127.0.0.1:8000
echo Frontend: http://127.0.0.1:5500
echo.

cd /d "%~dp0"

if not exist ".venv\" (
    echo Virtual environment not found.
    echo Please set up the project first.
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\uvicorn.exe" (
    echo Uvicorn was not found in the virtual environment.
    echo Please run:
    echo .venv\Scripts\python.exe -m pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

if not exist "frontend\index.html" (
    echo Version 2 frontend was not found.
    echo Expected file: frontend\index.html
    echo.
    pause
    exit /b 1
)

echo Checking FastAPI...
set API_READY=0
.venv\Scripts\python.exe -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()" >nul 2>nul
if not errorlevel 1 (
    set API_READY=1
    echo API already running.
    goto api_ready
)

echo Starting FastAPI in a separate window...
start "FairMatch AI V2 API" cmd /k ".venv\Scripts\python.exe -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000"

echo Waiting for the API to start...
for /L %%i in (1,1,10) do (
    .venv\Scripts\python.exe -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2).read()" >nul 2>nul
    if not errorlevel 1 (
        set API_READY=1
        goto api_ready
    )
    timeout /t 1 >nul
)

:api_ready
if "%API_READY%"=="0" (
    echo.
    echo API did not respond yet.
    echo The frontend will still open, but it may show API Offline until FastAPI finishes starting.
    echo Check the API terminal window for errors.
    echo.
) else (
    echo API Connected.
)

echo Checking frontend server...
set FRONTEND_READY=0
.venv\Scripts\python.exe -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5500/index.html', timeout=2).read()" >nul 2>nul
if not errorlevel 1 (
    set FRONTEND_READY=1
    echo Frontend already running.
    goto frontend_ready
)

echo Starting frontend server in a separate window...
start "FairMatch AI V2 Frontend" cmd /k "cd /d frontend && ..\.venv\Scripts\python.exe -m http.server 5500 --bind 127.0.0.1"

echo Waiting for the frontend server to start...
for /L %%i in (1,1,10) do (
    .venv\Scripts\python.exe -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:5500/index.html', timeout=2).read()" >nul 2>nul
    if not errorlevel 1 (
        set FRONTEND_READY=1
        goto frontend_ready
    )
    timeout /t 1 >nul
)

:frontend_ready
if "%FRONTEND_READY%"=="0" (
    echo.
    echo Frontend server did not respond yet.
    echo Check the frontend terminal window for errors.
    echo.
) else (
    echo Frontend Connected.
)

echo Opening Version 2 frontend...
start "" "http://127.0.0.1:5500/index.html"

echo.
echo FairMatch AI Version 2 is starting.
echo Keep the API and frontend server windows open while using Version 2.
echo.
pause
