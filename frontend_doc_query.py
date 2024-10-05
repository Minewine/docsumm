import streamlit as st
import asyncio
import tempfile
from pathlib import Path
import os

from multi_format_file_processor import FileProcessor, OutputManager, config
from generate_summary_title_from_txt import FileSummarizer

st.set_page_config(page_title="File Processor and Summarizer", page_icon="📄")

st.title("File Processor and Summarizer")

# Function to get list of processed files
def get_processed_files():
    processed_files = []
    for item in config.OUTPUT_DIR.iterdir():
        if item.is_dir():
            metadata_file = item / f"{item.name}_metadata.json"
            if metadata_file.exists():
                processed_files.append(item.name)
    return processed_files

# Function to display summary
def display_summary(title, summary):
    st.markdown("### Summary")
    st.markdown(f"**Title:** {title}")
    st.markdown(f"**Summary:** {summary}")

# Initialize session state variables
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

if 'file_processed' not in st.session_state:
    st.session_state['file_processed'] = False

# Main content area for file upload and processing
uploaded_file = st.file_uploader("Choose a file to process", type=['mp3', 'wav', 'opus', 'pdf', 'epub', 'docx', 'url'])

# If a new file is uploaded and no file has been processed yet
if uploaded_file is not None and not st.session_state['file_processed']:
    st.session_state['uploaded_file'] = uploaded_file  # Store the uploaded file in session state
    st.write("File uploaded successfully!")
    
    # Create a temporary directory to store the uploaded file
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_path = Path(tmpdirname) / uploaded_file.name
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        st.write("Processing file...")
        
        # Create instances of necessary classes
        file_processor = FileProcessor()
        file_summarizer = FileSummarizer()
        
        # Process the file
        async def process_and_summarize_file():
            try:
                # Process the file
                content = await file_processor.process_file(temp_path)
                
                # Save the output
                output_dir = config.OUTPUT_DIR / temp_path.stem
                OutputManager.save_output(content, output_dir, temp_path.stem)
                
                # Generate summary and title
                processed_file_path = output_dir / f"{temp_path.stem}.txt"
                title, summary = await file_summarizer.get_file_topics(processed_file_path)
                
                # Save summary and title
                summary_file = output_dir / f"{temp_path.stem}_summary.txt"
                with open(summary_file, 'w', encoding=config.DEFAULT_ENCODING) as f:
                    f.write(f"Title: {title}\n\nSummary: {summary}")
                
                return content, processed_file_path, title, summary, summary_file
            
            except Exception as e:
                st.error(f"An error occurred while processing the file: {str(e)}")
                return None, None, None, None, None

        # Run the async function
        content, processed_file_path, title, summary, summary_file = asyncio.run(process_and_summarize_file())
        
        if content is not None:
            # Display success message and link to original file
            st.success("File processed and summarized successfully!")
            st.markdown(f"[View Original Processed File]({processed_file_path})")
            
            # Display the summary
            display_summary(title, summary)

            # Mark the file as processed
            st.session_state['file_processed'] = True

# View Processed Files section is always visible
st.write("---")
st.header("View Processed Files")

processed_files = get_processed_files()
if processed_files:
    selected_file = st.selectbox("Select a processed file", [""] + processed_files)

    if selected_file:
        selected_dir = config.OUTPUT_DIR / selected_file
        metadata_file = selected_dir / f"{selected_file}_metadata.json"
        processed_file = selected_dir / f"{selected_file}.txt"
        summary_file = selected_dir / f"{selected_file}_summary.txt"
        
        if metadata_file.exists() and processed_file.exists():
            st.markdown(f"[View Original Processed File]({processed_file})")
            
            if summary_file.exists():
                with open(summary_file, 'r') as f:
                    summary_content = f.read()
                title = summary_content.split('\n')[0].replace('Title: ', '')
                summary = '\n'.join(summary_content.split('\n')[2:])
                display_summary(title, summary)
            
        else:
            st.error(f"Could not find processed file or metadata for {selected_file}")
else:
    st.info("No processed files available.")

# Clear the uploaded file from session state if processed
if st.session_state['file_processed']:
    if st.button("Clear Uploaded File"):
        st.session_state['uploaded_file'] = None  # Clear the uploaded file
        st.session_state['file_processed'] = False  # Reset processed flag
        st.success("Uploaded file cleared.")
