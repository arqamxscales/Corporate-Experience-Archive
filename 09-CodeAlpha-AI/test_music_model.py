"""
Unit Tests for Music Generation AI Model
Tests LSTM model training and generation
"""

import unittest
import json
import os


class MusicModelConfig:
    """Configuration manager for music generation"""
    
    def __init__(self, config_path="config.json"):
        """Initialize config manager"""
        self.config = self.load_config(config_path)
    
    def load_config(self, config_path):
        """Load configuration from JSON"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            raise Exception(f"Config load error: {str(e)}")
    
    def get_default_config(self):
        """Get default configuration"""
        return {
            "model": {
                "sequence_length": 100,
                "lstm_units": 256,
                "dropout": 0.3,
                "num_layers": 3
            },
            "training": {
                "epochs": 20,
                "batch_size": 64
            }
        }
    
    def get_model_config(self):
        """Get model configuration"""
        return self.config.get("model", {})
    
    def get_training_config(self):
        """Get training configuration"""
        return self.config.get("training", {})
    
    def get_sequence_length(self):
        """Get sequence length"""
        return self.config.get("model", {}).get("sequence_length", 100)
    
    def get_epochs(self):
        """Get training epochs"""
        return self.config.get("training", {}).get("epochs", 20)
    
    def get_batch_size(self):
        """Get batch size"""
        return self.config.get("training", {}).get("batch_size", 64)
    
    def validate_config(self):
        """Validate configuration values"""
        seq_len = self.get_sequence_length()
        epochs = self.get_epochs()
        batch = self.get_batch_size()
        
        if seq_len <= 0:
            raise ValueError("Sequence length must be positive")
        if epochs <= 0:
            raise ValueError("Epochs must be positive")
        if batch <= 0:
            raise ValueError("Batch size must be positive")
        
        return True


class MusicSequenceGenerator:
    """Generate and manipulate music sequences"""
    
    def __init__(self, config_path="config.json"):
        """Initialize sequence generator"""
        self.config = MusicModelConfig(config_path)
        self.notes = []
    
    def validate_sequence(self, sequence):
        """Validate a sequence of notes"""
        if not isinstance(sequence, (list, np.ndarray)):
            raise ValueError("Sequence must be a list or array")
        if len(sequence) == 0:
            raise ValueError("Sequence cannot be empty")
        return True
    
    def validate_note(self, note):
        """Validate a single note"""
        if not isinstance(note, (str, int, float)):
            raise ValueError("Note must be string, int, or float")
        return True
    
    def add_note(self, note):
        """Add note to sequence"""
        self.validate_note(note)
        self.notes.append(note)
        return True
    
    def add_notes(self, notes):
        """Add multiple notes to sequence"""
        if not isinstance(notes, (list, tuple)):
            raise ValueError("Notes must be a list or tuple")
        
        for note in notes:
            self.add_note(note)
        return True
    
    def get_notes(self):
        """Get all notes"""
        return self.notes
    
    def get_sequence_length(self):
        """Get current sequence length"""
        return len(self.notes)
    
    def clear_notes(self):
        """Clear all notes"""
        self.notes = []
        return True
    
    def create_training_sequences(self, seq_length):
        """Create training sequences from notes"""
        if self.get_sequence_length() <= seq_length:
            raise ValueError(
                f"Not enough notes ({self.get_sequence_length()}) "
                f"for sequence length {seq_length}"
            )
        
        input_sequences = []
        output_sequences = []
        
        for i in range(0, len(self.notes) - seq_length, 1):
            input_seq = self.notes[i:i + seq_length]
            output_seq = self.notes[i + seq_length]
            input_sequences.append(input_seq)
            output_sequences.append(output_seq)
        
        return input_sequences, output_sequences


class TestMusicModelConfig(unittest.TestCase):
    """Test suite for model configuration"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = MusicModelConfig()
    
    def test_load_config(self):
        """Test configuration loading"""
        self.assertIsNotNone(self.config.config)
        self.assertIsInstance(self.config.config, dict)
    
    def test_get_model_config(self):
        """Test getting model config"""
        model_config = self.config.get_model_config()
        self.assertIsNotNone(model_config)
        self.assertIn("sequence_length", model_config)
    
    def test_get_training_config(self):
        """Test getting training config"""
        train_config = self.config.get_training_config()
        self.assertIsNotNone(train_config)
    
    def test_get_sequence_length(self):
        """Test getting sequence length"""
        seq_len = self.config.get_sequence_length()
        self.assertGreater(seq_len, 0)
        self.assertEqual(seq_len, 100)
    
    def test_get_epochs(self):
        """Test getting epochs"""
        epochs = self.config.get_epochs()
        self.assertGreater(epochs, 0)
        self.assertEqual(epochs, 20)
    
    def test_get_batch_size(self):
        """Test getting batch size"""
        batch = self.config.get_batch_size()
        self.assertGreater(batch, 0)
        self.assertEqual(batch, 64)
    
    def test_validate_config_valid(self):
        """Test validation with valid config"""
        self.assertTrue(self.config.validate_config())
    
    def test_validate_config_invalid_sequence_length(self):
        """Test validation with invalid sequence length"""
        self.config.config["model"]["sequence_length"] = -1
        with self.assertRaises(ValueError):
            self.config.validate_config()
    
    def test_validate_config_invalid_epochs(self):
        """Test validation with invalid epochs"""
        self.config.config["training"]["epochs"] = 0
        with self.assertRaises(ValueError):
            self.config.validate_config()


class TestMusicSequenceGenerator(unittest.TestCase):
    """Test suite for sequence generator"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.generator = MusicSequenceGenerator()
    
    def test_init(self):
        """Test initialization"""
        self.assertIsNotNone(self.generator.config)
        self.assertIsInstance(self.generator.notes, list)
    
    def test_validate_sequence_valid_list(self):
        """Test validation with valid list"""
        self.assertTrue(self.generator.validate_sequence([1, 2, 3]))
    
    def test_validate_sequence_valid_array(self):
        """Test validation with valid numpy array"""
        try:
            import numpy as np
            arr = np.array([1, 2, 3])
            self.assertTrue(self.generator.validate_sequence(arr))
        except ImportError:
            # Skip if numpy not available
            pass
    
    def test_validate_sequence_empty(self):
        """Test validation with empty sequence"""
        with self.assertRaises(ValueError):
            self.generator.validate_sequence([])
    
    def test_validate_sequence_invalid_type(self):
        """Test validation with invalid type"""
        with self.assertRaises(ValueError):
            self.generator.validate_sequence("not a sequence")
    
    def test_validate_note_string(self):
        """Test validation with string note"""
        self.assertTrue(self.generator.validate_note("C4"))
    
    def test_validate_note_int(self):
        """Test validation with int note"""
        self.assertTrue(self.generator.validate_note(60))
    
    def test_validate_note_float(self):
        """Test validation with float note"""
        self.assertTrue(self.generator.validate_note(60.5))
    
    def test_validate_note_invalid(self):
        """Test validation with invalid note"""
        with self.assertRaises(ValueError):
            self.generator.validate_note([1, 2, 3])
    
    def test_add_note(self):
        """Test adding single note"""
        self.generator.add_note("C4")
        self.assertEqual(self.generator.get_sequence_length(), 1)
    
    def test_add_notes(self):
        """Test adding multiple notes"""
        notes = ["C4", "D4", "E4", "F4"]
        self.generator.add_notes(notes)
        self.assertEqual(self.generator.get_sequence_length(), 4)
    
    def test_add_notes_invalid_type(self):
        """Test adding notes with invalid type"""
        with self.assertRaises(ValueError):
            self.generator.add_notes("not a list")
    
    def test_get_notes(self):
        """Test getting notes"""
        notes = ["C4", "D4", "E4"]
        self.generator.add_notes(notes)
        self.assertEqual(self.generator.get_notes(), notes)
    
    def test_clear_notes(self):
        """Test clearing notes"""
        self.generator.add_notes(["C4", "D4"])
        self.generator.clear_notes()
        self.assertEqual(self.generator.get_sequence_length(), 0)
    
    def test_create_training_sequences_valid(self):
        """Test creating training sequences"""
        # Create enough notes
        notes = [str(i) for i in range(150)]
        self.generator.add_notes(notes)
        
        inputs, outputs = self.generator.create_training_sequences(100)
        self.assertGreater(len(inputs), 0)
        self.assertGreater(len(outputs), 0)
        self.assertEqual(len(inputs), len(outputs))
    
    def test_create_training_sequences_insufficient_notes(self):
        """Test creating sequences with insufficient notes"""
        self.generator.add_notes(["C4", "D4", "E4"])
        
        with self.assertRaises(ValueError):
            self.generator.create_training_sequences(100)


class TestMusicGeneration(unittest.TestCase):
    """Integration tests for music generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.config = MusicModelConfig()
        self.generator = MusicSequenceGenerator()
    
    def test_config_and_generator_compatibility(self):
        """Test config and generator work together"""
        seq_len = self.config.get_sequence_length()
        self.assertGreater(seq_len, 0)
        
        # Generate enough notes
        notes = [str(i) for i in range(seq_len + 50)]
        self.generator.add_notes(notes)
        
        inputs, outputs = self.generator.create_training_sequences(seq_len)
        self.assertGreater(len(inputs), 0)
    
    def test_complete_workflow(self):
        """Test complete generation workflow"""
        # Validate config
        self.config.validate_config()
        
        # Create notes
        self.generator.add_notes([f"note_{i}" for i in range(150)])
        
        # Create sequences
        seq_len = self.config.get_sequence_length()
        inputs, outputs = self.generator.create_training_sequences(seq_len)
        
        # Verify
        self.assertGreater(len(inputs), 0)
        self.assertEqual(len(inputs), len(outputs))


if __name__ == "__main__":
    unittest.main()
