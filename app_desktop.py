import os
import threading
import tkinter as tk
from tkinter import messagebox

import yt_dlp

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "MP3_Downloads")
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOADS_FOLDER, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
        "noplaylist": True,
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


class App:
    def __init__(self, window):
        self.window = window
        self.window.title("YouTube to MP3")
        self.window.geometry("420x180")
        self.window.resizable(False, False)

        tk.Label(window, text="YouTube link:").pack(pady=(15, 0))

        self.url_field = tk.Entry(window, width=50)
        self.url_field.pack(pady=5)

        self.convert_button = tk.Button(
            window, text="Convert to MP3", command=self.on_convert_click
        )
        self.convert_button.pack(pady=10)

        self.status_label = tk.Label(window, text="", fg="gray")
        self.status_label.pack(pady=5)

    def on_convert_click(self):
        url = self.url_field.get().strip()

        if not url:
            messagebox.showwarning("Missing link", "Paste a YouTube link first.")
            return

        self.convert_button.config(state="disabled")
        self.status_label.config(text="Downloading and converting...", fg="orange")

        thread = threading.Thread(target=self.run_download, args=(url,))
        thread.start()

    def run_download(self, url):
        try:
            download_audio(url)
            self.window.after(0, self.on_success)
        except Exception as e:
            self.window.after(0, lambda: self.on_error(str(e)))

    def on_success(self):
        self.status_label.config(text=f"Done! Saved to {DOWNLOADS_FOLDER}", fg="green")
        self.convert_button.config(state="normal")
        self.url_field.delete(0, tk.END)

    def on_error(self, error_message):
        self.status_label.config(text="An error occurred.", fg="red")
        self.convert_button.config(state="normal")
        messagebox.showerror("Error", error_message)


if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()
