"""
Unit Tests for FAQ Chatbot
Tests NLP matching and response generation
"""

import unittest
import json
import os


class ChatbotEngine:
    """Reusable chatbot engine with NLP"""
    
    def __init__(self, config_path="config.json", faq_path="faqs.json"):
        """Initialize chatbot with configuration and FAQ data"""
        self.config = self.load_config(config_path)
        self.faqs = self.load_faqs(faq_path)
        self.questions = list(self.faqs.keys()) if self.faqs else []
        self.similarity_threshold = self.config.get(
            "chatbot", {}
        ).get("similarity_threshold", 0.3)
    
    def load_config(self, config_path):
        """Load configuration from JSON"""
        try:
            if os.path.exists(config_path):
                with open(config_path, 'r') as f:
                    return json.load(f)
            else:
                return {"chatbot": {"similarity_threshold": 0.3}}
        except Exception as e:
            raise Exception(f"Config load error: {str(e)}")
    
    def load_faqs(self, faq_path):
        """Load FAQ database from JSON"""
        try:
            if os.path.exists(faq_path):
                with open(faq_path, 'r') as f:
                    return json.load(f)
            else:
                return {}
        except Exception as e:
            raise Exception(f"FAQ load error: {str(e)}")
    
    def validate_input(self, user_input):
        """Validate user input"""
        if not user_input:
            raise ValueError("Input cannot be empty")
        if len(user_input) > 1000:
            raise ValueError("Input exceeds maximum length (1000 chars)")
        return True
    
    def preprocess_text(self, text):
        """Preprocess text for NLP"""
        return text.lower().strip()
    
    def find_best_match(self, user_input):
        """Find best matching FAQ using TF-IDF and cosine similarity"""
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.metrics.pairwise import cosine_similarity
        
        self.validate_input(user_input)
        
        if not self.questions:
            return None, 0.0
        
        try:
            # Prepare data
            all_text = self.questions + [user_input]
            
            # TF-IDF vectorization
            vectorizer = TfidfVectorizer()
            tfidf_matrix = vectorizer.fit_transform(all_text)
            
            # Calculate similarity
            scores = cosine_similarity(tfidf_matrix[-1], tfidf_matrix[:-1])
            match_index = scores.argmax()
            highest_score = float(scores[0][match_index])
            
            if highest_score < self.similarity_threshold:
                return None, highest_score
            
            return self.questions[match_index], highest_score
        
        except Exception as e:
            raise Exception(f"Matching error: {str(e)}")
    
    def get_response(self, user_input):
        """Get chatbot response for user input"""
        matched_question, score = self.find_best_match(user_input)
        
        if matched_question is None:
            return self.config.get(
                "chatbot", {}
            ).get(
                "default_response",
                "I'm sorry, I don't understand that."
            ), score
        
        return f"✅ {self.faqs[matched_question]}", score
    
    def add_faq(self, question, answer):
        """Add new FAQ pair"""
        if not question or not answer:
            raise ValueError("Question and answer cannot be empty")
        
        self.faqs[question] = answer
        self.questions = list(self.faqs.keys())
        return True
    
    def remove_faq(self, question):
        """Remove FAQ pair"""
        if question not in self.faqs:
            raise ValueError("Question not found in FAQ database")
        
        del self.faqs[question]
        self.questions = list(self.faqs.keys())
        return True
    
    def get_faq_count(self):
        """Get total FAQ count"""
        return len(self.faqs)


class TestChatbotEngine(unittest.TestCase):
    """Test suite for Chatbot Engine"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Create temporary config
        self.test_config = {
            "chatbot": {
                "similarity_threshold": 0.3,
                "default_response": "I don't understand"
            }
        }
        
        # Create temporary FAQs
        self.test_faqs = {
            "What is CodeAlpha?": "CodeAlpha is an AI internship program",
            "How do I start?": "Visit www.codealpha.tech to get started",
            "What technologies are taught?": "Python, ML, AI, and more"
        }
        
        self.engine = ChatbotEngine()
    
    def test_load_config(self):
        """Test configuration loading"""
        self.assertIsNotNone(self.engine.config)
        self.assertIn("chatbot", self.engine.config)
    
    def test_load_faqs(self):
        """Test FAQ loading"""
        self.assertIsNotNone(self.engine.faqs)
        self.assertIsInstance(self.engine.faqs, dict)
    
    def test_validate_input_empty(self):
        """Test validation with empty input"""
        with self.assertRaises(ValueError):
            self.engine.validate_input("")
    
    def test_validate_input_too_long(self):
        """Test validation with input exceeding limit"""
        long_input = "a" * 1001
        with self.assertRaises(ValueError):
            self.engine.validate_input(long_input)
    
    def test_validate_input_valid(self):
        """Test validation with valid input"""
        self.assertTrue(self.engine.validate_input("What is CodeAlpha?"))
    
    def test_preprocess_text(self):
        """Test text preprocessing"""
        result = self.engine.preprocess_text("  HELLO WORLD  ")
        self.assertEqual(result, "hello world")
    
    def test_get_faq_count(self):
        """Test FAQ count"""
        count = self.engine.get_faq_count()
        self.assertGreaterEqual(count, 0)
    
    def test_add_faq(self):
        """Test adding new FAQ"""
        initial_count = self.engine.get_faq_count()
        self.engine.add_faq("Test Question?", "Test Answer")
        new_count = self.engine.get_faq_count()
        self.assertEqual(new_count, initial_count + 1)
    
    def test_add_faq_invalid(self):
        """Test adding invalid FAQ"""
        with self.assertRaises(ValueError):
            self.engine.add_faq("", "Answer")
    
    def test_remove_faq(self):
        """Test removing FAQ"""
        if self.engine.get_faq_count() > 0:
            question = list(self.engine.faqs.keys())[0]
            initial_count = self.engine.get_faq_count()
            self.engine.remove_faq(question)
            new_count = self.engine.get_faq_count()
            self.assertEqual(new_count, initial_count - 1)
    
    def test_remove_faq_not_found(self):
        """Test removing non-existent FAQ"""
        with self.assertRaises(ValueError):
            self.engine.remove_faq("Non-existent question?")
    
    def test_similarity_threshold(self):
        """Test similarity threshold setting"""
        self.assertGreater(self.engine.similarity_threshold, 0)
        self.assertLess(self.engine.similarity_threshold, 1)


class TestChatbotMatching(unittest.TestCase):
    """Test matching and response generation"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.engine = ChatbotEngine()
    
    def test_find_best_match_with_faqs(self):
        """Test matching when FAQs exist"""
        if self.engine.get_faq_count() > 0:
            question, score = self.engine.find_best_match(
                list(self.engine.faqs.keys())[0]
            )
            self.assertIsNotNone(question)
            self.assertGreater(score, 0)
    
    def test_get_response_valid_input(self):
        """Test getting response with valid input"""
        response, score = self.engine.get_response("What is CodeAlpha?")
        self.assertIsNotNone(response)
        self.assertIsInstance(score, float)
    
    def test_get_response_invalid_input(self):
        """Test getting response with invalid input"""
        with self.assertRaises(ValueError):
            self.engine.get_response("")


if __name__ == "__main__":
    unittest.main()
