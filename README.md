# YouTube to MP3 - Desktop App

A simple desktop app built with Python and Tkinter that downloads a YouTube
video and converts it to MP3, using yt-dlp.

## Requirements

- Python 3.8+
- `tkinter` (on Debian/Ubuntu/Kali, install with `sudo apt install python3-tk`
  if it's not already present)
- `ffmpeg` installed on the system:
  - Windows: download from https://ffmpeg.org and add the `bin` folder to PATH
  - Linux (Debian/Ubuntu/Kali): `sudo apt install ffmpeg`
  - macOS: `brew install ffmpeg`

## Quick install (Linux)

Run the included script to install system dependencies, set up the virtual
environment, build the executable, and add it to your applications menu,
all in one go:

```bash
chmod +x install.sh
./install.sh
```

## Manual install

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python3 app_desktop.py
```

Downloaded MP3 files are saved to `~/MP3_Downloads`.

## Project structure

- `download_audio(url)`: does the actual work using yt-dlp. It knows nothing
  about the UI — it just downloads and converts.
- `App`: the class that builds the window and wires up the button. When
  "Convert to MP3" is clicked, it runs `download_audio` on a background
  thread so the window doesn't freeze while downloading.
- `if __name__ == "__main__":` at the bottom is what actually starts the
  window when you run the script.

## Building a standalone executable

To package the app so it can run without Python installed:

```bash
pip install pyinstaller
pyinstaller --onefile --windowed app_desktop.py
```

The executable will be at `dist/app_desktop`. Note that:

- `ffmpeg` is **not** bundled — it still needs to be installed separately on
  the machine running the app.
- The executable must be built **on the same OS** you want to run it on
  (a Linux build won't produce a Windows `.exe`, and vice versa).
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
