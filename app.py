import os
import streamlit as st
import csv
from src.helper import llm_pipeline

# Set up directories for static files
BASE_DOCS_FOLDER = 'static/docs/'
BASE_OUTPUT_FOLDER = 'static/output/'

if not os.path.isdir(BASE_DOCS_FOLDER):
    os.makedirs(BASE_DOCS_FOLDER)
if not os.path.isdir(BASE_OUTPUT_FOLDER):
    os.makedirs(BASE_OUTPUT_FOLDER)

st.title("PDF File Upload and QA Generation")
st.subheader("Upload a PDF file to generate questions and answers.")

def llm_pipeline_and_generate_csv(pdf_filename):
    # Process the file and generate questions and answers
    answer_generation_chain, ques_list = llm_pipeline(pdf_filename)
    
    # Define the output file path
    output_file = os.path.join(BASE_OUTPUT_FOLDER, "QA.csv")

    # Write questions and answers to CSV
    with open(output_file, "w", newline="", encoding="utf-8") as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Question", "Answer"])

        for question in ques_list:
            answer = answer_generation_chain.run(question)
            csv_writer.writerow([question, answer])

    return output_file, ques_list, answer_generation_chain

# File upload widget
pdf_file = st.file_uploader("Choose a PDF file", type="pdf")

if pdf_file:
    # Save uploaded file
    pdf_filename = os.path.join(BASE_DOCS_FOLDER, pdf_file.name)
    with open(pdf_filename, 'wb') as f:
        f.write(pdf_file.getbuffer())

    # Notify user that file is saved
    st.success(f"File '{pdf_file.name}' saved successfully!")

    # Call the LLM pipeline to generate questions and answers
    output_file, ques_list, answer_generation_chain = llm_pipeline_and_generate_csv(pdf_filename)

    # Display the generated questions and answers
    st.subheader("Generated Questions and Answers:")

    # Display questions and answers
    for i, question in enumerate(ques_list):
        answer = answer_generation_chain.run(question)
        st.write(f"**Q{i + 1}:** {question}")
        st.write(f"**Answer:** {answer}")

    # Provide a download button for the generated CSV
    if output_file:
        st.success("Questions and answers have been generated successfully!")
        with open(output_file, "rb") as file:
            st.download_button(
                label="Download QA CSV File",
                data=file,
                file_name="QA.csv",
                mime="text/csv"
            )
