import streamlit as st
import fitz
from utils import extract_text_from_pdf, generate_image_prompt, get_pollinations_url

# Page Config
st.set_page_config(layout="wide", page_title="BookChores")

# Sidebar
st.sidebar.title("Configuration")
api_key = st.sidebar.text_input("GEMINI_API_KEY", type="password")
uploaded_file = st.sidebar.file_uploader("Upload a PDF", type=["pdf"])

# Session State
if 'current_page_number' not in st.session_state:
    st.session_state.current_page_number = 0

# Main Layout
st.title("BookChores")

if uploaded_file and api_key:
    # Open doc to get total pages for navigation
    # Use getvalue() to handle Streamlit UploadedFile
    doc = fitz.open(stream=uploaded_file.getvalue(), filetype="pdf")
    total_pages = len(doc)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.header("Page Text")
        page_text = extract_text_from_pdf(uploaded_file, st.session_state.current_page_number)
        
        container = st.container(height=600)
        container.write(page_text)

    with col2:
        st.header("Visual Scene")
        if page_text and "Error" not in page_text:
            # Only generate if we have text
            if len(page_text.strip()) > 0:
                with st.spinner("Dreaming up the scene..."):
                    image_prompt = generate_image_prompt(page_text, api_key)
                    
                    if "Error" not in image_prompt:
                        image_url = get_pollinations_url(image_prompt)
                        st.image(image_url)
                        st.caption(f"Prompt: {image_prompt}")
                    else:
                        st.error(image_prompt)
            else:
                st.info("This page seems empty.")
        elif "Error" in page_text:
            st.error(page_text)

    # Navigation
    st.markdown("---")
    
    # Simple navigation
    c1, c2, c3 = st.columns([1, 1, 8])
    with c1:
        if st.button("Previous Page"):
            if st.session_state.current_page_number > 0:
                st.session_state.current_page_number -= 1
                st.rerun()
    with c2:
        if st.button("Next Page"):
            if st.session_state.current_page_number < total_pages - 1:
                st.session_state.current_page_number += 1
                st.rerun()

    st.sidebar.info(f"Page {st.session_state.current_page_number + 1} of {total_pages}")

else:
    st.info("Please upload a PDF and provide your Gemini API Key to start.")
