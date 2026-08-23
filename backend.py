import os
from dotenv import load_dotenv
from pypdf import PdfReader
from langchain_groq import ChatGroq
from concurrent.futures import ThreadPoolExecutor
import json

# Load API key from .env file
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Setup LLM
llm = ChatGroq(model="openai/gpt-oss-120b", temperature=0)


def extract_text_from_pdf(file):
    """Extracts all text from a single PDF file"""
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text


def evaluate_resume(resume_data, job_description):
    """Evaluates a single resume against the job description using the LLM"""
    name = resume_data["name"]
    resume_text = resume_data["text"]

    prompt = f"""You are an expert HR recruiter. Evaluate this resume against the job description.

Job Description:
{job_description}

Resume:
{resume_text}

Respond ONLY in valid JSON format like this:
{{
    "match_score": <number between 0 and 100>,
    "strengths": "<short summary of strengths, 1-2 sentences>",
    "weaknesses": "<short summary of gaps or weaknesses, 1-2 sentences>"
}}"""

    result = llm.invoke(prompt).content

    # Clean up in case the model adds extra formatting around the JSON
    result = result.strip()
    if result.startswith("```"):
        result = result.strip("`").replace("json", "", 1).strip()

    try:
        parsed = json.loads(result)
    except json.JSONDecodeError:
        # Fallback in case the model does not return valid JSON
        parsed = {"match_score": 0, "strengths": "N/A", "weaknesses": "Could not evaluate this resume."}

    return {
        "name": name,
        "match_score": parsed.get("match_score", 0),
        "strengths": parsed.get("strengths", ""),
        "weaknesses": parsed.get("weaknesses", "")
    }


def rank_resumes(uploaded_files, job_description):
    """Extracts, evaluates, and ranks all uploaded resumes in parallel"""

    # Step 1: Extract text from each PDF
    resumes = []
    for file in uploaded_files:
        text = extract_text_from_pdf(file)
        resumes.append({"name": file.name, "text": text})

    # Step 2: Evaluate all resumes in parallel for speed
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(
            executor.map(lambda r: evaluate_resume(r, job_description), resumes)
        )

    # Step 3: Sort by match score, highest first
    ranked_results = sorted(results, key=lambda x: x["match_score"], reverse=True)

    return ranked_results
