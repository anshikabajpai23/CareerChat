import streamlit as st
import requests
import json
from pathlib import Path
from backend.parse_resume import parse_resume
import time

def home_page():
    UPLOADS_DIR = Path(__file__).parent / "pages" / "uploads"
    st.session_state.uploads_dir = UPLOADS_DIR
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    open_ai_key = st.text_input("Enter your OpenAI API key: ", type="password", key="open_ai_key")
    resume = st.file_uploader("Upload your resume", type=["pdf"])
    
    if resume:
        # ---------- UI elements ----------
        progress_bar = st.progress(0)
        status_text = st.empty()

        # ---------- Step 1: Save file ----------
        status_text.text("Saving resume...")
        pdf_path = UPLOADS_DIR / resume.name
        with open(pdf_path, "wb") as f:
            f.write(resume.getbuffer())
    
        st.write(f"**File name:** {resume.name}")
        st.write(f"**Size (bytes):** {resume.size}")
        st.write(f"**Saved to:** {pdf_path}")

        # ---------- Step 2: Parse resume ----------
        status_text.text("Parsing resume with AI...")
        progress_bar.progress(40)
    
        # Call your backend function
        result = parse_resume(open_ai_key,str(pdf_path))
        # st.write("### Review and Edit JSON")

        progress_bar.progress(75)
        time.sleep(0.3)

        # ---------- Step 3: Prepare JSON ----------
        status_text.text("Preparing editable JSON...")
        progress_bar.progress(90)


        if "editable_json" not in st.session_state:
            st.session_state.editable_json = json.dumps(result, indent=2, ensure_ascii=False)

        progress_bar.progress(100)
        status_text.text("✅ Done!")

        # ---------- JSON Editor ----------
        st.write("### Review and Edit JSON")

        edited_text = st.text_area(
            "Edit the JSON below:",
            value=st.session_state.editable_json,
            height=350,
            key="json_editor"
        )

        col1, col2 = st.columns([1,1])
        st.info('💡 Click **Apply Changes** to save profile info')

        with col1:
            if st.button("Apply Changes"):
                try:
                    parsed = json.loads(edited_text)
                    st.session_state.editable_json = json.dumps(parsed, indent=2, ensure_ascii=False)
                    OUTPUT_PATH = UPLOADS_DIR / "payload.json"
                    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
                        json.dump(parsed, f, indent=2, ensure_ascii=False)
        
                    st.success(f"JSON updated and saved to: {UPLOADS_DIR}")
                except Exception as e:
                    st.error(f"Invalid JSON: {e}")
        with col2:
            st.download_button(
                "Download JSON",
                data=st.session_state.editable_json,
                file_name="resume_payload.json",
                mime="application/json"
            )

    st.success(f"Saved to {UPLOADS_DIR}")