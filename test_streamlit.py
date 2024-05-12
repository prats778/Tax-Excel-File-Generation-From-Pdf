import streamlit as st
from pdf_reader import pdfreader

# # Define the text extraction and processing functions here (omitted for brevity)

def app():
    st.title('PDF to Tax Excel Converter')

    # Initialize session state variables if not already present
    if 'files_ready' not in st.session_state:
        st.session_state['files_ready'] = False
    if 'download_files' not in st.session_state:
        st.session_state['download_files'] = []

    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type='pdf')
    convert_button = st.button('Convert')

    if convert_button and uploaded_files:
        st.session_state['download_files'] = []  # Reset/Clear previous files on new convert
        # Process each file
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            # Assuming 'pdfreader' is a function you've defined elsewhere to process your PDFs
            p = pdfreader(uploaded_file.name)  # Process the PDF file
            # Store the file data and filename for download
            st.session_state['download_files'].append((f"{p.gst_num}.xlsx", uploaded_file.name))
        
        st.session_state['files_ready'] = True  # Indicate files are ready for download

    # Generate download buttons based on session state
    if st.session_state['files_ready']:
        for file_data, orig_filename in st.session_state['download_files']:
            with open(file_data, "rb") as file:
                btn = st.download_button(
                        label=f"Download Excel for {orig_filename}",
                        data=file,
                        file_name=file_data,
                        mime="application/vnd.ms-excel"
                    )


if __name__ == "__main__":
    app()
