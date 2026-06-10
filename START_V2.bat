@echo off
setlocal

echo Starting FairMatch AI Version 2...
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

echo Starting FastAPI in a separate window...
start "FairMatch AI V2 API" cmd /k ".venv\Scripts\activate.bat && uvicorn api.main:app --reload"

echo Waiting for the API to start...
set API_READY=0
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

echo Opening Version 2 frontend...
start "" "%CD%\frontend\index.html"

echo.
echo FairMatch AI Version 2 is starting.
echo Keep the API window open while using the frontend.
echo.
pause
