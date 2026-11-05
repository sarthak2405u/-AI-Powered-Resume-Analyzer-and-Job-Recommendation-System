# AI-Powered Resume Analyzer and Job Recommendation System

An AI-powered web application that analyzes resumes, extracts skills, recommends suitable job roles, and identifies skill gaps using Natural Language Processing (NLP) and semantic similarity techniques.

The main objective of this project is to help job seekers evaluate their resumes, discover relevant career opportunities, and identify the technical skills they need to improve.

## 🚀 Features

- **Resume Upload:** Upload resumes in PDF and DOCX formats.
- **Resume Parsing:** Extract text and relevant information from uploaded resumes.
- **Skill Extraction:** Automatically identify technical and professional skills.
- **Job Recommendations:** Recommend suitable job roles based on resume content.
- **Semantic Similarity:** Use Sentence Transformers to compare resumes with job descriptions.
- **Skill Matching:** Calculate skill match scores between resumes and job requirements.
- **Skill Gap Analysis:** Identify missing skills for recommended job roles.
- **Interactive Dashboard:** Display resume analysis results using Streamlit.
- **Data Visualization:** Present insights through charts and graphical representations.
- **PDF Report Generation:** Download resume analysis reports.

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core programming language |
| Streamlit | Frontend and interactive dashboard |
| FastAPI | Backend API development |
| PostgreSQL | Database management |
| SQLAlchemy | Database ORM |
| Sentence Transformers | Semantic similarity |
| Scikit-learn | Machine learning and data processing |
| Pandas | Data manipulation |
| NumPy | Numerical operations |
| PyMuPDF | PDF text extraction |
| python-docx | DOCX text extraction |
| ReportLab | PDF report generation |
| Uvicorn | FastAPI server |

## 🏗️ Project Architecture

The application follows a frontend-backend architecture.

1. **Frontend:** Streamlit provides the user interface for resume uploads and displaying analysis results.
2. **Backend:** FastAPI processes uploaded resumes and handles the analysis workflow.
3. **Resume Processing:** Extracts text from PDF and DOCX documents.
4. **Skill Extraction:** Identifies relevant skills from resume content.
5. **Job Recommendation:** Compares resume information with available job descriptions.
6. **Semantic Analysis:** Uses Sentence Transformers to calculate contextual similarity.
7. **Database:** PostgreSQL stores resume information, job recommendations, and skill-gap records.
8. **Results:** Displays recommendations, matching scores, extracted skills, and skill-gap analysis.

## 📂 Project Structure

```text
AI_Resume_Analyzer/
│
├── app.py
│
├── backend/
│   ├── api.py
│   ├── auth.py
│   ├── resume_parser.py
│   ├── skill_extractor.py
│   ├── recommender.py
│   └── skill_gap.py
│
├── database/
│   ├── connection.py
│   └── models.py
│
├── data/
│   └── jobs.csv
│
├── models/
│
├── utils/
│   └── preprocessing.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

## ⚙️ Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/sarthak2405u/-AI-Powered-Resume-Analyzer-and-Job-Recommendation-System.git
```

### 2. Navigate to the Project Directory

```bash
cd AI-Resume-Analyzer
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

Activate the virtual environment.

**Windows PowerShell:**

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks script execution:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\venv\Scripts\Activate.ps1
```

### 4. Install Required Dependencies

```bash
pip install -r requirements.txt
```

### 5. Configure Environment Variables

Create a `.env` file in the root directory and configure your PostgreSQL database credentials.

```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=resume_analyzer
DB_USER=your_database_username
DB_PASSWORD=your_database_password
```

Replace the example credentials with your own database configuration.

**Note:** Never upload your `.env` file or database credentials to GitHub.

### 6. Create the PostgreSQL Database

Create a database named `resume_analyzer` in PostgreSQL.

```sql
CREATE DATABASE resume_analyzer;
```

Make sure the required database tables are initialized using the project's SQLAlchemy models.

### 7. Start the FastAPI Backend

Open the first terminal and execute:

```bash
python -m uvicorn backend.api:app --host 127.0.0.1 --port 8002
```

FastAPI documentation:

http://127.0.0.1:8002/docs

### 8. Start the Streamlit Frontend

Open a second terminal and execute:

```bash
streamlit run app.py
```

Open the application in your browser:

http://localhost:8501

**Important:** Keep both the FastAPI backend and Streamlit frontend running while using the application.

## 🔍 Application Workflow

1. Upload a resume in PDF or DOCX format.
2. Extract textual information from the uploaded resume.
3. Identify technical and professional skills using NLP-based processing.
4. Compare extracted skills with available job descriptions.
5. Calculate skill matching and semantic similarity scores.
6. Generate suitable job recommendations.
7. Identify missing skills for the recommended job roles.
8. Display the results on an interactive dashboard.
9. Generate and download the resume analysis report in PDF format.

## 🤖 Job Recommendation Methodology

The recommendation system uses two major components:

### 1. Skill Matching

The system compares the skills extracted from the resume with the skills required by different job roles.

### 2. Semantic Similarity

Sentence Transformers are used to understand the contextual similarity between resume content and job descriptions.

Both components contribute to evaluating how relevant a job role is to the uploaded resume.

## 📈 Future Enhancements

- Integration with real-time job portals and job APIs.
- Advanced resume ranking and evaluation.
- Personalized learning resource recommendations.
- Support for additional resume formats.
- Improved skill extraction using advanced NLP models.
- Cloud deployment using AWS or other cloud platforms.

## 👨‍💻 Author

**Sarthak Udapure**

AI and Machine Learning Enthusiast

- GitHub: https://github.com/sarthak2405u
- LinkedIn: www.linkedin.com/in/sarthak-udapure-1a2a47265

## ⭐ Support

If you find this project useful, please consider giving this repository a star!