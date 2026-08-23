# Resume Ranker 📄

An intelligent resume ranking application that uses AI to evaluate and rank candidate resumes against a job description. This application helps recruiters quickly identify the best-fit candidates by leveraging advanced language models for resume analysis.

## Features

- **Job Description Input**: Paste any job description to set your evaluation criteria
- **Multiple Resume Upload**: Upload multiple PDF resumes at once for batch evaluation
- **AI-Powered Evaluation**: Uses a large language model (via Groq) to intelligently analyze resumes
- **Ranked Results**: Candidates are automatically ranked by match score (0-100)
- **Detailed Analysis**: For each candidate, view:
  - **Match Score**: Overall fit percentage
  - **Strengths**: Key qualifications that align with the job
  - **Weaknesses**: Skills or experience gaps
- **Parallel Processing**: Evaluates multiple resumes simultaneously for faster results
- **Clean Web Interface**: Built with Streamlit for an intuitive, user-friendly experience

## Tech Stack

- **Frontend**: [Streamlit](https://streamlit.io/) - Fast web app framework
- **Backend**: Python
- **AI/LLM**: [LangChain](https://www.langchain.com/) + [Groq](https://groq.com/) - High-performance language model inference
- **PDF Processing**: [PyPDF](https://github.com/py-pdf/pypdf) - Extract text from PDF resumes
- **Concurrency**: Python `ThreadPoolExecutor` - Parallel resume evaluation

## Prerequisites

- Python 3.8+
- A Groq API key (free tier available at [groq.com](https://groq.com))

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Zunaira-Mazhar/resume-ranker.git
   cd resume-ranker
