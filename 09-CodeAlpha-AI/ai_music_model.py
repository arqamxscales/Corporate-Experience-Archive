import numpy as np
from music21 import converter, instrument, note, chord, stream
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import pickle
import os

class MusicAI:
    def __init__(self):
        self.notes = []
        self.model = None
        self.network_input = []
        self.network_output = []
        self.n_vocab = 0
        self.note_to_int = {}
        self.int_to_note = {}
        
    def extract_notes_from_midi(self, midi_folder='output'):
        """Extract notes from MIDI files"""
        self.notes = []
        
        # If no MIDI files exist, create sample data
        if not os.path.exists(midi_folder) or len(os.listdir(midi_folder)) == 0:
            print("No MIDI files found. Creating sample data...")
            self.create_sample_training_data()
            return self.notes
            
        for file in os.listdir(midi_folder):
            if file.endswith('.mid') or file.endswith('.midi'):
                try:
                    midi = converter.parse(os.path.join(midi_folder, file))
                    notes_to_parse = midi.flatten().notes
                    
                    for element in notes_to_parse:
                        if isinstance(element, note.Note):
                            self.notes.append(str(element.pitch))
                        elif isinstance(element, chord.Chord):
                            self.notes.append('.'.join(str(n) for n in element.normalOrder))
                except Exception as e:
                    print(f"Error parsing {file}: {e}")
        
        # If still no notes, create sample data
        if len(self.notes) == 0:
            self.create_sample_training_data()
            
        return self.notes
    
    def create_sample_training_data(self):
        """Create sample musical sequences for training"""
        # Create a simple melodic pattern (C major scale patterns)
        patterns = [
            ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5'],  # Ascending scale
            ['C5', 'B4', 'A4', 'G4', 'F4', 'E4', 'D4', 'C4'],  # Descending scale
            ['C4', 'E4', 'G4', 'C5'],  # C major chord arpeggio
            ['G4', 'B4', 'D5', 'G5'],  # G major chord arpeggio
            ['F4', 'A4', 'C5', 'F5'],  # F major chord arpeggio
            ['A4', 'C5', 'E5', 'A5'],  # A minor chord arpeggio
        ]
        
        # Repeat patterns to create more training data
        for _ in range(20):
            for pattern in patterns:
                self.notes.extend(pattern)
        
        return self.notes
    
    def prepare_sequences(self, sequence_length=100, midi_folder='output'):
        """Prepare sequences for training"""
        if len(self.notes) == 0:
            self.extract_notes_from_midi(midi_folder)

        if len(self.notes) <= sequence_length:
            raise ValueError(
                f"Not enough notes ({len(self.notes)}) for sequence length {sequence_length}. "
                "Reduce sequence length or add more MIDI data."
            )

        # Get unique notes
        pitchnames = sorted(set(self.notes))
        self.n_vocab = len(pitchnames)
        
        # Create mappings
        self.note_to_int = {note: number for number, note in enumerate(pitchnames)}
        self.int_to_note = {number: note for number, note in enumerate(pitchnames)}
        
        # Create input sequences
        self.network_input = []
        self.network_output = []
        
        for i in range(0, len(self.notes) - sequence_length, 1):
            sequence_in = self.notes[i:i + sequence_length]
            sequence_out = self.notes[i + sequence_length]
            self.network_input.append([self.note_to_int[char] for char in sequence_in])
            self.network_output.append(self.note_to_int[sequence_out])
        
        n_patterns = len(self.network_input)
        
        # Reshape and normalize input
        self.network_input = np.reshape(self.network_input, (n_patterns, sequence_length, 1))
        self.network_input = self.network_input / float(self.n_vocab)
        
        # One-hot encode output
        if len(self.network_output) == 0:
            raise ValueError(
                "No training patterns were created. Reduce sequence length or add more MIDI data."
            )
        self.network_output = keras.utils.to_categorical(self.network_output)
        
        return self.network_input, self.network_output
    
    def create_model(self, sequence_length=100):
        """Create LSTM neural network"""
        if self.n_vocab == 0:
            raise ValueError("No vocabulary found. Prepare sequences before creating the model.")
        self.model = keras.Sequential([
            layers.LSTM(256, input_shape=(sequence_length, 1), return_sequences=True),
            layers.Dropout(0.3),
            layers.LSTM(256, return_sequences=True),
            layers.Dropout(0.3),
            layers.LSTM(256),
            layers.Dropout(0.3),
            layers.Dense(256),
            layers.Dropout(0.3),
            layers.Dense(self.n_vocab, activation='softmax')
        ])
        
        self.model.compile(loss='categorical_crossentropy', optimizer='adam')
        return self.model
    
    def train(self, epochs=10, batch_size=64):
        """Train the model"""
        if self.model is None:
            raise Exception("Model not created. Call create_model() first.")
        if len(self.network_input) == 0 or len(self.network_output) == 0:
            raise ValueError("Training data is empty. Prepare sequences before training.")
        
        self.model.fit(
            self.network_input, 
            self.network_output, 
            epochs=epochs, 
            batch_size=batch_size,
            verbose=1
        )
        
        return self.model
    
    def generate_notes(self, length=100, sequence_length=100):
        """Generate new notes using the trained model"""
        if len(self.network_input) == 0:
            raise ValueError("No input patterns found. Train or load a model first.")
        # Pick a random sequence from the input as a starting point
        start = np.random.randint(0, len(self.network_input) - 1)
        pattern = self.network_input[start].flatten().tolist()
        
        prediction_output = []
        
        # Generate notes
        for note_index in range(length):
            prediction_input = np.reshape(pattern, (1, len(pattern), 1))
            prediction_input = prediction_input / float(self.n_vocab)
            
            prediction = self.model.predict(prediction_input, verbose=0)
            index = np.argmax(prediction)
            result = self.int_to_note[index]
            prediction_output.append(result)
            
            pattern.append(index / float(self.n_vocab))
            pattern = pattern[1:]
        
        return prediction_output
    
    def create_midi_from_notes(self, prediction_output, filename='output/ai_generated.mid'):
        """Convert predicted notes to MIDI file"""
        offset = 0
        output_notes = []
        
        for pattern in prediction_output:
            # Pattern is a chord
            if '.' in pattern:
                notes_in_chord = pattern.split('.')
                notes = []
                for current_note in notes_in_chord:
                    new_note = note.Note(int(current_note))
                    new_note.storedInstrument = instrument.Piano()
                    notes.append(new_note)
                new_chord = chord.Chord(notes)
                new_chord.offset = offset
                output_notes.append(new_chord)
            # Pattern is a note
            else:
                new_note = note.Note(pattern)
                new_note.offset = offset
                new_note.storedInstrument = instrument.Piano()
                output_notes.append(new_note)
            
            # Increase offset each iteration so notes don't stack
            offset += 0.5
        
        midi_stream = stream.Stream(output_notes)
        
        # Ensure output directory exists
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        midi_stream.write('midi', fp=filename)
        return filename
    
    def save_model(self, model_path='models/music_model.h5', 
                   notes_path='models/notes.pkl'):
        """Save trained model and notes"""
        os.makedirs('models', exist_ok=True)
        self.model.save(model_path)
        with open(notes_path, 'wb') as f:
            pickle.dump({
                'notes': self.notes,
                'note_to_int': self.note_to_int,
                'int_to_note': self.int_to_note,
                'n_vocab': self.n_vocab
            }, f)
    
    def load_model(self, model_path='models/music_model.h5',
                   notes_path='models/notes.pkl'):
        """Load trained model and notes"""
        self.model = keras.models.load_model(model_path)
        with open(notes_path, 'rb') as f:
            data = pickle.load(f)
            self.notes = data['notes']
            self.note_to_int = data['note_to_int']
            self.int_to_note = data['int_to_note']
            self.n_vocab = data['n_vocab']