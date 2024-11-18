## Text_Summarizer

![cover](https://github.com/user-attachments/assets/5cfae579-f2ba-4801-b31d-7cc009365b5d)

## Objective

Designed and implemented a PDF summarization application using OpenAI GPT-4 for concise summaries and TF-IDF for keyword extraction. Integrated MongoDB for storing metadata, summaries and keywords. Delivered a user friendly Streamlit interface for efficient document processing and analysis.

## Principles

- Our application has to process single or multiple pdf which is uploaded by user.

- It should display the metadata to the user interface.

- It should process the text present in the pdf and give concise summary according to the length of text in pdf and It should also extract the keywords.

- It should calculate the processing time and display it to the user for measuring performance.

- It should save the metadata, extracted summary and keywords to the mongodb Atlas database which can be extracted later for analysis purpose.

## Setup Instructions

- Step 1: Install the packages mentioned in the requirement.txt (optional but recommended: create a virtual environment).
- Step 2: In Bash, type the code "streamlit run app.py" to run the user interface.
- step 3: Insert the pdf you like to summarize and the application will handle the rest.

## Procedure

- I have used streamlit for user interface, the file uploader function will get the pdf from user and give it to the pdf_processor.
- I have used pdfplumber to extract text from pdf and store it to varibale.
- I have displayed the file name and file size in the user interface.
- The text stored in the variable is cleaned properly like removel of urls, HTML tags, non-ascii characters, extra spaces, punctuation and convert all text into smaller case, giving it to the model.
- I have used OpenAI's Chatgpt-4 model to summarize the text and give consize summary.
- I have used Tf-idf vectorizer to extract important keywords from the processed text and give it to user.
- I have used time library to calculate the execution time of all the process and display it to the user.
- Parallely, The metadata of the pdf like id, file name, file path and file size and the processed summary and extracted keywords will be automatically saved in Mongodb Atlas (Cloud). 

## Snapshot

![Screenshot 2024-11-18 215425](https://github.com/user-attachments/assets/0b8348ba-f221-4f4f-bef1-6fd1d828a9cb)
