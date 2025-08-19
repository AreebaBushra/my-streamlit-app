import streamlit as st
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# -------------------------------
# 🔹 Azure Setup (Replace with your details)
# -------------------------------
AZURE_ENDPOINT = "https://<your-resource-name>.cognitiveservices.azure.com/"
AZURE_KEY = "<your-key>"

# -------------------------------
# 🔹 Authenticate with Azure
# -------------------------------
def authenticate_client():
    credential = AzureKeyCredential(AZURE_KEY)
    client = TextAnalyticsClient(endpoint=AZURE_ENDPOINT, credential=credential)
    return client

client = authenticate_client()

# -------------------------------
# 🔹 Extract Key Phrases Function
# -------------------------------
def extract_key_phrases(text):
    try:
        response = client.extract_key_phrases([text])[0]
        if not response.is_error:
            return response.key_phrases
        else:
            return [f"Error: {response.error.code} - {response.error.message}"]
    except Exception as e:
        return [f"Exception: {str(e)}"]

# -------------------------------
# 🔹 Streamlit UI
# -------------------------------
st.set_page_config(page_title="📄➡️📌 Text Summarizer", page_icon="✨")

st.title("📄➡️📌 Text Summarizer (Key Phrase Extractor)")
st.write("Paste a long article or text below and extract **key phrases & main topics** using Azure Text Analytics.")

# Text input
user_text = st.text_area("✍️ Paste your text here:", height=200)

# Button to summarize
if st.button("Summarize"):
    if user_text.strip():
        with st.spinner("Analyzing text... ⏳"):
            phrases = extract_key_phrases(user_text)

        st.success("✨ Key Phrases Extracted:")
        for p in phrases:
            st.write(f"- {p}")
    else:
        st.warning("⚠️ Please enter some text before summarizing!")

# Footer
st.markdown("---")
st.caption("Built with ❤️ using Azure Cognitive Services + Streamlit")
