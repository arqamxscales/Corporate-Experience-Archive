"""
Unit Tests for Language Translation Tool
Tests core translation functionality
"""

import unittest
import json
import os
from io import StringIO
import sys


class TranslationEngine:
    """Reusable translation engine"""
    
    def __init__(self, config_path="config.json"):
        """Initialize translation engine with config"""
        self.config = self.load_config(config_path)
        self.lang_map = self.config.get("languages", {})
    
    def load_config(self, config_path):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                # Default config
                return {
                    "languages": {
                        "Spanish": "es",
                        "French": "fr",
                        "German": "de",
                        "Japanese": "ja"
                    }
                }
        except Exception as e:
            raise Exception(f"Config load error: {str(e)}")
    
    def get_languages(self):
        """Get available languages"""
        return list(self.lang_map.keys())
    
    def is_valid_language(self, language):
        """Check if language is supported"""
        return language in self.lang_map
    
    def get_language_code(self, language):
        """Get language code for translation"""
        return self.lang_map.get(language)
    
    def validate_text(self, text):
        """Validate input text"""
        if not text:
            raise ValueError("Text cannot be empty")
        if len(text) > 5000:
            raise ValueError("Text exceeds maximum length (5000 chars)")
        return True
    
    def validate_translation_input(self, text, language):
        """Validate translation input"""
        self.validate_text(text)
        if not self.is_valid_language(language):
            raise ValueError(f"Unsupported language: {language}")
        return True


class TestTranslationEngine(unittest.TestCase):
    """Test suite for Translation Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = TranslationEngine()
    
    def test_load_config(self):
        """Test configuration loading"""
        self.assertIsNotNone(self.engine.config)
        self.assertIn("languages", self.engine.config)
    
    def test_get_languages(self):
        """Test getting language list"""
        languages = self.engine.get_languages()
        self.assertIsInstance(languages, list)
        self.assertGreater(len(languages), 0)
    
    def test_is_valid_language(self):
        """Test language validation"""
        self.assertTrue(self.engine.is_valid_language("Spanish"))
        self.assertTrue(self.engine.is_valid_language("French"))
        self.assertFalse(self.engine.is_valid_language("InvalidLanguage"))
    
    def test_get_language_code(self):
        """Test getting language code"""
        self.assertEqual(self.engine.get_language_code("Spanish"), "es")
        self.assertEqual(self.engine.get_language_code("French"), "fr")
        self.assertIsNone(self.engine.get_language_code("InvalidLanguage"))
    
    def test_validate_text_empty(self):
        """Test validation with empty text"""
        with self.assertRaises(ValueError):
            self.engine.validate_text("")
    
    def test_validate_text_too_long(self):
        """Test validation with text exceeding limit"""
        long_text = "a" * 5001
        with self.assertRaises(ValueError):
            self.engine.validate_text(long_text)
    
    def test_validate_text_valid(self):
        """Test validation with valid text"""
        self.assertTrue(self.engine.validate_text("Hello world"))
        self.assertTrue(self.engine.validate_text("a" * 5000))
    
    def test_validate_translation_input_valid(self):
        """Test translation input validation - valid"""
        self.assertTrue(
            self.engine.validate_translation_input("Hello", "Spanish")
        )
    
    def test_validate_translation_input_invalid_language(self):
        """Test translation input validation - invalid language"""
        with self.assertRaises(ValueError):
            self.engine.validate_translation_input("Hello", "InvalidLang")
    
    def test_validate_translation_input_empty_text(self):
        """Test translation input validation - empty text"""
        with self.assertRaises(ValueError):
            self.engine.validate_translation_input("", "Spanish")
    
    def test_config_has_ui_settings(self):
        """Test that config has UI settings"""
        self.assertIn("ui", self.engine.config)
        self.assertIn("colors", self.engine.config["ui"])


class TestTranslationIntegration(unittest.TestCase):
    """Integration tests for translation tool"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = TranslationEngine()
    
    def test_language_code_mapping_complete(self):
        """Test that all languages have codes"""
        for language in self.engine.get_languages():
            code = self.engine.get_language_code(language)
            self.assertIsNotNone(code)
            self.assertIsInstance(code, str)
    
    def test_multiple_validations(self):
        """Test multiple validations in sequence"""
        text = "This is a test message"
        for language in self.engine.get_languages():
            self.assertTrue(
                self.engine.validate_translation_input(text, language)
            )


if __name__ == "__main__":
    unittest.main()
