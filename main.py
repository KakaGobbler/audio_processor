# visualizer.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from audio_processor import PyAudioProcessor

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

def main():
    # Example usage
    visualizer = AudioVisualizer("path/to/your/audio.wav")
    visualizer.start()

if __name__ == "__main__":
    main()