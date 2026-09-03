# YouTube to MP3 - Desktop App for Windows 10/11 & Linux (Debian/Ubuntu)

A simple desktop app built with Python and Tkinter that downloads a YouTube
video and converts it to MP3, using yt-dlp.

## Requirements

Installed automatically running the installer (**no action needed**):

  - `Python 3.8+`
  - `tkinter`
  - `ffmpeg`

  Virtual environment libraries:

  - `yt-dlp`
  - `pyinstaller`

## Quick install (Linux)

Run `install.sh` to install system dependencies, set up the virtual
environment, build the executable, and add it to your applications menu,
all in one go:

```bash
chmod +x install.sh
./install.sh
```

It will try to install Python and ffmpeg automatically using
**apt install** if they're missing.

## Quick install (Windows)

Run `install.bat` from a terminal to install system dependencies, set up the virtual
environment, build the executable and add a shortcut to your Desktop, all in one go:

```bat
./install.bat
```

It will try to install Python and ffmpeg automatically using
**winget** if they're missing.

## Manual install

## Install

`ffmpeg` is **not** bundled - it still needs to be installed separately on
  the machine running the app:

- Linux: `sudo apt install ffmpeg`
- Windows: `winget install ffmpeg`

Then, go to the folder and run:

```bash
python3 -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install yt-dlp
```

## Run

```bash
python3 app_desktop.py
```

Downloaded MP3 files are saved to `~/MP3_Downloads`.

## Project structure

- `app_desktop.py`: builds the application's window and downloads the mp3 from the given url to ~/MP3_Downloads
- `install.bat`: Windows installer.
- `install.sh`: Linux installer.

## Building a standalone executable

To package the app so it can run without Python installed:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed app_desktop.py
```

The executable will be at `dist/app_desktop` (or `dist\app_desktop.exe` on
Windows). Note that:

- For best compatibility across Linux distributions, build on the oldest
  Debian/Ubuntu version you want to support, since newer `glibc` versions
  are backward compatible but not forward compatible.

### Desktop launcher (Linux)

To make the executable appear in your applications menu, create
`~/.local/share/applications/yt2mp3.desktop`:

```ini
[Desktop Entry]
Type=Application
Name=YouTube to MP3
Comment=Download and convert YouTube videos to MP3
Exec=/path/to/dist/app_desktop
Icon=audio-x-generic
Terminal=false
Categories=AudioVideo;Audio;
```

Update the `Exec=` path to match where you keep the built executable.
