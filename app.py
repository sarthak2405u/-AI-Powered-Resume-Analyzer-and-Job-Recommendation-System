import streamlit as st
import requests
import pandas as pd
import html
from io import BytesIO
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    HRFlowable
)


# =====================================================
# PDF REPORT GENERATION FUNCTION
# =====================================================

def generate_pdf_report(data):

    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "CustomTitle",
        parent=styles["Title"],
        fontSize=23,
        textColor=colors.HexColor("#312E81"),
        spaceAfter=15
    )

    heading_style = ParagraphStyle(
        "CustomHeading",
        parent=styles["Heading2"],
        fontSize=14,
        textColor=colors.HexColor("#4338CA"),
        spaceBefore=15,
        spaceAfter=10
    )

    normal_style = styles["BodyText"]

    story = []

    # REPORT TITLE

    story.append(
        Paragraph("AI RESUME ANALYZER", title_style)
    )

    story.append(
        Paragraph(
            "Resume Analysis and Job Recommendation Report",
            normal_style
        )
    )

    story.append(Spacer(1, 20))

    # RESUME INFORMATION

    story.append(
        Paragraph("1. Resume Information", heading_style)
    )

    filename = escape(
        str(data.get("filename", "Resume"))
    )

    story.append(
        Paragraph(
            f"<b>Resume:</b> {filename}",
            normal_style
        )
    )

    story.append(Spacer(1, 15))

    # EXTRACTED SKILLS

    story.append(
        Paragraph("2. Extracted Skills", heading_style)
    )

    extracted_skills = data.get(
        "extracted_skills", {}
    )

    for category, skills in extracted_skills.items():

        safe_category = escape(str(category))

        safe_skills = escape(
            ", ".join(map(str, skills))
        )

        story.append(
            Paragraph(
                f"<b>{safe_category}:</b> {safe_skills}",
                normal_style
            )
        )

        story.append(Spacer(1, 5))

    # JOB RECOMMENDATIONS

    story.append(
        Paragraph("3. Job Recommendations", heading_style)
    )

    table_data = [
        [
            "Job Role",
            "Skill Match",
            "Semantic Match",
            "Final Score"
        ]
    ]

    recommendations = data.get(
        "recommendations", []
    )

    for job in recommendations:

        table_data.append([

            Paragraph(
                escape(str(job["Job Title"])),
                normal_style
            ),

            f'{job["Skill Match"]}%',

            f'{job["Semantic Similarity"]}%',

            f'{job["Final Score"]}%'

        ])

    table = Table(
        table_data,
        colWidths=[
            2.2 * inch,
            1.1 * inch,
            1.25 * inch,
            1.1 * inch
        ],
        repeatRows=1
    )

    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#312E81")
            ),

            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.white
            ),

            (
                "FONTNAME",
                (0, 0),
                (-1, 0),
                "Helvetica-Bold"
            ),

            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#F1F5F9")
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "ALIGN",
                (1, 1),
                (-1, -1),
                "CENTER"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )

    story.append(table)

    # SKILL GAP ANALYSIS

    story.append(
        Paragraph("4. Skill Gap Analysis", heading_style)
    )

    skill_gaps = data.get(
        "skill_gap_analysis", []
    )

    if skill_gaps:

        for gap in skill_gaps:

            skill = escape(str(gap["skill"]))

            jobs = escape(
                ", ".join(gap["recommended_for"])
            )

            story.append(
                Paragraph(
                    f"<b>Missing Skill:</b> {skill}",
                    normal_style
                )
            )

            story.append(
                Paragraph(
                    f"<b>Recommended For:</b> {jobs}",
                    normal_style
                )
            )

            story.append(Spacer(1, 8))

    else:

        story.append(
            Paragraph(
                "No missing skills identified.",
                normal_style
            )
        )

    # BEST JOB MATCH

    if recommendations:

        best_job = recommendations[0]

        story.append(
            Paragraph("5. Best Job Match", heading_style)
        )

        story.append(
            Paragraph(
                f"<b>Recommended Position:</b> "
                f"{escape(str(best_job['Job Title']))}",
                normal_style
            )
        )

        story.append(
            Paragraph(
                f"<b>Compatibility Score:</b> "
                f"{best_job['Final Score']}%",
                normal_style
            )
        )

    # REPORT FOOTER

    story.append(Spacer(1, 30))

    story.append(
        HRFlowable(
            width="100%",
            color=colors.grey
        )
    )

    story.append(Spacer(1, 10))

    story.append(
        Paragraph(
            "Generated by ResumeAI - AI-Powered Resume Analyzer",
            styles["Italic"]
        )
    )

    doc.build(story)

    buffer.seek(0)

    return buffer.getvalue()


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="ResumeAI | AI Resume Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #0b1020;
    color: #f8fafc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1400px;
}

/* SIDEBAR */

[data-testid="stSidebar"] {
    background-color: #111827 !important;
    border-right: 1px solid #26334d;
}

[data-testid="stSidebar"] * {
    color: #e2e8f0;
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 {
    color: #ffffff !important;
}

[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #cbd5e1 !important;
}

[data-testid="stSidebar"] hr {
    border-color: #334155 !important;
}

/* HERO SECTION */

.hero {
    background: linear-gradient(
        120deg,
        #172554,
        #312e81,
        #581c87
    );

    padding: 45px 35px;
    border-radius: 18px;
    margin-bottom: 35px;
    border: 1px solid #6366f1;
}

.hero h1 {
    color: #ffffff !important;
    font-size: 38px;
    font-weight: 800;
    margin-bottom: 15px;
}

.hero p {
    color: #e0e7ff !important;
    font-size: 17px;
    line-height: 1.7;
}

/* SECTION HEADINGS */

.section-title {
    font-size: 25px;
    font-weight: 700;
    color: #ffffff;
    margin-top: 35px;
    margin-bottom: 20px;
}

/* GENERAL TEXT */

.stApp p {
    color: #cbd5e1;
}

.stApp h1,
.stApp h2,
.stApp h3 {
    color: #ffffff;
}

.stApp label {
    color: #e2e8f0 !important;
}

/* FILE UPLOADER */

[data-testid="stFileUploader"] {
    background-color: #172036 !important;
    border: 1px dashed #6366f1 !important;
    border-radius: 15px !important;
    padding: 15px !important;
}

[data-testid="stFileUploaderDropzone"] {
    background-color: #1e293b !important;
    border: 1px solid #475569 !important;
    border-radius: 10px !important;
}

[data-testid="stFileUploaderDropzone"] button {
    background-color: #4f46e5 !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 8px !important;
}

[data-testid="stFileUploaderDropzone"] button * {
    color: #ffffff !important;
}

[data-testid="stFileUploaderDropzone"] div,
[data-testid="stFileUploaderDropzone"] span,
[data-testid="stFileUploaderDropzone"] small {
    color: #e2e8f0 !important;
}

/* BUTTONS */

.stButton button,
.stFormSubmitButton button {
    background: linear-gradient(
        90deg,
        #4f46e5,
        #7c3aed
    ) !important;

    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 12px 25px !important;
    font-weight: 700 !important;
    min-height: 45px;
}

.stButton button:hover,
.stFormSubmitButton button:hover {
    background: linear-gradient(
        90deg,
        #4338ca,
        #6d28d9
    ) !important;

    color: #ffffff !important;
}

/* METRIC CARDS */

div[data-testid="stMetric"] {
    background-color: #172036;
    border: 1px solid #334155;
    padding: 20px;
    border-radius: 15px;
}

div[data-testid="stMetricValue"] {
    color: #818cf8;
}

div[data-testid="stMetricLabel"] {
    color: #cbd5e1;
}

/* SKILL CARDS */

.skill-card {
    background-color: #172036;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 18px;
    margin-bottom: 15px;
}

.skill-badge {
    display: inline-block;
    background-color: #312e81;
    color: #c7d2fe;
    padding: 7px 12px;
    margin: 5px 4px;
    border-radius: 20px;
    font-size: 13px;
    border: 1px solid #4f46e5;
}

/* SKILL GAP CARDS */

.gap-card {
    background-color: #2b1b2a;
    border: 1px solid #7f1d1d;
    padding: 15px;
    border-radius: 10px;
    margin-bottom: 12px;
}

/* DOWNLOAD BUTTON */

.stDownloadButton button {
    background-color: #059669 !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
}

.stDownloadButton button:hover {
    background-color: #047857 !important;
}

/* DIVIDERS */

hr {
    border-color: #334155;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown("# 🚀 ResumeAI")

    st.caption("INTELLIGENT CAREER ASSISTANT")

    st.markdown("---")

    page = st.radio(
        "NAVIGATION",
        [
            "🏠 Dashboard",
            "📊 About Project"
        ]
    )

    st.markdown("---")

    st.markdown("### 🛠️ Technologies")

    technologies = [
        "Python",
        "Machine Learning",
        "NLP",
        "Sentence Transformers",
        "FastAPI",
        "Streamlit"
    ]

    for tech in technologies:
        st.write(f"• {tech}")

    st.markdown("---")

    st.caption("ResumeAI Version 1.0")

    # ==============================================
    # USER LOGIN
    # ==============================================

    st.markdown("---")

    st.markdown("### 🔐 User Login")

    if "access_token" not in st.session_state:

        with st.form("login_form"):

            email = st.text_input("Email")

            password = st.text_input(
                "Password",
                type="password"
            )

            login_button = st.form_submit_button("Login")

        if login_button:

            try:

                login_response = requests.post(
                    "http://127.0.0.1:8002/auth/login",

                    data={
                        "username": email,
                        "password": password
                    },

                    timeout=30
                )

                if login_response.status_code == 200:

                    token_data = login_response.json()

                    st.session_state["access_token"] = (
                        token_data["access_token"]
                    )

                    st.success("Login successful!")

                    st.rerun()

                else:

                    st.error("Invalid email or password.")

            except requests.exceptions.ConnectionError:

                st.error("Cannot connect to FastAPI.")

    else:

        st.success("You are logged in!")

        if st.button("Logout"):

            st.session_state.pop("access_token", None)

            st.rerun()

    st.markdown("---")

    st.caption("ResumeAI Version 1.0")
# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero">
<h1>🚀 AI-Powered Resume Analyzer</h1>
<p>
Discover your career potential with Artificial Intelligence.
Analyze your resume, find matching jobs and identify missing skills.
</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# ABOUT PROJECT PAGE
# =====================================================

if page == "📊 About Project":

    st.markdown("## About ResumeAI")

    st.write("""
    ResumeAI is an intelligent resume analysis and job
    recommendation system developed using Python, NLP and
    Machine Learning.

    It analyzes candidate resumes, extracts technical skills,
    compares them against job descriptions and recommends
    suitable career opportunities.
    """)

    col1, col2, col3 = st.columns(3)

    col1.metric("Core Technology", "NLP")
    col2.metric("Recommendation", "AI Based")
    col3.metric("Backend", "FastAPI")

    st.markdown("### Main Features")

    features = [
        "Automated Resume Parsing",
        "Technical Skill Extraction",
        "Semantic Similarity Matching",
        "Intelligent Job Recommendations",
        "Skill Gap Analysis",
        "Visual Analytics"
    ]

    for feature in features:
        st.write(f"✅ {feature}")

    st.stop()


# =====================================================
# RESUME UPLOAD AND ANALYSIS FORM
# =====================================================

st.markdown(
    '<div class="section-title">📄 Upload Your Resume</div>',
    unsafe_allow_html=True
)

st.write(
    "Upload your PDF or DOCX resume to discover suitable "
    "job opportunities and identify your missing skills."
)

with st.form("resume_analysis_form"):

    uploaded_file = st.file_uploader(
        "Choose your resume",
        type=["pdf", "docx"],
        key="resume_upload"
    )

    analyze_button = st.form_submit_button(
        "🚀 Analyze My Resume",
        use_container_width=True
    )

    
# =====================================================
# PROCESS RESUME
# =====================================================

if analyze_button:

    if uploaded_file is None:

        st.warning("Please upload your resume first.")

    else:

        try:

            with st.spinner(
                "AI is analyzing your resume. Please wait..."
            ):

                response = requests.post(
                    "http://127.0.0.1:8002/analyze-resume",

                    files={
                        "file": (
                            uploaded_file.name,
                            uploaded_file.getvalue(),
                            uploaded_file.type
                        )
                    },

                    timeout=300
                )

                if response.status_code == 200:

                    st.session_state["analysis"] = response.json()

                    st.success(
                        "Your resume has been analyzed successfully!"
                    )

                else:

                    st.error(
                        f"API Error: {response.status_code}"
                    )

                    st.code(response.text)

        except requests.exceptions.ConnectionError:

            st.error(
                "Cannot connect to FastAPI. "
                "Please ensure your backend server is running."
            )

        except requests.exceptions.Timeout:

            st.error(
                "The request timed out. Please try again."
            )

        except Exception as error:

            st.error(f"Something went wrong: {error}")

# =====================================================
# DISPLAY ANALYSIS RESULTS
# =====================================================

if "analysis" in st.session_state:

    data = st.session_state["analysis"]

    recommendations = data.get("recommendations", [])

    if not recommendations:

        st.warning("No job recommendations were generated.")

        st.stop()

    st.markdown("---")


    # =================================================
    # CAREER OVERVIEW
    # =================================================

    st.markdown(
        '<div class="section-title">📈 Your Career Overview</div>',
        unsafe_allow_html=True
    )

    best_job = recommendations[0]

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Best Matching Job",
        best_job["Job Title"]
    )

    col2.metric(
        "Compatibility Score",
        f'{best_job["Final Score"]}%'
    )

    col3.metric(
        "Jobs Analyzed",
        len(recommendations)
    )


    # =================================================
    # EXTRACTED SKILLS
    # =================================================

    st.markdown(
        '<div class="section-title">🧠 Extracted Skills</div>',
        unsafe_allow_html=True
    )

    extracted_skills = data.get("extracted_skills", {})

    if extracted_skills:

        for category, skills in extracted_skills.items():

            safe_category = html.escape(category)

            badges = "".join(
                f'<span class="skill-badge">'
                f'{html.escape(skill)}</span>'
                for skill in skills
            )

            st.markdown(
                f"""
                <div class="skill-card">
                    <b>{safe_category}</b>
                    <br>
                    {badges}
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.warning("No skills were identified in this resume.")


    # =================================================
    # JOB RECOMMENDATIONS
    # =================================================

    st.markdown(
        '<div class="section-title">💼 Recommended Job Positions</div>',
        unsafe_allow_html=True
    )

    for index, job in enumerate(recommendations[:5], start=1):

        with st.container(border=True):

            col1, col2 = st.columns([3, 1])

            with col1:

                st.markdown(
                    f"### {index}. {job['Job Title']}"
                )

                st.write(
                    f"Skill Match: {job['Skill Match']}%"
                )

                st.progress(
                    min(
                        max(float(job["Skill Match"]) / 100, 0),
                        1
                    )
                )

                st.write(
                    f"Semantic Similarity: "
                    f"{job['Semantic Similarity']}%"
                )

                matched_skills = job["Matched Skills"]

                st.write(
                    "Matched Skills: " +
                    (
                        ", ".join(matched_skills)
                        if matched_skills
                        else "None"
                    )
                )

            with col2:

                st.metric(
                    "Final Score",
                    f'{job["Final Score"]}%'
                )


    # =================================================
    # JOB MATCHING ANALYTICS
    # =================================================

    st.markdown(
        '<div class="section-title">📊 Job Matching Analytics</div>',
        unsafe_allow_html=True
    )

    df = pd.DataFrame(recommendations)

    chart_data = df[
        ["Job Title", "Final Score"]
    ].set_index("Job Title")

    st.bar_chart(
        chart_data,
        horizontal=True
    )


    # =================================================
    # SKILL GAP ANALYSIS
    # =================================================

    st.markdown(
        '<div class="section-title">🎯 Skill Gap Analysis</div>',
        unsafe_allow_html=True
    )

    skill_gaps = data.get("skill_gap_analysis", [])

    if skill_gaps:

        for gap in skill_gaps:

            safe_skill = html.escape(gap["skill"])

            safe_jobs = html.escape(
                ", ".join(gap["recommended_for"])
            )

            st.markdown(
                f"""
                <div class="gap-card">
                    <b>⚠️ Missing Skill: {safe_skill}</b>
                    <br>
                    <small>
                        Recommended for: {safe_jobs}
                    </small>
                </div>
                """,
                unsafe_allow_html=True
            )

    else:

        st.success(
            "No missing skills identified in the top recommendations."
        )


    # =================================================
    # DOWNLOAD PDF REPORT
    # =================================================

    st.markdown("---")

    st.markdown(
        '<div class="section-title">📥 Download Your Report</div>',
        unsafe_allow_html=True
    )

    pdf_report = generate_pdf_report(data)

    st.download_button(
        label="📄 Download Resume Analysis (PDF)",
        data=pdf_report,
        file_name="ResumeAI_Analysis_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )

    st.success(
        "Your resume analysis is complete!"
    )