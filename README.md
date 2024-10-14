# Audio-Detective
# Audio Forensic Tool

A simple GUI application built with Python using Tkinter for audio forensic analysis. This tool allows users to upload two audio files, play them, obtain information about them, and compare them for potential tampering.

## Features

- Upload two audio files (WAV or MP3).
- Play the uploaded audio files.
- Get detailed information about each audio file, including duration, sample rate, and number of samples.
- Compare the two audio files to determine if one has been tampered with.
- Plot waveforms of the audio files for visual analysis.

## Requirements

- Python 3.x
- Libraries:
  - `tkinter`
  - `librosa`
  - `sounddevice`
  - `numpy`
  - `matplotlib`

You can install the required libraries using pip:

```bash
pip install librosa sounddevice numpy matplotlib
