import tkinter as tk
import pygame as sound
import time
import librosa
import numpy as np
from tkinterdnd2 import DND_FILES, TkinterDnD

LOAD_PER_LOOP = 2048
BANDS = 64
RAINBOW_COLORS = [
    "#ff0000", "#ff0000", "#ff1f00", "#ff1f00", "#ff3e00", "#ff5d00", "#ff7c00", "#ff9b00", "#ffba00", "#ffba00", "#ffd900", 
    "#fff800", "#eaff00", "#cbff00", "#cbff00", "#adff00", "#8eff00", "#8eff00", "#6fff00", "#51ff00", "#32ff00", 
    "#13ff00", "#00ff0b", "#00ff2a", "#00ff49", "#00ff49", "#00ff49", "#00ff68", "#00ff87", "#00ffa6", "#00ffc4", 
    "#00ffe3", "#00ffff", "#00e0ff", "#00c1ff", "#00a3ff", "#00a3ff", "#0084ff", "#0066ff", "#0066ff", "#0047ff", 
    "#0028ff", "#000aff", "#1400ff", "#1400ff", "#3300ff", "#5100ff", "#7000ff", "#7000ff", "#8f00ff", "#ad00ff", 
    "#cc00ff", "#cc00ff", "#eb00ff", "#ff00f4", "#ff00d5", "#ff00b7", "#ff0098", "#ff0079", "#ff0079", "#ff005b", 
    "#ff003c", "#ff001d", "#ff001d"
]

sound.mixer.init()

root = TkinterDnD.Tk()
root.title("See Music")
root.geometry("800x600")
root.configure(bg="#000000")

current_theme = "colorful"
def set_theme(theme):
    global current_theme
    current_theme = theme

canvas = tk.Canvas(root, bg="#000000", highlightthickness=0)

button_frame = tk.Frame(root)
button_frame.pack(side="bottom", fill="x")
toggle_black = tk.Button(
    button_frame, text="Black & White", 
    bg="#000000", fg="#FFFFFF", 
    command=lambda: set_theme("black")
)
toggle_colorful = tk.Button(
    button_frame, text="Colorful", 
    bg="#9B1E1E", fg="#58F45A", 
    highlightbackground="#1DA0E7", 
    command=lambda: set_theme("colorful")
)

label = tk.Label(
    root,
    text="Drop a file here", bg="#000000",
    fg="white", width=45,
    height=15, font=("TkDefaultFont", 24, "bold")
)
label.place(relx=0.5, rely=0.5, anchor="center")

def darken_hex(color, factor = 0.8):
    color = color.lstrip("#")

    r = int(color[0:2], 16)
    g = int(color[2:4], 16)
    b = int(color[4:6], 16)

    r = max(0, min(255, int(r * factor)))
    g = max(0, min(255, int(g * factor)))
    b = max(0, min(255, int(b * factor)))

    return f"#{r:02x}{g:02x}{b:02x}"

# ================= FFT =================
def runfft(frame):
    frame = frame * np.hanning(len(frame))
    fft = np.fft.rfft(frame)
    mag = np.abs(fft)

    band_size = len(mag) // BANDS
    bands = np.array([
        np.mean(mag[i*band_size:(i+1)*band_size])
        for i in range(BANDS)
    ])

    bands /= np.max(bands) + 1e-6
    bands[0:4] *= 0.7
    return bands

# ================= DRAW =================
def draw_lines(bands):
    canvas.delete("bars")

    w = canvas.winfo_width()
    h = canvas.winfo_height()

    padding = 40
    usable_w = w - padding*2
    spacing = usable_w / BANDS
    max_height = h * 0.6

    for i, val in enumerate(bands):
        x = padding + i*spacing
        bar_h = val * max_height + 2

        canvas.create_line(
            x, h/2 + bar_h,
            x, h/2 - bar_h,
            width=3,
            fill=RAINBOW_COLORS[i] if current_theme=="colorful" else "white",
            tags="bars"
        )

# ================= VISUAL LOOP =================
bg_count = 0
def update_visual():
    if not sound.mixer.music.get_busy():
        # canvas.delete("bars")
        return

    t = time.time() - start_time
    idx = int(t * sr)

    if idx + LOAD_PER_LOOP >= len(audio):
        return

    frame = audio[idx:idx+LOAD_PER_LOOP]
    bands = runfft(frame)
    draw_lines(bands)
    if current_theme == "colorful":
        global bg_count
        if bg_count >= len(RAINBOW_COLORS):
            bg_count = 0
        canvas.config(bg=darken_hex(RAINBOW_COLORS[bg_count], factor=0.2))
        button_frame.config(bg=darken_hex(RAINBOW_COLORS[bg_count], factor=0.2))
        bg_count += 1
    elif current_theme == "black":
        canvas.config(bg="black")
        button_frame.config(bg="black")

    root.after(16, update_visual)

# ================= PLAY =================
def play(path):
    global audio, sr, start_time
    audio, sr = librosa.load(path, sr=None, mono=True)
    audio = audio / np.max(np.abs(audio))
    label.place_forget()
    canvas.pack(fill="both", expand=True)
    toggle_black.pack(side="left", padx=10, pady=5)
    toggle_colorful.pack(side="left", padx=10, pady=5)
    stop_button.pack(side="right", padx=10, pady=5)

    sound.mixer.music.load(path)
    sound.mixer.music.play()

    start_time = time.time()
    update_visual()

def stop_music():
    sound.mixer.music.stop() # Stop the audio
    canvas.delete("bars") # Clear visualizer bars
    canvas.pack_forget() # Hide the visualizer canvas
    
    canvas.config(bg="#000000")
    button_frame.config(bg="#000000")
    
    # Bring back the original drop label
    label.config(text="Drop a file here")
    label.place(relx=0.5, rely=0.4, anchor="center")

# ================= DRAG DROP =================
def on_drop(event):
    label.config(text="Processing...")
    root.update_idletasks()
    path = event.data.strip("{}")
    play(path)

# label.drop_target_register(DND_FILES)
# label.dnd_bind("<<Drop>>", on_drop)

root.drop_target_register(DND_FILES)
root.dnd_bind("<<Drop>>", on_drop)

stop_button = tk.Button(
    button_frame, text="Stop Music", 
    bg="#FF3333", fg="#FFFFFF", 
    command=stop_music
)
root.mainloop()