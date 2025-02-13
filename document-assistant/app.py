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

from flask import Flask, request, jsonify
import openai
import pymongo

app = Flask(__name__)

# Configure OpenAI GPT API
openai.api_key = "YOUR_OPENAI_API_KEY"

# MongoDB connection for fetching university-specific requirements
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["university_database"]
university_collection = db["universities"]

# Sample stateful conversation storage (to be replaced with a more robust solution in production)
session_state = {}

@app.route('/start-sop-conversation', methods=['POST'])
def start_sop_conversation():
    """Initialize the SOP drafting process."""
    student_id = request.json.get("student_id")
    university_name = request.json.get("university_name")
    
    # Fetch university-specific background and requirements
    university = university_collection.find_one({"name": {"$regex": f"^{university_name}$", "$options": "i"}})
    
    if not university:
        return jsonify({"message": f"University '{university_name}' not found in our database."}), 404
    
    session_state[student_id] = {
        "university_name": university_name,
        "university_requirements": university.get("requirements", "General SOP requirements."),
        "conversation_history": []
    }
    
    question = "Let's begin drafting your SOP. To start, tell me about your academic background and major achievements."
    session_state[student_id]["conversation_history"].append({"role": "assistant", "content": question})
    
    return jsonify({"message": question})

@app.route('/continue-sop-conversation', methods=['POST'])
def continue_sop_conversation():
    """Continue the SOP drafting conversation."""
    student_id = request.json.get("student_id")
    student_response = request.json.get("student_response")
    
    if student_id not in session_state:
        return jsonify({"message": "No active SOP drafting session found. Please start a new session."}), 400
    
    session_state[student_id]["conversation_history"].append({"role": "student", "content": student_response})
    
    # Generate AI-driven follow-up or partial SOP draft based on the conversation history
    conversation_history = session_state[student_id]["conversation_history"]
    prompt = create_prompt(conversation_history, session_state[student_id]["university_requirements"])
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=800,
        temperature=0.7
    )
    
    assistant_reply = response.choices[0].text.strip()
    session_state[student_id]["conversation_history"].append({"role": "assistant", "content": assistant_reply})
    
    return jsonify({"message": assistant_reply})

@app.route('/get-sop-draft', methods=['GET'])
def get_sop_draft():
    """Generate and return the full SOP draft based on the conversation history."""
    student_id = request.args.get("student_id")
    
    if student_id not in session_state:
        return jsonify({"message": "No active SOP session found."}), 400
    
    conversation_history = session_state[student_id]["conversation_history"]
    final_prompt = create_prompt(conversation_history, session_state[student_id]["university_requirements"], full_draft=True)
    
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=final_prompt,
        max_tokens=1500,
        temperature=0.7
    )
    
    sop_draft = response.choices[0].text.strip()
    
    return jsonify({"sop_draft": sop_draft})

def create_prompt(conversation_history, university_requirements, full_draft=False):
    """Generate the GPT prompt based on the conversation history and university requirements."""
    conversation_text = "\n".join([f"{entry['role'].capitalize()}: {entry['content']}" for entry in conversation_history])
    
    if full_draft:
        return f"""
        Based on the following conversation and the university-specific requirements, generate a full Statement of Purpose (SOP):

        University Requirements: {university_requirements}

        Conversation:
        {conversation_text}

        Draft the SOP in a professional and structured manner with appropriate sections for introduction, academic background, professional experience, goals, and conclusion.
        """
    else:
        return f"""
        Continue this conversation for drafting a Statement of Purpose (SOP) based on the student's responses and the following university-specific requirements:

        University Requirements: {university_requirements}

        Conversation so far:
        {conversation_text}

        Provide the next question or generate a partial SOP draft based on the responses so far.
        """

if __name__ == '__main__':
    app.run(port=5002, debug=True)

