from transformers import pipeline
import re

# Load once when the application starts
sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)


def analyze_text(text):

    text = text.strip()

    if not text:
        return {
            "error": "Text cannot be empty."
        }

    # Sentiment
    sentiment_result = sentiment_pipeline(text[:512])[0]

    label = sentiment_result["label"]
    confidence = round(sentiment_result["score"] * 100, 2)

    if label == "POSITIVE":
        sentiment = "Positive"
    else:
        sentiment = "Negative"

    # Basic sentence analysis
    sentences = [
        s.strip()
        for s in re.split(r"[.!?]+", text)
        if s.strip()
    ]

    words = re.findall(r"\b[\w']+\b", text)

    word_count = len(words)
    sentence_count = len(sentences)

    avg_sentence_length = (
        round(word_count / sentence_count, 1)
        if sentence_count
        else 0
    )

    # Communication score
    score = 100

    if word_count < 10:
        score -= 20

    if avg_sentence_length > 30:
        score -= 10

    score = max(0, min(100, score))

    # Simple keyword extraction
    stop_words = {
        "the", "is", "a", "an", "and", "or", "to",
        "of", "in", "on", "for", "with", "this",
        "that", "it", "i", "you", "we", "are",
        "was", "be", "as", "at", "by", "from"
    }

    keywords = []

    for word in words:
        cleaned = word.lower()

        if len(cleaned) > 3 and cleaned not in stop_words:
            if cleaned not in keywords:
                keywords.append(cleaned)

    keywords = keywords[:8]

    return {
        "sentiment": sentiment,
        "confidence": confidence,
        "word_count": word_count,
        "sentence_count": sentence_count,
        "average_sentence_length": avg_sentence_length,
        "communication_score": score,
        "keywords": keywords
    }