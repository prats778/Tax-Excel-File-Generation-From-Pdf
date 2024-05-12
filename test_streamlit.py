import streamlit as st
from pdf_reader import pdfreader

# # Define the text extraction and processing functions here (omitted for brevity)

def app():
    st.title('PDF to Tax Excel Converter')

    # File uploader allows user to add multiple files
    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type='pdf')
    convert_button = st.button('Convert')
    files = []

    if convert_button and uploaded_files:
        # Process each file
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            p=pdfreader(uploaded_file.name)
            files.append(p.gst_num)

        # Download button
        for i in range(len(files)):
            with open(f"{files[i]}.xlsx", "rb") as file:
                btn = st.download_button(
                        label="Download Excel",
                        data=file,
                        file_name=f"{files[i]}.xlsx",
                        mime="application/vnd.ms-excel"
                    )

if __name__ == "__main__":
    app()