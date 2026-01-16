class SentimentAnalyzer:
    def analyze(self, text):
        if not text:
            return {"sentiment": "neutral", "score": 0.0}
        return {"sentiment": "positive", "score": 0.9}
