# visualizer.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from audio_processor import PyAudioProcessor
import tkinter as tk
from tkinter import filedialog

class AudioVisualizer:
    def __init__(self, audio_file, num_bars=20):
        self.processor = PyAudioProcessor(audio_file)
        self.num_bars = num_bars
        self.fig, self.ax = plt.subplots()
        self.bars = None
        
        # Initial setup
        self.x = np.arange(0, num_bars)
        self.initial_data = self.processor.get_frequency_bands(num_bars)
        self.max_height = max(self.initial_data) * 1.5

    def init_animation(self):
        self.bars = self.ax.bar(self.x, self.initial_data)
        self.ax.set_ylim(0, self.max_height)
        self.ax.set_title('Audio Visualizer')
        self.ax.set_xlabel('Frequency Bands')
        self.ax.set_ylabel('Amplitude')
        return self.bars

    def update(self, frame):
        # Get new frequency data
        data = self.processor.get_frequency_bands(self.num_bars)
        
        # Update bar heights
        for bar, height in zip(self.bars, data):
            bar.set_height(height)
        return self.bars

    def start(self):
        ani = animation.FuncAnimation(
            self.fig,
            self.update,
            init_func=self.init_animation,
            interval=50,  # Update every 50ms
            blit=True
        )
        plt.show()

def select_audio_file():
    """Open a file dialog to select an audio file."""
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select an Audio File",
        filetypes=[("Audio Files", "*.wav *.mp3 *.flac *.aac *.ogg")]
    )
    return file_path

def main():
    # Allow the user to select an audio file via file dialog
    audio_file = select_audio_file()
    if not audio_file:
        print("No file selected. Exiting...")
        return

    visualizer = AudioVisualizer(audio_file)
    visualizer.start()

if __name__ == "__main__":
    main()