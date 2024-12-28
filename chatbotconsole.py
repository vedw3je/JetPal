import sqlite3
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz
import re
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the lightweight Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Initialize the sentiment analyzer
analyzer = SentimentIntensityAnalyzer()

# Load FAQs from SQLite database
def load_faqs_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faqs")
    faqs = cursor.fetchall()
    conn.close()
    return faqs

# Preprocess queries to normalize text (lowercase, remove extra spaces, etc.)
def preprocess_text(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)  # Remove special characters
    text = re.sub(r'\s+', ' ', text).strip()  # Remove extra spaces
    return text

# Function to find the best match using semantic similarity and fuzzy matching
def find_best_match(user_query, faqs, semantic_weight=0.7, fuzzy_weight=0.3):
    # Preprocess user query
    user_query = preprocess_text(user_query)

    # Separate questions and answers
    questions = [preprocess_text(faq[0]) for faq in faqs]
    answers = [faq[1] for faq in faqs]

    # Encode the user query and FAQ questions into embeddings
    query_embedding = model.encode(user_query, convert_to_tensor=True)
    faq_embeddings = model.encode(questions, convert_to_tensor=True)

    # Compute semantic similarity scores
    semantic_scores = util.cos_sim(query_embedding, faq_embeddings).cpu().numpy()[0]

    # Compute fuzzy matching scores
    fuzzy_scores = [fuzz.partial_ratio(user_query, question) for question in questions]

    # Combine both scores with weights
    combined_scores = [
        (semantic_weight * semantic_score + fuzzy_weight * (fuzzy_score / 100))
        for semantic_score, fuzzy_score in zip(semantic_scores, fuzzy_scores)
    ]

    # Find the best match
    best_match_idx = combined_scores.index(max(combined_scores))
    best_question = questions[best_match_idx]
    best_answer = answers[best_match_idx]
    best_score = combined_scores[best_match_idx]

    return best_question, best_answer, best_score

# Function for sentiment analysis on user query
def analyze_sentiment(user_query):
    sentiment = analyzer.polarity_scores(user_query)
    return sentiment['compound']  # Returns the compound score (-1 to 1)

# Load FAQs and run the chatbot
db_path = 'faqs.db'  # Path to your SQLite database
faqs = load_faqs_from_db(db_path)

print("Welcome to the FAQ Chatbot! Type 'exit' to quit.")
while True:
    user_query = input("You: ")
    if user_query.lower() == 'exit':
        print("Goodbye!")
        break

    # Analyze the sentiment of the user query
    sentiment_score = analyze_sentiment(user_query)

    # Find the best match and respond
    best_question, best_answer, best_score = find_best_match(user_query, faqs)

    # Set a confidence threshold for matching
    if best_score > 0.5:  # You can adjust this threshold based on testing
        # Adjust response based on sentiment score
        if sentiment_score < -0.2:  # Negative sentiment
            response = f"It seems you're upset. Let me help you better with this:\nAnswer: {best_answer}"
        elif sentiment_score > 0.2:  # Positive sentiment
            response = f"That's great!:\nAnswer: {best_answer}"
        else:  # Neutral sentiment
            response = f"Here's the answer to your query:\nAnswer: {best_answer}"

        print(f"FAQ Match: {best_question}")
        print(response)
        print(f"Confidence Score: {best_score:.2f}")
    else:
        print("Sorry, I couldn't find a relevant FAQ for your query.")
