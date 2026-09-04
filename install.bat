@echo off
setlocal enabledelayedexpansion

cd /d "%~dp0"
echo ==^> Project directory: %cd%

REM Check/install Python

where python >nul 2>&1
if errorlevel 1 (
    echo ==^> Python not found.
    where winget >nul 2>&1
    if errorlevel 1 (
        echo ERROR: Python is not installed, and winget is not available to install it automatically.
        echo Download it manually from https://www.python.org/downloads/
        echo IMPORTANT: during installation, check "Add python.exe to PATH".
        pause
        exit /b 1
    ) else (
        echo ==^> Installing Python via winget...
        winget install -e --id Python.Python.3.12 --scope user --silent --accept-package-agreements --accept-source-agreements
        echo.
        echo ==^> Python was installed. Windows needs a new terminal session to pick up
        echo     the updated PATH, so please close this window and run install.bat again.
        pause
        exit /b 0
    )
)

REM Check/install ffmpeg

where ffmpeg >nul 2>&1
if errorlevel 1 (
    echo ==^> ffmpeg not found.
    where winget >nul 2>&1
    if errorlevel 1 (
        echo WARNING: ffmpeg is not installed, and winget is not available to install it automatically.
        echo The app needs ffmpeg to convert audio to MP3.
        echo Download it from https://ffmpeg.org/download.html
        echo and add its "bin" folder to your PATH environment variable.
        echo.
        echo Continuing anyway - you can install ffmpeg later.
        echo.
    ) else (
        echo ==^> Installing ffmpeg via winget...
        winget install -e --id Gyan.FFmpeg --scope user --silent --accept-package-agreements --accept-source-agreements
        echo.
        echo ==^> ffmpeg was installed, but this terminal session won't see it until you
        echo     open a new one. MP3 conversion won't work until you restart the terminal
        echo     ^(or your PC^) before running the app.
        echo.
    )
)

REM Create the virtual environment if it doesn't exist

if not exist venv (
    echo ==^> Creating virtual environment...
    python -m venv venv
) else (
    echo ==^> Virtual environment already exists, reusing it.
)

REM Install Python dependencies inside the venv (skip if already installed)

venv\Scripts\python.exe -c "import yt_dlp, PyInstaller" 2>nul
if errorlevel 1 (
    echo ==^> Installing Python dependencies...
    venv\Scripts\python.exe -m pip install --upgrade pip --quiet
    venv\Scripts\pip.exe install yt-dlp --quiet
    venv\Scripts\pip.exe install pyinstaller --quiet
) else (
    echo ==^> Python dependencies already installed, skipping.
)

REM Build the executable with PyInstaller

echo ==^> Building the executable (this may take a minute)...
venv\Scripts\pyinstaller.exe --onefile --windowed --noconfirm app_desktop.py > pyinstaller_log.txt 2>&1

if not exist "dist\app_desktop.exe" (
    echo ERROR: the executable was not created. Check pyinstaller_log.txt for details.
    pause
    exit /b 1
)

echo ==^> Executable created at: %cd%\dist\app_desktop.exe

REM Create a desktop shortcut

echo ==^> Creating desktop shortcut...
powershell -NoProfile -Command ^
    "$ws = New-Object -ComObject WScript.Shell;" ^
    "$shortcut = $ws.CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'YouTube to MP3.lnk'));" ^
    "$shortcut.TargetPath = '%cd%\dist\app_desktop.exe';" ^
    "$shortcut.WorkingDirectory = '%cd%\dist';" ^
    "$shortcut.Description = 'Download and convert YouTube videos to MP3';" ^
    "$shortcut.Save()"

echo.
echo ==================================================
echo  Installation complete.
echo  A "YouTube to MP3" shortcut was added to your Desktop.
echo  You can also run it directly from:
echo    %cd%\dist\app_desktop.exe
echo ==================================================
pause
