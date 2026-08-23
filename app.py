import streamlit as st
from backend import rank_resumes

st.set_page_config(page_title="Resume Ranker", page_icon="📄", layout="wide")

st.title("Resume Ranking Assistant")
st.caption("Upload resumes and a job description to get a ranked list of best-fit candidates.")

# Job description input
job_description = st.text_area(
    "Paste the Job Description here:",
    height=150,
    placeholder="e.g. We are looking for a Python developer with 3+ years of experience...",
    key="job_desc_input"
)



# Multiple resume upload
uploaded_files = st.file_uploader(
    "Upload Resumes (PDF only):",
    type=["pdf"],
    accept_multiple_files=True
)

# Evaluate button
if st.button("Rank Resumes", type="primary"):
    if not job_description:
        st.warning("Please paste a job description first.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        with st.spinner("Evaluating resumes..."):
            results = rank_resumes(uploaded_files, job_description)

        st.success(f"Evaluated {len(results)} resumes!")

        st.subheader("Ranked Candidates")

        for i, candidate in enumerate(results, start=1):
            with st.container(border=True):
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"**#{i}. {candidate['name']}**")
                with col2:
                    st.markdown(f"**Score: {candidate['match_score']}/100**")

                st.write(f"**Strengths:** {candidate['strengths']}")
                st.write(f"**Weaknesses:** {candidate['weaknesses']}")
