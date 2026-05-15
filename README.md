# Breast Cancer Detection Backend

This project represents the backend system for an AI based Breast Cancer Detection platform. It is developed using FastAPI and is responsible for handling image uploads, validation, preprocessing, authentication, database management, and AI model integration.

---

## Project Overview

The backend system performs the following tasks:

- Secure image upload (JPG / JPEG / PNG)
- File validation (type, size, dimensions)
- Image preprocessing (resize + normalization)
- Ultrasound-like detection (grayscale check)
- Integration with AI model via API
- User authentication using JWT
- Storing analysis results in database
- Retrieving user history
- Structured API responses

---

## System Architecture

Doctor → Backend → AI Model → Backend → Database → Doctor

- The backend validates and processes the image  
- Sends it to the AI model  
- Receives prediction results  
- Stores results in database  
- Returns results to the user  

---

## Project Structure

```
BC_DETECTION_BACKEND/

app/
├── main.py
├── database.py
│
├── models/
│   ├── user.py
│   └── analysis.py
│
├── routes/
│   ├── auth.py
│   └── predict.py
│
├── services/
│   ├── ai_service.py
│   ├── model_service.py
│   └── security.py
│
├── utils/
│   ├── validators.py
│   └── preprocess.py
│
└── __init__.py

database.db
requirements.txt
.gitignore
README.md
```
---

## Installation

1. Clone the repository:

   git clone https://github.com/YOUR_USERNAME/breast-cancer-backend.git

2. Navigate to the project directory:

   cd breast-cancer-backend

3. (Optional) Create a virtual environment:

   python -m venv venv

4. Activate the virtual environment:

   Windows:
   venv\Scripts\activate

5. Install required packages:

   pip install -r requirements.txt

---

## Running the Server

Start the development server using:

   uvicorn app.main:app --reload

The API will run at:

   http://127.0.0.1:8000

API documentation (Swagger UI):

   http://127.0.0.1:8000/docs

---

## API Endpoints

Authentication
- POST /register
- POST /login
Prediction
- POST /predict
- Requires image + token
User Data
- GET /history
- GET /analysis/{id}

---

## AI Integration

The backend integrates with an external AI model hosted on Render.

- The image is sent to the AI service
- The AI model processes it and returns prediction results
- The backend stores and returns the result

---

## Security Measures

- File type validation
- Content type validation
- Image verification using PIL
- File size limitation
- Dimension validation
- JWT authentication
- Password hashing
- Protected endpoints

---

## Academic Context

This backend is part of a university graduation project focused on AI based breast cancer detection using ultrasound images.

The system is designed as a decision-support tool and not a replacement for medical diagnosis.