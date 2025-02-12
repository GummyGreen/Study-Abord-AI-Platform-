# university-matching/app.py
#
# This Flask application reads a local JSON file ("distilled_data.json")
# from ../data/ and provides a basic recommendation endpoint.
#
# Usage Example:
#  GET /recommendations?GPA=3.2&major=Computer+Science&location=California
#
# The code will filter the local dataset on these query parameters:
#   - Minimum GPA
#   - Exact match on desired major (if provided)
#   - Exact match on location preference (if provided)
#
# It then returns the top 5 matches in JSON format.
# Adjust the filtering logic or limit as needed for your real use case.

import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Adjust path to match your local folder structure
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'distilled_data.json')

def load_distilled_data():
    """
    Load the distilled dataset from a local JSON file.
    Returns a list of dictionaries, each representing a student profile.
    """
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Load the dataset once at startup
DISTILLED_DATA = load_distilled_data()

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    """
    Filter the local 'distilled_data.json' based on query parameters.
    
    Query Params (all optional):
      - GPA: float, minimum GPA required (default 0.0)
      - major: str, student's intended major (exact match)
      - location: str, location preference in the US (exact match)

    Returns:
      A JSON list of up to 5 matching records from the distilled dataset.
    """
    # Parse query parameters
    try:
        min_gpa = float(request.args.get('GPA', 0.0))
    except ValueError:
        min_gpa = 0.0

    desired_major = request.args.get('major', '')  # exact text match
    desired_location = request.args.get('location', '')  # exact text match

    # Basic filtering logic
    filtered_results = []
    for record in DISTILLED_DATA:
        student_gpa = record.get('GPA', 0.0)
        student_major = record.get('major', '')
        student_location = record.get('location_preference', '')

        # Check GPA requirement
        if student_gpa < min_gpa:
            continue

        # If major is provided, check for an exact match
        if desired_major and desired_major.lower() != student_major.lower():
            continue

        # If location is provided, check for an exact match
        if desired_location and desired_location.lower() != student_location.lower():
            continue

        # If we get here, the record passed all filters
        filtered_results.append(record)

    # Limit to top 5 results (arbitrary limit for demonstration)
    top_results = filtered_results[:5]

    return jsonify({"recommendations": top_results}), 200

if __name__ == '__main__':
    # Run on port 5001 in debug mode
    app.run(port=5001, debug=True)

