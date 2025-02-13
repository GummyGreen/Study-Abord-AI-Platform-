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

from flask import Flask, request, jsonify
import openai
import pymongo

app = Flask(__name__)

# MongoDB connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["university_database"]
university_collection = db["universities"]

# Configure OpenAI GPT API
openai.api_key = "YOUR_OPENAI_API_KEY"

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    # Get query parameters
    gpa = request.args.get('GPA')
    budget = request.args.get('budget')
    country_preference = request.args.get('countryPreference')
    
    # Fetch relevant data from MongoDB
    universities = university_collection.find({
        "country": country_preference,
        "fees": {"$lte": int(budget)},
        "min_gpa": {"$lte": float(gpa)}
    })
    
    university_list = list(universities)
    
    # Use GPT to refine and rank the results
    prompt = f"Given these universities: {university_list}, rank and summarize them for a student with a GPA of {gpa}, budget of {budget}, and preference for {country_preference}."
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=500
    )
    
    return jsonify({"recommendations": response.choices[0].text.strip()})

if __name__ == '__main__':
    app.run(port=5001, debug=True)
