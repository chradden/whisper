import streamlit as st
import requests

# Define API endpoint and your OpenAI API key
API_ENDPOINT = "https://api.openai.com/v1/engines/whisper-1.0.0/completions"
API_KEY = "YOUR_API_KEY"

# Function to transcribe uploaded file using OpenAI Whisper API
def transcribe_file(file):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json",
    }

    # Read file content
    content = file.read()

    # Convert content to string
    content_str = content.decode("utf-8")

    # Prepare API request payload
    payload = {
        "prompt": "Transcribe the following audio:",
        "examples": [{"document": content_str}],
        "max_tokens": 2048,
    }

    # Send request to OpenAI API
    response = requests.post(API_ENDPOINT, headers=headers, json=payload)
    response.raise_for_status()

    # Parse and return the transcription result
    result = response.json()
    return result["choices"][0]["text"].strip()

# Streamlit app code
def main():
    st.title("Whisper Transcription App")
    st.write("Upload an audio file to transcribe it using OpenAI's Whisper API.")

    # Upload file
    file = st.file_uploader("Upload an audio file", type=["wav", "mp3"])

    if file is not None:
        if st.button("Transcribe"):
            try:
                # Transcribe the uploaded file
                transcription = transcribe_file(file)
                st.success("Transcription complete!")
                st.text_area("Transcription Result", transcription)
            except Exception as e:
                st.error(f"Transcription failed: {e}")

# Run the app
if __name__ == "__main__":
    main()
