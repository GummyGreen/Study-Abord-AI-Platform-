# **Study Abroad AI Assistant**

The **Study Abroad AI Assistant** is a microservices-based platform designed to help international students find suitable universities, manage their applications, and navigate complex visa processes. It combines AI-driven recommendations, a chatbot for Q&A, and application tracking features into a single, scalable solution.

## **Table of Contents**
1. [Overview](#overview)  
2. [Key Features](#key-features)  
3. [Architecture](#architecture)  
4. [Project Structure](#project-structure)  
5. [Prerequisites](#prerequisites)  
6. [Local Setup](#local-setup)  
7. [Microservices](#microservices)  
8. [Usage](#usage)  
9. [Contributing](#contributing)  
10. [License](#license)

---

## **1. Overview**

With thousands of universities worldwide, varying visa rules, and tedious application steps, the study abroad process can be overwhelming. This platform leverages **AI models** (Transformer-based, e.g., BERT/GPT) for:

- **Personalized university recommendations** (hybrid filtering approach).  
- **Chatbot-based guidance** for application and visa queries.  
- **Automated document assistance** for drafting Statements of Purpose (SOPs) and Letters of Recommendation (LORs).  

By centralizing these features, students can streamline their journey from application to admission and visa approval.

---

## **2. Key Features**

1. **University Matching Engine**  
   - **Hybrid Recommendation** using collaborative filtering and content-based filtering.  
   - Ranks and filters institutions by **location, fees, ranking,** and other user preferences.

2. **AI Chatbot**  
   - Natural Language Processing (NLP) using **transformer-based models**.  
   - Provides real-time Q&A on **application procedures** and **visa requirements**.

3. **Document Assistant**  
   - Generates **SOP/LOR drafts** using GPT-based models.  
   - Integrates with grammar and plagiarism APIs for improved language quality.

4. **Visa Guidance**  
   - Stores country-specific visa rules and checklists.  
   - Offers **rule-based** steps and NLP-driven answers to user queries.

5. **Scalable & Modular**  
   - Each feature is a **microservice** with dedicated endpoints.  
   - Containerized deployment on **Google Cloud (GCP)** with automated CI/CD.

---

## **3. Architecture**

The platform uses a **microservices** architecture, where each service runs independently and communicates via RESTful APIs. Below is a simplified view:

```
┌─────────────┐
│   Frontend   │ (React.js)
└─────────────┘
      |
      | REST/GraphQL
      |
┌────────────────────────────┐       ┌───────────────┐
│ University Matching Service│ <---->│  MongoDB       │
└────────────────────────────┘       └───────────────┘
┌────────────────────────────┐       ┌───────────────┐
│ Chatbot Service            │ <---->│  ML Models     │
└────────────────────────────┘       └───────────────┘
┌────────────────────────────┐
│ Document Assistant Service │
└────────────────────────────┘
┌────────────────────────────┐
│ Visa Guidance Service      │
└────────────────────────────┘
```

- **Backend**: Python/Flask microservices for each core function.  
- **Database**: MongoDB (Atlas or local) to store unstructured data (universities, visa info, user profiles).  
- **AI Models**: Transformer-based models (BERT, GPT) fine-tuned on domain-specific datasets.  
- **MLOps**: MLflow for model tracking; Docker & Kubernetes for deployment.  

---

## **4. Project Structure**

A possible layout for this repository:

```
study-abroad-ai-assistant/
├── university-matching/
│   ├── app.py                # Flask entry point for university matching
│   ├── requirements.txt      # Dependencies for this service
│   ├── db.py                 # MongoDB connection code
│   └── ...
├── chatbot/
│   ├── app.py                # Flask entry point for chatbot
│   ├── requirements.txt
│   ├── ...
├── document-assistant/
│   ├── app.py
│   ├── requirements.txt
│   └── ...
├── visa-guidance/
│   ├── app.py
│   ├── requirements.txt
│   └── ...
├── frontend/
│   ├── package.json
│   ├── src/
│   └── ...
├── docker-compose.yml        # (optional) Or separate Dockerfiles for each service
├── .github/workflows/ci.yml  # CI/CD pipeline (GitHub Actions)
├── README.md                 # You are here!
└── ...
```

---

## **5. Prerequisites**

- **Python 3.8+** for backend microservices  
- **Node.js 14+** for the React.js frontend  
- **MongoDB** (local or Atlas)  
- **Docker** (optional, for containerized deployment)  
- **Git** for version control  
- **(Optional) GCP CLI** for deployment on Google Cloud

---

## **6. Local Setup**

1. **Clone the Repository**  
   ```bash
   git clone https://github.com/<your-org>/study-abroad-ai-assistant.git
   cd study-abroad-ai-assistant
   ```

2. **Set Up Python Environments**  
   - For each microservice (e.g., `university-matching`):
     ```bash
     cd university-matching
     python -m venv venv
     source venv/bin/activate  # or venv\Scripts\activate on Windows
     pip install -r requirements.txt
     ```

3. **Run MongoDB**  
   - **Option A: Local**  
     ```bash
     # Mac/Ubuntu typically
     sudo service mongod start
     ```
   - **Option B: Docker**  
     ```bash
     docker run -d -p 27017:27017 --name mongo mongo
     ```

4. **Launch Each Microservice**  
   In separate terminals (or use `tmux`/`screen`):
   ```bash
   # University Matching Service
   cd university-matching
   source venv/bin/activate
   python app.py

   # Chatbot Service
   cd chatbot
   source venv/bin/activate
   python app.py

   # Document Assistant Service
   cd document-assistant
   source venv/bin/activate
   python app.py

   # Visa Guidance Service
   cd visa-guidance
   source venv/bin/activate
   python app.py
   ```
   By default, each Flask service may run on a different port (e.g., 5001, 5002, etc.). Adjust as needed.

5. **Frontend**  
   ```bash
   cd frontend
   npm install
   npm start
   # Access at http://localhost:3000 (default for CRA/Vite/Next.js)
   ```

---

## **7. Microservices**

### University Matching Service
- **Location**: `university-matching/`
- **Core Endpoint**:  
  - `GET /recommendations`  
    Returns a list of recommended universities based on query params (e.g., `GPA`, `countryPreference`, `budget`).

### Chatbot Service
- **Location**: `chatbot/`
- **Core Endpoint**:  
  - `POST /chat`  
    Receives a `user_query` and responds with AI-generated answers using a transformer-based model (BERT/GPT).

### Document Assistant Service
- **Location**: `document-assistant/`
- **Core Endpoint**:  
  - `POST /generate-sop`  
    Accepts user profile information (academic background, achievements, etc.) and returns a draft SOP.

### Visa Guidance Service
- **Location**: `visa-guidance/`
- **Core Endpoint**:  
  - `GET /visa-info?country=COUNTRY_NAME`  
    Fetches visa requirements and steps for the specified country.

---

## **8. Usage**

1. **University Matching**  
   - Send a GET request:
     ```
     GET http://localhost:5001/recommendations?GPA=3.5&budget=30000&countryPreference=Canada
     ```
   - Response contains a JSON list of recommended universities.

2. **Chatbot**  
   - Send a POST request with JSON body:
     ```json
     {
       "user_query": "How do I apply for a Master's in Computer Science?"
     }
     ```
   - Expect a JSON response with the chatbot’s answer.

3. **Document Assistant**  
   - Send a POST request with SOP details:
     ```json
     {
       "student_profile": {
         "major": "Computer Science",
         "achievements": ["research publication", "internship at XYZ"],
         "target_university": "ABC University"
       }
     }
     ```
   - Response includes a generated SOP draft with placeholders you can edit.

4. **Visa Guidance**  
   - Send a GET request:
     ```
     GET http://localhost:5003/visa-info?country=Canada
     ```
   - Response returns a step-by-step guide for the specified country.

---

## **9. Contributing**

We welcome contributions from the community or collaborators! To get started:

1. **Fork** the repository.  
2. **Create** a new feature branch (e.g., `feature/my-new-idea`).  
3. **Commit** your changes and **push** to your branch.  
4. **Open a Pull Request** and describe your changes in detail.

Please ensure that your code follows our style guidelines and passes all tests (see `.github/workflows/ci.yml`).

---

## **10. License**

This project is licensed under the [MIT License](./LICENSE). You’re free to use, modify, and distribute the code as long as the original license is included.

---

### **Contact & Support**

- If you have questions or want to discuss features, please open an **Issue** in this repo.  
- For direct inquiries, email the core team at [example@studyabroadai.com](mailto:example@studyabroadai.com).

_Thanks for checking out the Study Abroad AI Assistant! We hope it helps streamline your international study journey._
