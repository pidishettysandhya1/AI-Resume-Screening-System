import streamlit as st
import pdfplumber
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ===============================
# PAGE SETTINGS
# ===============================
st.set_page_config(
    page_title="AI Resume Screening System",
    layout="wide"
)

st.title("🚀 AI Resume Screening System")

# ===============================
# FUNCTIONS
# ===============================

def extract_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text.lower()

def get_similarity_score(resume_text, jd_text):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform([resume_text, jd_text])
    score = cosine_similarity(vectors[0], vectors[1])[0][0]
    return round(score * 100, 2)

def skill_match_percentage(found, required):
    if len(required) == 0:
        return 0
    return round((len(found) / len(required)) * 100, 2)

# ===============================
# JOB DESCRIPTION
# ===============================
st.subheader("📄 Job Description")

job_description = st.text_area(
    "Paste Job Description Here",
    height=220
)

# ===============================
# UPLOAD FILES
# ===============================
st.subheader("📂 Upload Resume PDFs")

uploaded_files = st.file_uploader(
    "Upload multiple resumes",
    type=["pdf"],
    accept_multiple_files=True
)

# ===============================
# ANALYZE
# ===============================
if st.button("🔍 Analyze Resumes"):

    if not job_description:
        st.warning("Please enter Job Description.")
    elif not uploaded_files:
        st.warning("Please upload resumes.")
    else:

        st.success("✅ Analysis Completed Successfully!")

        skills = [
            "python","java","sql","machine learning",
            "nlp","flask","django","pandas","numpy","api"
        ]

        required_skills = [s for s in skills if s in job_description.lower()]

        results = []

        for file in uploaded_files:
            resume_text = extract_text(file)
            score = get_similarity_score(resume_text, job_description)

            found = [s for s in skills if s in resume_text]
            missing = [s for s in required_skills if s not in resume_text]

            skill_percent = skill_match_percentage(found, required_skills)

            results.append({
                "Name": file.name,
                "Score": score,
                "Found": found,
                "Missing": missing,
                "Skill%": skill_percent
            })

        # SORT RESULTS
        results = sorted(results, key=lambda x: x["Score"], reverse=True)

        # ===============================
        # DASHBOARD
        # ===============================
        st.markdown("---")
        st.subheader("📊 ATS Dashboard")

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Resumes", len(results))
        col2.metric("Top ATS Score", f"{results[0]['Score']}%")
        col3.metric("Best Candidate", results[0]["Name"])

        st.markdown("---")

        # ===============================
        # TOP CANDIDATE CARD
        # ===============================
        st.success(f"🏆 TOP CANDIDATE: {results[0]['Name']}  |  Score: {results[0]['Score']}%")

        # ===============================
        # DOWNLOAD REPORT
        # ===============================
        df = pd.DataFrame(results)
        csv = df[["Name","Score","Skill%"]].to_csv(index=False)

        st.download_button(
            "📥 Download Ranking Report (CSV)",
            csv,
            "ATS_Ranking_Report.csv",
            "text/csv"
        )

        st.markdown("---")
        st.header("🏅 Candidate Ranking")

        # ===============================
        # RESULT CARDS
        # ===============================
        for rank, r in enumerate(results, start=1):

            score = r["Score"]

            if score >= 70:
                color = "🟢"
                status = "Excellent Match"
            elif score >= 40:
                color = "🟡"
                status = "Average Match"
            else:
                color = "🔴"
                status = "Low Match"

            with st.expander(f"{color} Rank {rank}: {r['Name']}"):

                st.progress(int(score))
                st.write(f"⭐ ATS Score: **{score}%**")
                st.write(f"📈 Skill Match: **{r['Skill%']}%**")
                st.info(f"📊 Status: {status}")

                c1, c2 = st.columns(2)

                with c1:
                    st.success("✔ Skills Found")
                    st.write(", ".join(r["Found"]) if r["Found"] else "None")

                with c2:
                    st.error("❌ Missing Skills")
                    st.write(", ".join(r["Missing"]) if r["Missing"] else "None")

                st.markdown("---")