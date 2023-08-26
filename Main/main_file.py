import customtkinter as ct
import tkinter as tk
import numpy as np
import pyaudio
import threading

# Constants
CHUNK = 1024  # Number of audio frames per buffer
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100  # Samples per second

class AudioAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Analyzer")

        self.canvas = ct.CTkCanvas(self.root, width=800, height=300, bg="white")
        self.canvas.pack()

        self.Label = ct.CTkLabel(master=root, text="Hello, I am your personal AI speech therapist", font=("Ariel", 20))
        self.Label.pack(pady=20)

        self.start_button = ct.CTkButton(self.root, text="1. Start Session", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = ct.CTkButton(self.root, text="Stop Recording", command=self.stop_recording)
        self.stop_button.pack()

        self.p = pyaudio.PyAudio()
        self.stream = None

        self.running = False
        self.thread = None

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_recording(self):
        self.stream = self.p.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK
        )

        self.running = True
        self.thread = threading.Thread(target=self.update)
        self.thread.start()

        self.start_button.configure(state=tk.DISABLED)
        self.stop_button.configure(state=tk.NORMAL)

    def stop_recording(self):
        self.running = False
        self.thread.join()
        self.stream.stop_stream()
        self.stream.close()

        self.start_button.configure(state=tk.NORMAL)
        self.stop_button.configure(state=tk.DISABLED)

    def update(self):
        while self.running:
            data = np.frombuffer(self.stream.read(CHUNK), dtype=np.int16)
            frequencies = np.fft.fft(data)
            magnitude = np.abs(frequencies)
            normalized_magnitude = magnitude / np.max(magnitude)

            self.draw_spectrum(normalized_magnitude)


    def draw_spectrum(self, spectrum_data):
        self.canvas.delete("all")
        num_bars = len(spectrum_data)
        bar_width = 800 / num_bars
        x = 0

        for value in spectrum_data:
            bar_height = value * 300
            self.canvas.create_rectangle(x, 300, x + bar_width, 300 - bar_height, fill="blue")
            x += bar_width

        self.root.after(100, self.draw_spectrum, spectrum_data)  # Continuously update the visualization


    def on_closing(self):
        self.stop_recording()
        self.root.destroy()

if __name__ == "__main__":
    root = ct.CTk()
    app = AudioAnalyzerApp(root)
    root.mainloop()


