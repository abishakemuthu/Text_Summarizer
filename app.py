import os
import tempfile
import streamlit as st
import openai
import pdfplumber
import re
import string
from pymongo import MongoClient
import urllib.parse
from sklearn.feature_extraction.text import TfidfVectorizer
import time
from dotenv import load_dotenv
load_dotenv()

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# MongoDB credentials
username = urllib.parse.quote_plus("Abishake")
password = urllib.parse.quote_plus("Abi4@mongodb")
#MONGO_URI = f"mongodb+srv://{MONGO_USERNAME}:{MONGO_PASSWORD}@task.rtek8.mongodb.net/?retryWrites=true&w=majority&appName=task"

# Streamlit UI
st.title("PDF Summarizer 📖")
st.subheader("Upload PDF files to summarize and extract keywords.")

# File uploader
files = st.file_uploader("Upload PDF files", type=["pdf"], accept_multiple_files=True)

def connect_to_mongo():
    # Use the encoded username and password in the connection string
    connection_string = (
        f"mongodb+srv://{username}:{password}@task.rtek8.mongodb.net/"
        "?retryWrites=true&w=majority&appName=task"
    )
    client = MongoClient(connection_string)
    db = client["wasserstoff"]
    collection = db["task"]
    return collection

# Store summary and keywords in MongoDB
def store_summary_to_db(file_name, file_path, file_size, summary, keywords):
    collection = connect_to_mongo()
    document = {
        "file_name": file_name,
        "file_path": file_path,
        "file_size": file_size,
        "summary": summary,
        "keywords": keywords,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    collection.insert_one(document)

# Extract text from PDF
def extract_text_from_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = ''.join([page.extract_text() for page in pdf.pages])
    return text

# Preprocess text
def preprocess_text(text):
    text = re.sub(r"http\S+|www\S+|https\S+", "", text, flags=re.MULTILINE)  # Remove URLs
    text = re.sub(r"<.*?>", "", text)  # Remove HTML tags
    text = re.sub(r"[^\x00-\x7f]", r"", text)  # Remove non-ASCII characters
    text = text.lower()  # Convert to lowercase
    text = text.translate(str.maketrans("", "", string.punctuation))  # Remove punctuation
    text = re.sub(r"\s+", " ", text).strip()  # Remove extra spaces
    return text

# Extract keywords using TF-IDF
def extract_keywords(text):
    vectorizer = TfidfVectorizer(stop_words="english", max_features=10)
    X = vectorizer.fit_transform([text])
    keywords = vectorizer.get_feature_names_out()
    return list(keywords)

def summarize(text):
    # Generate a summary using OpenAI's ChatCompletion API
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes documents."},
            {"role": "user", "content": f"Summarize the following text:\n\n{text}"}
        ],
        temperature=0.7,
    )
    summary = response["choices"][0]["message"]["content"]
    return summary

# Measure performance
def measure_total_performance(func, *args):
    start_time = time.time()
    result = func(*args)
    elapsed_time = time.time() - start_time
    return result, elapsed_time

# Process document
if files:
    for file in files:
        file_name = file.name
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(file.read())
            temp_file_path = tmp_file.name

        st.write(f"**File Name:** {file_name}")
        st.write(f"**File Size:** {round(os.path.getsize(temp_file_path) / 1048576, 2)} MB")

        try:
            def process_document(file_name, temp_file_path):
                text = extract_text_from_pdf(temp_file_path)
                processed_text = preprocess_text(text)
                summary = summarize(processed_text)
                keywords = extract_keywords(processed_text)
                store_summary_to_db(file_name, temp_file_path, os.path.getsize(temp_file_path), summary, keywords)
                return summary, keywords

            (summary, keywords), total_time = measure_total_performance(process_document, file_name, temp_file_path)

            st.write("### Summary:")
            st.write(summary)
            st.write("### Keywords:")
            st.write(", ".join(keywords))
            st.write(f"**Total Processing Time:** {round(total_time, 2)} seconds")

        except Exception as e:
            st.error(f"Error processing {file_name}: {str(e)}")

        os.remove(temp_file_path)