import streamlit as st
import cohere
from io import StringIO

# Cohere API key
COHERE_API_KEY = "gLeXvv76gOu9qF4lt6F6aqLl6Y3OO4VERjVdWUwa"

# Initialize Cohere client
co = cohere.Client(COHERE_API_KEY)

# Function to translate text using Cohere
def translate_text(text, target_lang='ar'):
    response = co.generate(
        model='command-r-plus',  # Updated to the correct model name
        prompt=f"Translate the following text to {target_lang}:\n\n{text}",
        max_tokens=500
    )
    return response.generations[0].text.strip()

# Function to split text into smaller chunks
def split_text(text, max_tokens=500):
    sentences = text.split('.')
    chunks = []
    chunk = ''
    for sentence in sentences:
        if len(chunk.split()) + len(sentence.split()) <= max_tokens:
            chunk += sentence + '.'
        else:
            chunks.append(chunk)
            chunk = sentence + '.'
    if chunk:
        chunks.append(chunk)
    return chunks

# Streamlit user interface
def main():
    st.set_page_config(page_title="Document Translator", layout="centered")
    
    st.markdown(
        """
        <style>
        body {
            direction: rtl;
        }
        .css-1d391kg {
            direction: rtl;
        }
        .stButton button {
            background-color: #4CAF50;
            color: white;
            font-size: 18px;
            padding: 10px 24px;
            border: none;
            cursor: pointer;
        }
        .stButton button:hover {
            background-color: #45a049;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    st.title("ترجمة المستند إلى العربية")
    st.write("قم بتحميل ملف نصي وترجمة محتواه إلى اللغة العربية.")
    
    uploaded_file = st.file_uploader("اختر ملف نصي...", type="txt")
    
    if uploaded_file is not None:
        # Read the file
        stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
        text = stringio.read()
        
        st.write("### النص الأصلي")
        st.write(text)
        
        if st.button("ترجمة إلى العربية"):
            with st.spinner("جار الترجمة..."):
                chunks = split_text(text)
                translated_chunks = []
                progress_bar = st.progress(0)
                
                for i, chunk in enumerate(chunks):
                    translated_chunk = translate_text(chunk)
                    translated_chunks.append(translated_chunk)
                    progress_bar.progress((i + 1) / len(chunks))
                
                translated_text = ''.join(translated_chunks)
                
                st.write("### النص المترجم")
                st.write(translated_text)
                st.download_button("تنزيل النص المترجم", translated_text, file_name="translated.txt")

if __name__ == "__main__":
    main()
