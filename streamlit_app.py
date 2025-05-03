from google import genai
from google.genai import types
import pathlib
import httpx
import streamlit as st
import json
import os
from dotenv import load_dotenv
load_dotenv()

if "pdf_bytes" not in st.session_state:
    st.session_state["pdf_bytes"] = None

st.title("Enhance Resume")
client = genai.Client(api_key=os.getenv("GENAI_API_KEY"))

#  Retrieve and encode the PDF byte
uploaded_file = st.file_uploader("Upload your resume (PDF only)", type=["pdf"])

# Store uploaded file in session state to avoid re-uploading
if uploaded_file:
    st.session_state["pdf_bytes"] = uploaded_file.getvalue()
#  filepath.write_bytes(httpx.get(doc_url).content)
if st.session_state["pdf_bytes"] is not None:
    prompt = """You are an expert career advisor and resume reviewer with deep knowledge of hiring trends across multiple industries. Your task is to critically analyze the provided resume and offer a detailed, constructive, and professional review. Your analysis should help the candidate significantly improve their chances of securing job interviews.
                Understand the target job market and the specific role the candidate is applying for. The resume may be tailored for a specific job or industry, so consider this context in your analysis.
                ---

                Analyze the resume using the following criteria:

                    1. Structure & Formatting
                - Is the resume well-organized and easy to navigate?
                - Are sections clearly labeled (e.g., Summary, Experience, Education, Skills)?
                - Does the layout make effective use of white space, fonts, and bullet points?
                - Are formatting elements (e.g., bold, italics, dates) used consistently?

                    2. Clarity & Language
                - Is the wording clear, concise, and professional?
                - Are action verbs used to begin bullet points?
                - Is there any jargon, vague wording, or redundancy that should be revised?
                - Are grammar, punctuation, and spelling correct throughout?

                    3. Content Relevance
                - Is all content directly relevant to the job market or targeted roles?
                - Does the resume include unnecessary or outdated information?
                - Are technical and soft skills listed appropriately?
                - Is the work experience quantified with metrics where possible?

                    4. Effectiveness & Impact
                - Does the resume showcase the candidate’s most impressive accomplishments?
                - Are key achievements highlighted and easy to spot?
                - Does it demonstrate growth, leadership, or problem-solving capabilities?
                - Does the resume present a strong value proposition to potential employers?

                    5. Tailoring for Job Roles or Industries
                - Based on the resume content, suggest which industries or roles it is best suited for.
                - Recommend changes to better tailor the resume to specific job types (e.g., software engineer, data analyst, cybersecurity specialist).
                - Provide suggestions for how to align the resume with job descriptions from real-world listings (e.g., using keywords from relevant postings).

                ---

                Provide actionable suggestions for improvement, including:
                - Rewriting vague or passive phrases to sound more impactful.
                - Highlighting or reordering achievements that deserve more attention.
                - Replacing or removing irrelevant content.
                - Formatting tips for improved readability and visual appeal.
                - Suggestions for adding missing but relevant sections (e.g., Projects, Certifications).
                - Tips for tailoring the resume toward a specific industry or company.

                ---

                Output Format:
                Provide your review and suggestions with example changes in the following structure:

                1. Summary of Overall Impression
                2. Detailed Analysis by Section (Structure, Clarity, Content, Effectiveness, Tailoring)
                3. Constructive Suggestions for Improvement
                4. Sample Rewrite Snippets (Rewrite 1–2 weak bullet points or summary lines as examples)
                5. Optional Industry-Specific Tailoring Advice

                ---

                Tone: Professional, encouraging, specific, and focused on helping the candidate succeed.

                """
    response = client.models.generate_content(
    model="gemini-1.5-pro",
    contents=[
        types.Part.from_bytes(
            data=st.session_state["pdf_bytes"],
            mime_type='application/pdf',
        ),
        prompt])
    
    output = response.text
    st.write(output)
