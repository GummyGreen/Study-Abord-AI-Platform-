# document-assistant/app.py
#
# A simple Flask application that:
# 1. Loads a local JSON dataset ("distilled_data.json") from ../data/
# 2. Provides a POST /generate-sop endpoint, which takes:
#     {
#       "student_id": 1,
#       "additional_goals": "I want to focus on machine learning.",
#       "target_program": "M.S. in Computer Science at XYZ University"
#     }
# 3. Returns a naive SOP draft by combining data from the student's record
#    with the provided "additional_goals" and "target_program".
#
# For a more robust solution:
#  - Integrate GPT (e.g., via OpenAI API) and pass relevant data as prompts.
#  - Use a templating engine or a specialized library for text generation.

import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Adjust the path to match your local folder structure
DATA_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'distilled_data.json')

def load_distilled_data():
    """
    Load the distilled dataset (10 or so records) from a local JSON file.
    Returns a list of dictionaries, each representing a student's info.
    """
    with open(DATA_PATH, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Load the dataset once at startup
DISTILLED_DATA = load_distilled_data()

@app.route('/generate-sop', methods=['POST'])
def generate_sop():
    """
    POST /generate-sop
    Expects a JSON body, e.g.:
      {
        "student_id": 1,
        "additional_goals": "I want to focus on machine learning.",
        "target_program": "M.S. in Computer Science at XYZ University"
      }

    Returns a naive SOP draft in JSON:
      {
        "sop_draft": "...multi-paragraph text..."
      }
    """
    data = request.get_json(force=True)

    student_id = data.get('student_id')
    additional_goals = data.get('additional_goals', '')
    target_program = data.get('target_program', '')

    # Find the matching student record in the loaded dataset
    student_record = None
    for record in DISTILLED_DATA:
        if record.get('student_id') == student_id:
            student_record = record
            break

    if not student_record:
        return jsonify({
            "error": f"No student found with student_id={student_id}"
        }), 404

    # Retrieve info from the student's record
    undergrad_univ = student_record.get('undergrad_university', 'Unknown University')
    major = student_record.get('major', 'Undeclared Major')
    gpa = student_record.get('GPA', 0.0)
    sop_excerpt = student_record.get('SoP_excerpt', '')
    location_pref = student_record.get('location_preference', '')

    # Construct a naive SOP draft
    sop_draft = (
        f"Statement of Purpose (Draft)\n\n"
        f"Introduction:\n"
        f"I am a graduate of {undergrad_univ}, where I studied {major} and achieved a GPA of {gpa}. "
        f"My academic journey has been shaped by a persistent curiosity and a drive to explore "
        f"the leading frontiers of my field. {sop_excerpt}\n\n"

        f"Motivation and Goals:\n"
        f"I am applying to {target_program or 'your esteemed graduate program'} to deepen my expertise "
        f"in {major} and further hone my research capabilities. {additional_goals}\n\n"

        f"Why This Program:\n"
        f"I believe that the location preference of {location_pref} in the United States offers an "
        f"excellent environment for both academic success and cultural enrichment. "
        f"Through engagement with diverse peers and faculty, I hope to cultivate new perspectives "
        f"and innovative approaches.\n\n"

        f"Future Plans:\n"
        f"My post-graduate aspiration is to leverage the knowledge and experience gained from this "
        f"program and make meaningful contributions in my field. Whether in industry or academia, "
        f"I aim to build upon the foundation established at {undergrad_univ}, and I am confident "
        f"that by attending this graduate program, I will be one step closer to achieving "
        f"my long-term goals.\n\n"

        f"Conclusion:\n"
        f"Thank you for considering my application. I look forward to the opportunity to further "
        f"discuss how my background, passion, and goals align with the values of your institution.\n"
    )

    return jsonify({"sop_draft": sop_draft}), 200

if __name__ == '__main__':
    app.run(port=5003, debug=True)

