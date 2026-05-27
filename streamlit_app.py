import streamlit as st
import requests
import time
import json

BASE_URL = "http://127.0.0.1:5000"

st.set_page_config(page_title="Transcript Ingestor", page_icon="📝")

st.title("📝 Transcript Ingestion UI")
st.markdown("""
This tool allows you to upload conversation transcripts, process them using AI embeddings, 
and store them in a vector database (ChromaDB) for searching.
""")

tabs = st.tabs(["1. Upload & Ingest", "2. Check Status", "3. Ask Questions"])

with tabs[0]:
    st.header("Upload Transcript")
    uploaded_file = st.file_uploader("Choose a JSON transcript file", type=["json"])
    
    if uploaded_file is not None:
        if st.button("Step 1: Upload to Server"):
            files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "application/json")}
            try:
                response = requests.post(f"{BASE_URL}/upload", files=files)
                if response.status_code == 200:
                    st.session_state['transcript_url'] = response.json().get("url")
                    st.success(f"File uploaded successfully!")
                    st.info(f"Internal URL: {st.session_state['transcript_url']}")
                else:
                    st.error(f"Upload failed: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

    st.divider()

    st.header("Start Ingestion")
    t_id = st.text_input("Transcript ID (Unique Name)", value="transcript_001")
    t_url = st.text_input("Transcript URL", value=st.session_state.get('transcript_url', ""))

    if st.button("Step 2: Start Ingesting"):
        if not t_id or not t_url:
            st.warning("Please provide both an ID and a URL.")
        else:
            payload = {
                "transcript_id": t_id,
                "transcript_url": t_url,
                "ttl": 3600
            }
            try:
                response = requests.post(f"{BASE_URL}/ingest", data=payload)
                if response.status_code == 200:
                    st.session_state['last_job_id'] = t_id
                    st.success(f"Job queued successfully for ID: {t_id}")
                    st.balloons()
                else:
                    st.error(f"Ingestion failed: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

with tabs[1]:
    st.header("Monitor Progress")
    job_id_to_check = st.text_input("Enter Job ID to check status", value=st.session_state.get('last_job_id', ""))
    
    if st.button("Check Status"):
        if job_id_to_check:
            try:
                response = requests.get(f"{BASE_URL}/status/{job_id_to_check}")
                if response.status_code == 200:
                    data = response.json()
                    status = data.get("status", "UNKNOWN")
                    
                    if status == "COMPLETED":
                        st.success(f"Status: {status}")
                    elif "FAILED" in status:
                        st.error(f"Status: {status}")
                    else:
                        st.warning(f"Status: {status}")
                    
                    st.json(data)
                else:
                    st.error("Job not found or server error.")
            except Exception as e:
                st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a Job ID.")

with tabs[2]:
    st.header("Query Ingested Transcript")
    q_id = st.text_input("Transcript ID to Query", value=st.session_state.get('last_job_id', ""))
    question = st.text_area("Enter your question (e.g., 'What was the customer complaining about?')")

    if st.button("Get Answer"):
        if not q_id or not question:
            st.warning("Please provide both Transcript ID and a question.")
        else:
            payload = {
                "transcript_id": q_id,
                "question": question
            }
            try:
                response = requests.post(f"{BASE_URL}/query", data=payload)
                if response.status_code == 200:
                    results = response.json()
                    documents = results.get("documents", [[]])[0]
                    
                    if documents:
                        st.subheader("📝 Summary of Findings")
                        # Combine the top chunks into a readable paragraph or list
                        full_context = "\n\n".join(documents)
                        st.write("Based on the transcript, here are the most relevant parts:")
                        for doc in documents:
                            st.info(f"“...{doc}...”")
                    else:
                        st.warning("No relevant information found for that ID.")
                else:
                    st.error(f"Query failed: {response.text}")
            except Exception as e:
                st.error(f"Connection error: {e}")

st.sidebar.markdown("### System Status")
try:
    requests.get(BASE_URL)
    st.sidebar.success("Backend: Online")
except:
    st.sidebar.error("Backend: Offline (Run python run.py)")
