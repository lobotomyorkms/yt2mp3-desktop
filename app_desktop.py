import os
import threading
import tkinter as tk
from tkinter import messagebox

import yt_dlp

DOWNLOADS_FOLDER = os.path.join(os.path.expanduser("~"), "MP3_Downloads")
os.makedirs(DOWNLOADS_FOLDER, exist_ok=True)

GRADIENT_TOP = "#6b3a3a"
GRADIENT_BOTTOM = "#411414"
COLOR_CARD = "#171a21"
COLOR_ACCENT = "#ff3b3b"
COLOR_ACCENT_HOVER = "#ff6b6b"
COLOR_TEXT = "#f2f2f2"
COLOR_MUTED = "#9aa0ab"
COLOR_SUCCESS = "#7fe2a0"
COLOR_ERROR = "#ff8080"

WINDOW_WIDTH = 460
WINDOW_HEIGHT = 340
CARD_WIDTH = 380
CARD_RADIUS = 22


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


def hex_to_rgb(color):
    color = color.lstrip("#")
    return tuple(int(color[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


def interpolate_color(color_a, color_b, t):
    a = hex_to_rgb(color_a)
    b = hex_to_rgb(color_b)
    mixed = tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))
    return rgb_to_hex(mixed)


def draw_vertical_gradient(canvas, width, height, color_top, color_bottom):
    for y in range(height):
        t = y / height
        color = interpolate_color(color_top, color_bottom, t)
        canvas.create_line(0, y, width, y, fill=color)


def draw_rounded_rect(canvas, x1, y1, x2, y2, radius, **kwargs):
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, smooth=True, **kwargs)


class App:
    def __init__(self, window):
        self.window = window
        self.window.title("YouTube to MP3")
        self.window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.window.resizable(False, False)

        self.background = tk.Canvas(
            window, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, highlightthickness=0
        )
        self.background.pack(fill="both", expand=True)
        draw_vertical_gradient(self.background, WINDOW_WIDTH, WINDOW_HEIGHT, GRADIENT_TOP, GRADIENT_BOTTOM)

        self.card = tk.Frame(window, bg=COLOR_CARD, padx=30, pady=25)
        self.card.place(relx=0.5, rely=0.5, anchor="center", width=CARD_WIDTH)

        header = tk.Frame(self.card, bg=COLOR_CARD)
        header.pack(fill="x")

        tk.Label(
            header, text="YouTube to MP3", bg=COLOR_CARD, fg=COLOR_TEXT,
            font=("Segoe UI", 16, "bold")
        ).pack(anchor="w")

        tk.Frame(self.card, bg=COLOR_ACCENT, height=2, width=48).pack(anchor="w", pady=(6, 10))

        tk.Label(
            self.card, text="Paste a link and get the MP3", bg=COLOR_CARD, fg=COLOR_MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(0, 18))

        self.url_field = tk.Entry(
            self.card, width=40, bg="#0f1218", fg=COLOR_TEXT, insertbackground=COLOR_TEXT,
            relief="flat", highlightthickness=1, highlightbackground="#2b2f3a",
            highlightcolor=COLOR_ACCENT, font=("Segoe UI", 10)
        )
        self.url_field.pack(ipady=8, fill="x")

        self.convert_button = tk.Button(
            self.card, text="Convert to MP3", command=self.on_convert_click,
            bg=COLOR_ACCENT, fg="white", activebackground=COLOR_ACCENT_HOVER,
            activeforeground="white", relief="flat", font=("Segoe UI", 10, "bold"),
            cursor="hand2", bd=0
        )
        self.convert_button.pack(fill="x", ipady=9, pady=(16, 10))
        self.convert_button.bind("<Enter>", self.on_button_hover)
        self.convert_button.bind("<Leave>", self.on_button_leave)

        self.status_label = tk.Label(
            self.card, text="", bg=COLOR_CARD, fg=COLOR_MUTED, font=("Segoe UI", 9), wraplength=320
        )
        self.status_label.pack()

        self.window.update_idletasks()
        self.draw_card_background()

    def draw_card_background(self):
        card_width = self.card.winfo_width()
        card_height = self.card.winfo_height()
        x1 = (WINDOW_WIDTH - card_width) / 2
        y1 = (WINDOW_HEIGHT - card_height) / 2
        x2 = x1 + card_width
        y2 = y1 + card_height
        draw_rounded_rect(
            self.background, x1, y1, x2, y2, CARD_RADIUS, fill=COLOR_CARD, outline=""
        )
        self.card.lift()

    def on_button_hover(self, event):
        if self.convert_button["state"] != "disabled":
            self.convert_button.config(bg=COLOR_ACCENT_HOVER)

    def on_button_leave(self, event):
        if self.convert_button["state"] != "disabled":
            self.convert_button.config(bg=COLOR_ACCENT)

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