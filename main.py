import asyncio
import tempfile

import streamlit as st
from langchain_community.document_loaders import PyPDFLoader

from graph.analyze_graph import app

from dotenv import  load_dotenv
load_dotenv()
try:
    st.set_page_config(page_title="AI Resume Critiquer", page_icon="📃", layout="centered")

    st.title("AI Resume Critiquer")
    st.markdown("Upload your resume and get AI-powered feedback tailored to your needs!")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    job_role = st.text_input("Enter the job role you're taregtting")
    analyze = st.button("Analyze Resume")

    if analyze:
        if not uploaded_file:
            st.warning("Please upload your resume first.")
        if not job_role:
            st.warning("Please enter your job role first.")
        else:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as tmp:
                tmp.write(uploaded_file.getvalue())
                file_path = tmp.name
            with st.spinner("Analyzing..."):
                response = asyncio.run(app.ainvoke({"file_path": file_path,"documents":PyPDFLoader(file_path).load(), "job_role": job_role}))
            st.markdown("### Analysis Results")
            st.markdown(response["generation"])

except Exception as e:
    st.error(f"An error occured: {str(e)}")