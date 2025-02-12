# chatbot/app.py
#
# A simple Flask chatbot service that:
# 1. Loads a local JSON dataset (distilled_data.json) from ../data/
# 2. Accepts a POST request at /chat with JSON body { "user_query": "..." }
# 3. Parses the query to handle a few example questions about the dataset:
#    - "Who has the highest GPA?"
#    - "List all majors."
#    - "Which students want to study in <location>?"
# 4. Returns a JSON response with the "reply" field containing a basic answer.
#
# Usage Example:
#   POST /chat
#   {
#     "user_query": "Who has the highest GPA?"
#   }
#
# Note: This is a minimal illustration. For more complex queries or robust NLP,
# consider using a transformer-based QA model, RAG, or keyword extraction.

import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Adjust this path to match your local folder structure
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'distilled_data.json')

def load_distilled_data():
    """
    Load the distilled dataset from the local JSON file.
    Returns a list of dictionaries, each representing a student's record.
    """
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Load dataset once at startup
DISTILLED_DATA = load_distilled_data()

@app.route('/chat', methods=['POST'])
def chat():
    """
    Receives a user query in JSON format, e.g.:
      {
        "user_query": "Who has the highest GPA?"
      }
    Returns a simple rule-based response derived from the local dataset.
    """
    user_query = request.json.get('user_query', '').strip().lower()

    # Basic fallback reply if we can't parse the query
    answer = "I'm sorry, I didn't understand your question."

    # 1) Who has the highest GPA?
    if "highest gpa" in user_query:
        top_student = max(DISTILLED_DATA, key=lambda s: s.get('GPA', 0.0))
        answer = (f"The highest GPA is {top_student['GPA']}, from student_id "
                  f"{top_student['student_id']} studying {top_student['major']} at "
                  f"{top_student['undergrad_university']}.")
    
    # 2) List all majors in the dataset
    elif "list all majors" in user_query or ("what majors" in user_query and "have" in user_query):
        majors = set([record.get('major', '') for record in DISTILLED_DATA])
        majors_list = ", ".join(sorted(m for m in majors if m))
        answer = f"The majors in our dataset include: {majors_list}."

    # 3) Which students want to study in <location>?
    elif "which students want to study in" in user_query:
        # Naively extract location from the query
        # e.g., user_query: "Which students want to study in California?"
        words = user_query.split()
        # Find the last token if the user says something like "in California?"
        # We'll remove punctuation
        location_candidate = words[-1].replace("?", "")
        # Filter dataset by location
        matched_students = [
            record for record in DISTILLED_DATA
            if record.get('location_preference', '').lower() == location_candidate.lower()
        ]
        if matched_students:
            ids = [str(s['student_id']) for s in matched_students]
            answer = (f"Students wanting to study in {location_candidate} are student_id(s): " +
                      ", ".join(ids) + ".")
        else:
            answer = (f"No students found with a location preference of {location_candidate}.")
    
    # You can add more elif clauses for other queries:
    #  e.g. "lowest GPA", "majors for student_id=3", "show me all Education majors", etc.

    return jsonify({"reply": answer}), 200

if __name__ == '__main__':
    # Run on port 5002 (arbitrary choice for the chatbot microservice)
    app.run(port=5002, debug=True)

