import streamlit as st
import requests
import PyPDF2
# ---------------- CONFIG ---------------- #
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
    "Content-Type": "application/json"
}
MODEL = "meta-llama/llama-3-8b-instruct"
# ---------------- FUNCTIONS ---------------- #
def query(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        result = response.json()
        if "error" in result:
            return {"error": result["error"]["message"]}
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return {"error": str(e)}
def extract_text_from_pdf(file):
    reader = PyPDF2.PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text
def analyze_resume(text):
    text = text[:1500]
    summary = query(f"Summarize this PDF:\n{text}")
    # skills = query(f"Extract key skills from this resume:\n{text}")
    # suggestions = query(f"Give improvement suggestions for this resume:\n{text}")
    # return summary, skills, suggestions
    return summary
# ---------------- UI ---------------- #
st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄")
st.title("📄 AI PDF Analyzer")
st.markdown("Upload your PDF and get smart insights")
uploaded_file = st.file_uploader("Upload PDF", type=["txt", "pdf"])
if st.button("🚀 Analyze PDF"):
    if uploaded_file is None:
        st.warning("Please upload a PDF first!")
    else:
        with st.spinner("Analyzing..."):
            if uploaded_file.type == "application/pdf":
                text = extract_text_from_pdf(uploaded_file)
            else:
                text = uploaded_file.read().decode("utf-8")
            summary = analyze_resume(text)
            st.subheader("📄 Summary")
            st.write(summary)
            # st.subheader("💡 Skills")
            # st.write(skills)

            # st.subheader("📊 Suggestions")
            # st.write(suggestions)

            st.success("✅ Analysis complete!")