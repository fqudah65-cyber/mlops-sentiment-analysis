"""
Unit tests for Sentiment Analysis Model
Tests model functionality and prediction"""

import unittest
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.sentiment_model import SentimentAnalyzer

class TestSentimentAnalyzer(unittest.TestCase):
    """Test cases for SentimentAnalyzer class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.analyzer = SentimentAnalyzer()
    
    def test_model_initialization(self):
        """Test model initializes correctly"""
        self.assertIsNotNone(self.analyzer)
        self.assertTrue(self.analyzer.is_trained)
    
    def test_positive_sentiment(self):
        """Test positive sentiment detection"""
        result = self.analyzer.predict("This is amazing! I love it!")
        self.assertEqual(result['sentiment'], 'positive')
        self.assertGreater(result['confidence'], 0.4)
    
    def test_negative_sentiment(self):
        """Test negative sentiment detection"""
        result = self.analyzer.predict("This is terrible and awful!")
        self.assertEqual(result['sentiment'], 'negative')
        self.assertGreater(result['confidence'], 0.4)
    
    def test_neutral_sentiment(self):
        """Test neutral sentiment detection"""
        result = self.analyzer.predict("This is okay.")
        self.assertEqual(result['sentiment'], 'neutral')
    
    def test_prediction_output_structure(self):
        """Test prediction output has correct structure"""
        result = self.analyzer.predict("Test text")
        
        self.assertIn('text', result)
        self.assertIn('sentiment', result)
        self.assertIn('confidence', result)
        self.assertIn('scores', result)
        
        self.assertIn('negative', result['scores'])
        self.assertIn('positive', result['scores'])
        self.assertIn('neutral', result['scores'])
    
    def test_confidence_scores_sum_to_one(self):
        """Test confidence scores sum to approximately 1"""
        result = self.analyzer.predict("Test text")
        total = sum(result['scores'].values())
        self.assertAlmostEqual(total, 1.0, places=2)
    
    def test_batch_prediction(self):
        """Test batch prediction"""
        texts = ["Great product!", "Terrible experience.", "It's okay."]
        results = self.analyzer.predict_batch(texts)
        
        self.assertEqual(len(results), 3)
        self.assertEqual(results[0]['sentiment'], 'positive')
        self.assertEqual(results[1]['sentiment'], 'negative')
        self.assertEqual(results[2]['sentiment'], 'neutral')
    
    def test_empty_batch_raises_error(self):
        """Test empty batch raises error"""
        with self.assertRaises(ValueError):
            self.analyzer.predict_batch([])
    
    def test_invalid_input_type(self):
        """Test invalid input type raises error"""
        with self.assertRaises(ValueError):
            self.analyzer.predict(123)
    
    def test_empty_text_raises_error(self):
        """Test empty text raises error"""
        with self.assertRaises(ValueError):
            self.analyzer.predict("")
    
    def test_model_info(self):
        """Test model info retrieval"""
        info = self.analyzer.get_model_info()
        
        self.assertTrue(info['is_trained'])
        self.assertIn('model_type', info)
        self.assertIn('sentiment_classes', info)
        self.assertEqual(len(info['sentiment_classes']), 3)

if __name__ == '__main__':
    unittest.main()
