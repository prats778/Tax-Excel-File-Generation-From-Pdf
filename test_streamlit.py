import streamlit as st
from pdf_reader import pdfreader

def app():
    st.title('PDF to Tax Excel Converter')
    gst_data = {}
    pdf_names = {}
    # Initialize session state variables if not already present
    if 'files_ready' not in st.session_state:
        st.session_state['files_ready'] = False
    if 'download_files' not in st.session_state:
        st.session_state['download_files'] = []

    uploaded_files = st.file_uploader("Choose PDF files", accept_multiple_files=True, type='pdf')
    convert_button = st.button('Convert')

    if convert_button and uploaded_files:
        gst_data.clear()
        pdf_names.clear()
        st.session_state['download_files'] = []  # Reset/Clear previous files on new convert
        # Process each file
        for uploaded_file in uploaded_files:
            with open(uploaded_file.name, "wb") as f:
                f.write(uploaded_file.getbuffer())
            
            p = pdfreader(uploaded_file.name)  # Process the PDF file
            if p.gst_num in gst_data and p.year == gst_data[p.gst_num].year:
                gst_data[p.gst_num].update_data(p.periods,p.tax_values)
            else:
                gst_data[p.gst_num]=p
                pdf_names[p.gst_num]=uploaded_file.name

        unique_gst_list = gst_data.keys()
        for gst in unique_gst_list:
            gst_data[gst].export_data()
            st.session_state['download_files'].append((f"{gst}.xlsx", pdf_names[gst]))
        
        st.session_state['files_ready'] = True 

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
