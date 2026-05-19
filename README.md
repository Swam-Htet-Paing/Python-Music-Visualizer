# See Music - Simple Music Visualizer

A lightweight Python application that visualizes audio frequencies in real-time using Tkinter and Pygame. Drop an audio file, watch the frequencies dance, and toggle between colorful and monochrome themes.

## How It Works

The application bridges the gap between digital audio and computer graphics[cite: 2]:
1. **Audio Ingestion:** Loads an audio track using `librosa` and mirrors playback via `pygame.mixer`[cite: 2].
2. **Frequency Analysis:** Uses a Fast Fourier Transform (FFT) algorithm via `numpy` to extract frequency data (bass, mids, treble) from microscopic slices of live playback[cite: 2].
3. **Dynamic Rendering:** Maps the calculated loudness of 64 distinct frequency bands directly onto the height of canvas vector elements, refreshing roughly 60 times a second[cite: 2].

## Key Functions

* `play(path)`: Loads the target audio track into memory for analysis, initializes UI visibility states, starts background playback tracking, and fires up the core loop[cite: 2].
* `runfft(frame)`: Applies a Hanning window to a small sound slice, executes a Fast Fourier Transform, and compresses thousands of frequency outputs into 64 uniform bands[cite: 2].
* `draw_lines(bands)`: Calculates dynamic layout coordinates relative to current window dimensions and clears/redraws lines reflecting band magnitudes[cite: 2].
* `update_visual()`: Acts as the clockwork rendering engine; identifies the current millisecond marker, extracts the corresponding audio frame, coordinates calculation and redraw pipelines, and schedules the next frame cycle in 16ms intervals[cite: 2].

## Prerequisites & Installation

Ensure you have Python installed, then install the external dependencies[cite: 2]:

```bash
pip install -r requirements.txt
