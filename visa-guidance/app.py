# visa-guidance/app.py
#
# A simple Flask chatbot for visa guidance:
#  1. Loads data from ../data/visa_requirements.json
#  2. Expects a POST /chat with JSON: { "user_query": "..." }
#  3. Uses naive keyword matching to figure out which country the user is asking about,
#     and whether they're asking about 'steps' or 'documents'.
#  4. Returns the relevant info in a "reply" field of the JSON response.
#
# Example user queries:
#   - "How do I get a US student visa?"
#   - "Which documents do I need for Canada?"
#   - "What is the process for F-1?"
#
# Adapt or expand for real-world usage.

import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Path to the local JSON file with visa requirements
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'visa_requirements.json')

def load_visa_data():
    """
    Loads visa requirements from a local JSON file.
    Returns a dictionary keyed by country (e.g., "USA", "Canada"), each with
    'visaType', 'steps', 'requiredDocuments', etc.
    """
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Load the data at startup
VISA_DATA = load_visa_data()

@app.route('/chat', methods=['POST'])
def chat():
    """
    Expects JSON input: { "user_query": "string" }
    Returns a naive rule-based response about visa steps or documents.
    """
    user_query = request.json.get('user_query', '').strip().lower()

    # Fallback answer if we cannot parse the query
    answer = "Sorry, I’m not sure how to answer that. Can you be more specific?"

    if not user_query:
        return jsonify({"reply": answer}), 200

    # Attempt to figure out which country the user is asking about
    # We'll check each country in VISA_DATA to see if it's mentioned in user_query
    # e.g., if user_query has 'us' or 'usa' => match "USA"
    #       if user_query has 'canada' => match "Canada"

    matched_country = None
    for country in VISA_DATA:
        if country.lower() in user_query:
            matched_country = country
            break
        # Sometimes people say 'us' instead of 'usa':
        if country.lower() == "usa" and ("us " in user_query or "u.s." in user_query):
            matched_country = "USA"
            break

    # If no direct match, you can do more advanced NER or partial matching,
    # but let's keep it simple for now.

    if matched_country:
        country_data = VISA_DATA[matched_country]
        # Check if user is asking about steps or documents
        if "step" in user_query or "process" in user_query or "how to" in user_query:
            # Return the "steps" info
            steps_list = country_data.get("steps", [])
            if steps_list:
                steps_text = "\n".join([f"{i+1}. {step}" for i, step in enumerate(steps_list)])
                answer = (f"The process for a {country_data['visaType']} in {matched_country} typically includes:\n"
                          f"{steps_text}\nGood luck!")
            else:
                answer = (f"Sorry, I don't have specific steps for {matched_country}.")
        elif "document" in user_query or "paper" in user_query or "requirement" in user_query:
            # Return the "requiredDocuments" info
            docs_list = country_data.get("requiredDocuments", [])
            if docs_list:
                docs_text = ", ".join(docs_list)
                answer = (f"For a {country_data['visaType']} in {matched_country}, "
                          f"common required documents include: {docs_text}.")
            else:
                answer = (f"Sorry, I don't have a document list for {matched_country}.")
        else:
            # If the user references the country but not steps/documents
            # (maybe they're asking about something else)
            # Provide a generic prompt
            answer = (f"I see you're interested in {matched_country}. You might ask about the 'steps' "
                      f"or 'documents' needed for the {country_data['visaType']} process.")
    else:
        # The user didn't mention a recognized country
        # We might guess if they're referencing 'F-1' or 'student visa'
        if "f-1" in user_query or "student visa" in user_query or "study permit" in user_query:
            answer = ("Which country do you want to apply for? For example, 'US student visa' or 'Canada study permit'. "
                      "Currently, I have data for the USA and Canada.")
        else:
            answer = ("I'm not sure which country you're referring to. "
                      "Currently, I can provide info on USA or Canada. Please specify a country name.")

    return jsonify({"reply": answer}), 200

if __name__ == '__main__':
    # Run on port 5004 (for example) in debug mode
    app.run(port=5004, debug=True)

