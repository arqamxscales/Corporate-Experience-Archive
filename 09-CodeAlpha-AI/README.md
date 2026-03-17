# CodeAlpha_MusicGeneration

An AI-powered music generator with a Tkinter GUI. It trains an LSTM model on MIDI note sequences and generates new MIDI files.

## Features
- Create sample MIDI files or import your own
- Extract notes and train an LSTM model
- Generate AI music and export to MIDI
- Save and load trained models

## Installation
1. Create and activate a virtual environment.
2. Install dependencies:
   - `music21==9.1.0`
   - `tensorflow==2.15.0`
   - `numpy==1.24.3`
   - `keras==2.15.0`

## Usage
1. Run the GUI:
   - `python music_gui_enhanced.py`
2. Create or import MIDI files.
3. Extract notes and train the model.
4. Generate music and check the output folder.

## Output
Generated files are saved in the output folder (e.g., `output/ai_generated_music.mid`).

## Screenshots

![Music Generator Interface 1](docs/screenshot1.png)
*AI Music Generator interface*

![Music Generator Interface 2](docs/screenshot2.png)
*Training and generation controls*

![Music Generator Interface 3](docs/screenshot3.png)
*Model training progress*

![Music Generator Interface 4](docs/screenshot4.png)
*MIDI file selection and processing*

![Music Generator Interface 5](docs/screenshot5.png)
*Generated music output and playback*

## Technologies Used
- Python
- Tkinter
- TensorFlow / Keras
- music21
- NumPy
