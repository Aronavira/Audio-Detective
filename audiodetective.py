import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import librosa
import sounddevice as sd
import numpy as np
import matplotlib.pyplot as plt

class AudioForensicTool:
    def __init__(self, root):
        self.root = root
        self.root.title("Audio Forensic Tool")

        self.upload_button_1 = tk.Button(root, text="Upload First Audio", command=self.upload_audio_1)
        self.upload_button_1.pack()

        self.progress_1 = ttk.Progressbar(root, length=200)
        self.progress_1.pack()

        self.upload_button_2 = tk.Button(root, text="Upload Second Audio", command=self.upload_audio_2)
        self.upload_button_2.pack()

        self.progress_2 = ttk.Progressbar(root, length=200)
        self.progress_2.pack()

        self.play_button_1 = tk.Button(root, text="Play First Audio", command=self.play_audio_1)
        self.play_button_1.pack()

        self.play_button_2 = tk.Button(root, text="Play Second Audio", command=self.play_audio_2)
        self.play_button_2.pack()

        self.info_button_1 = tk.Button(root, text="Get Info for First Audio", command=self.get_info_1)
        self.info_button_1.pack()

        self.info_button_2 = tk.Button(root, text="Get Info for Second Audio", command=self.get_info_2)
        self.info_button_2.pack()

        self.compare_button = tk.Button(root, text="Compare Audios", command=self.compare_audios)
        self.compare_button.pack()

        self.plot_button_1 = tk.Button(root, text="Plot Waveform of First Audio", command=self.plot_waveform_1)
        self.plot_button_1.pack()

        self.plot_button_2 = tk.Button(root, text="Plot Waveform of Second Audio", command=self.plot_waveform_2)
        self.plot_button_2.pack()

        self.audio_paths = [None, None]
        self.audio_data = [None, None]
        self.sampling_rates = [None, None]

    def upload_audio_1(self):
        self.audio_paths[0] = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        self.load_audio(0, self.progress_1)

    def upload_audio_2(self):
        self.audio_paths[1] = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3")])
        self.load_audio(1, self.progress_2)

    def load_audio(self, index, progress_bar):
        if self.audio_paths[index]:
            self.audio_data[index], self.sampling_rates[index] = librosa.load(self.audio_paths[index], sr=None)
            progress_bar["value"] = 100  # Simulate completion
            self.root.update_idletasks()

    def play_audio_1(self):
        if self.audio_data[0] is not None:
            sd.play(self.audio_data[0], self.sampling_rates[0])

    def play_audio_2(self):
        if self.audio_data[1] is not None:
            sd.play(self.audio_data[1], self.sampling_rates[1])

    def get_info_1(self):
        if self.audio_data[0] is not None:
            duration = librosa.get_duration(y=self.audio_data[0], sr=self.sampling_rates[0])
            sample_rate = self.sampling_rates[0]
            num_samples = len(self.audio_data[0])
            messagebox.showinfo("Audio Info", f"First Audio\nDuration: {duration:.2f} seconds\nSample Rate: {sample_rate} Hz\nNumber of Samples: {num_samples}")

    def get_info_2(self):
        if self.audio_data[1] is not None:
            duration = librosa.get_duration(y=self.audio_data[1], sr=self.sampling_rates[1])
            sample_rate = self.sampling_rates[1]
            num_samples = len(self.audio_data[1])
            messagebox.showinfo("Audio Info", f"Second Audio\nDuration: {duration:.2f} seconds\nSample Rate: {sample_rate} Hz\nNumber of Samples: {num_samples}")

    def compare_audios(self):
        print("Comparing Audios...")  # Debug statement
        if self.audio_data[0] is not None and self.audio_data[1] is not None:
            print(f"Audio 1 Shape: {self.audio_data[0].shape}, Audio 2 Shape: {self.audio_data[1].shape}")  # Debug statement

            # Normalize audio data
            normalized_audio_1 = self.audio_data[0] / np.max(np.abs(self.audio_data[0])) if np.max(np.abs(self.audio_data[0])) > 0 else self.audio_data[0]
            normalized_audio_2 = self.audio_data[1] / np.max(np.abs(self.audio_data[1])) if np.max(np.abs(self.audio_data[1])) > 0 else self.audio_data[1]

            length_1 = len(normalized_audio_1)
            length_2 = len(normalized_audio_2)
            min_length = min(length_1, length_2)

            # Trim audio to the same length
            trimmed_audio_1 = normalized_audio_1[:min_length]
            trimmed_audio_2 = normalized_audio_2[:min_length]

            # Calculate Mean Squared Error (MSE)
            mse = np.mean((trimmed_audio_1 - trimmed_audio_2) ** 2)
            print(f"MSE: {mse:.5f}")  # Debug statement

            # Determine if tampered based on MSE threshold
            result = "Tampered" if mse > 0.01 else "Not Tampered"

            # Optionally, calculate Signal-to-Noise Ratio (SNR)
            noise = trimmed_audio_1 - trimmed_audio_2
            snr = 10 * np.log10(np.sum(trimmed_audio_1 ** 2) / np.sum(noise ** 2)) if np.sum(noise ** 2) != 0 else float('inf')

            messagebox.showinfo("Comparison Result", f"Audio Comparison Result: {result}\nMSE: {mse:.5f}\nSNR: {snr:.2f} dB")
        else:
            messagebox.showwarning("Comparison Error", "Please ensure both audio files are uploaded.")

    def plot_waveform_1(self):
        if self.audio_data[0] is not None:
            plt.figure(figsize=(10, 4))
            plt.plot(self.audio_data[0])
            plt.title("Waveform of First Audio")
            plt.xlabel("Samples")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.show()

    def plot_waveform_2(self):
        if self.audio_data[1] is not None:
            plt.figure(figsize=(10, 4))
            plt.plot(self.audio_data[1])
            plt.title("Waveform of Second Audio")
            plt.xlabel("Samples")
            plt.ylabel("Amplitude")
            plt.grid()
            plt.show()

if __name__ == "__main__":
    root = tk.Tk()
    app = AudioForensicTool(root)
    root.mainloop()
