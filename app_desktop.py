import os
import threading
import tkinter as tk
from tkinter import messagebox

import yt_dlp

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "MP3_Downloads")
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

COLOR_BG = "#6b3a3a"
COLOR_CARD = "#171a21"
COLOR_ACCENT = "#ff3b3b"
COLOR_ACCENT_HOVER = "#ff6b6b"
COLOR_TEXT = "#f2f2f2"
COLOR_MUTED = "#9aa0ab"
COLOR_SUCCESS = "#7fe2a0"
COLOR_ERROR = "#ff8080"

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 280


def download_audio(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(DOWNLOADS_FOLDER, "%(title)s.%(ext)s"),
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
        }],
        "quiet": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])



class App:

    def __init__(self, window):
        self.window = window
        self.window.title("YouTube to MP3")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)

        self.background = tk.Canvas(
            window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=COLOR_BG, highlightthickness=0
        )
        self.background.pack(fill="both", expand=True)

        self.card = tk.Frame(window, bg=COLOR_CARD, padx=30, pady=15)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=230)

        tk.Label(
            self.card, text="YouTube to MP3", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(pady=(0, 2))

        tk.Label(
            self.card, text="Paste a link and get the MP3", bg=COLOR_CARD, fg=COLOR_MUTED,
            font=("Segoe UI", 9)
        ).pack(pady=(0, 15))

        self.url_field = tk.Entry(
            self.card, width=40, bg="#0f1218", fg=COLOR_TEXT, insertbackground=COLOR_TEXT,
            relief="flat", highlightthickness=1, highlightbackground="#2b2f3a",
            highlightcolor=COLOR_ACCENT, font=("Segoe UI", 10)
        )
        self.url_field.pack(ipady=6, fill="x")

        self.convert_button = tk.Button(
            self.card, text="Convert to MP3", command=self.on_convert_click,
            bg=COLOR_ACCENT, fg="white", activebackground=COLOR_ACCENT_HOVER,
            activeforeground="white", relief="flat", font=("Segoe UI", 10, "bold"),
            cursor="hand2", bd=0
        )
        self.convert_button.pack(fill="x", ipady=8, pady=(15, 10))
        self.convert_button.bind("<Enter>", lambda e: self.convert_button.config(bg=COLOR_ACCENT_HOVER))
        self.convert_button.bind("<Leave>", lambda e: self.convert_button.config(bg=COLOR_ACCENT))

        self.status_label = tk.Label(
            self.card, text="", bg=COLOR_CARD, fg=COLOR_MUTED, font=("Segoe UI", 9), wraplength=340
        )
        self.status_label.pack()

    def on_convert_click(self):
        url = self.url_field.get().strip()

        if not url:
            messagebox.showwarning("Missing link", "Paste a YouTube link first.")
            return

        self.convert_button.config(state="disabled", bg=COLOR_ACCENT)
        self.status_label.config(text="Downloading and converting...", fg=COLOR_MUTED)

        thread = threading.Thread(target=self.run_download, args=(url,))
        thread.start()

    def run_download(self, url):
        try:
            download_audio(url)
            self.window.after(0, self.on_success)
        except Exception as e:
            self.window.after(0, lambda: self.on_error(str(e)))

    def on_success(self):
        self.status_label.config(text=f"Done! Saved to {DOWNLOADS_FOLDER}", fg=COLOR_SUCCESS)
        self.convert_button.config(state="normal")
        self.url_field.delete(0, tk.END)

    def on_error(self, error_message):
        self.status_label.config(text="An error occurred.", fg=COLOR_ERROR)
        self.convert_button.config(state="normal")
        messagebox.showerror("Error", error_message)


if __name__ == "__main__":
    window = tk.Tk()
    app = App(window)
    window.mainloop()
