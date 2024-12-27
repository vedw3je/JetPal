import sqlite3
from flask import Flask, request, jsonify
from sentence_transformers import SentenceTransformer, util
from rapidfuzz import fuzz

# Initialize Flask app
app = Flask(__name__)

# Load the lightweight Sentence Transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')


# Load FAQs from SQLite database
def load_faqs_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT question, answer FROM faqs")
    faqs = cursor.fetchall()
    conn.close()
    return faqs


# Function to find the best match using both semantic similarity and fuzzy matching
def find_best_match(user_query, faqs, semantic_weight=0.7, fuzzy_weight=0.3):
    questions = [faq[0] for faq in faqs]
    answers = [faq[1] for faq in faqs]

    query_embedding = model.encode(user_query, convert_to_tensor=True)
    faq_embeddings = model.encode(questions, convert_to_tensor=True)

    semantic_scores = util.cos_sim(query_embedding, faq_embeddings).cpu().numpy()[0]
    fuzzy_scores = [fuzz.partial_ratio(user_query, question) for question in questions]

    combined_scores = [
        (semantic_weight * semantic_score + fuzzy_weight * (fuzzy_score / 100))
        for semantic_score, fuzzy_score in zip(semantic_scores, fuzzy_scores)
    ]

    best_match_idx = combined_scores.index(max(combined_scores))
    best_answer = answers[best_match_idx]
    best_score = combined_scores[best_match_idx]

    return best_answer, best_score


# Load FAQs from the database
db_path = 'faqs.db'
faqs = load_faqs_from_db(db_path)


# Define the route for querying the FAQ
@app.route('/ask', methods=['POST'])
def ask():
    user_query = request.json.get('query')  # Get the query from the POST request

    if not user_query:
        return jsonify({"error": "No query provided"}), 400

    # Find the best match
    best_answer, best_score = find_best_match(user_query, faqs)

    # Set a confidence threshold for the match
    if best_score > 0.5:
        response = {
            "answer": best_answer
        }
    else:
        response = {"answer": "Sorry, I couldn't find a relevant FAQ for your query."}

    return jsonify(response)


# Run the app
if __name__ == '__main__':
    app.run(debug=True)
