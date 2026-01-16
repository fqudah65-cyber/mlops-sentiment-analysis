class SentimentAnalyzer:
    """
    Simple sentiment analyzer used for testing
    """

    def __init__(self):
        self.model_name = "DummySentimentAnalyzer"
        self.version = "1.0.0"

    def analyze(self, text: str) -> dict:
        if not text or not isinstance(text, str):
            raise ValueError("Invalid text")

        text_lower = text.lower()

        if any(word in text_lower for word in ["good", "great", "excellent", "happy"]):
            sentiment = "positive"
        elif any(word in text_lower for word in ["bad", "terrible", "sad", "angry"]):
            sentiment = "negative"
        else:
            sentiment = "neutral"

        return {
            "text": text,
            "sentiment": sentiment
        }

    def batch_analyze(self, texts: list) -> list:
        if not isinstance(texts, list):
            raise ValueError("Input must be a list")

        if len(texts) > 100:
            raise ValueError("Too many items")

        results = []
        for text in texts:
            results.append(self.analyze(text))

        return results

    def get_model_info(self) -> dict:
        return {
            "model_name": self.model_name,
            "version": self.version,
            "type": "rule-based"
        }
# Alias used by API routes
    def predict_batch(self, texts: list) -> list:
        return self.batch_analyze(texts)

