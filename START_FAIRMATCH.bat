@echo off
setlocal

cd /d "%~dp0"

echo ========================================
echo FairMatch AI Dashboard Launcher
echo ========================================
echo.

if not exist ".venv\Scripts\activate.bat" (
    echo Error: The local virtual environment was not found.
    echo.
    echo Please create and install it first:
    echo   python -m venv .venv
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

if not exist ".venv\Scripts\streamlit.exe" (
    echo Error: Streamlit is not installed in the local virtual environment.
    echo.
    echo Please install project dependencies first:
    echo   .venv\Scripts\activate
    echo   pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

call ".venv\Scripts\activate.bat"

echo Starting FairMatch AI dashboard...
echo Browser will open at http://localhost:8501
echo.

start "" "http://localhost:8501"
streamlit run app.py --server.port 8501

endlocal
