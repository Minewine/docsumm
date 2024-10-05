# Docsumm

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [File Descriptions](#file-descriptions)
- [Next Steps](#next-steps)
- [Technical Next Steps for Vector Store Integration](#technical-next-steps-for-vector-store-integration)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Overview
Docsumm is a powerful document summarization tool designed to process various document formats, extract key insights, and present concise summaries. Built using Python, this project utilizes state-of-the-art Natural Language Processing (NLP) techniques to help users quickly glean important information from large documents.
Initally used to transcribe and summarize audio from meetings, lectures or podcasts, it was extended to include other standard document types.

## Features
- Supports multiple document formats: MP3, OPUS, PDF, EPUB, DOCX, HTML
- Summarizes documents to provide concise insights
- Extracts key points from text
- Easy integration with various libraries for NLP tasks
- User-friendly command-line interface

## Installation
To set up Docsumm on your local machine, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Minewine/docsumm.git
   cd docsumm
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To use the Docsumm tool, run the following command in your terminal:

```bash
python generate_summary_title_from_txt.py <path_to_your_document>
```

You can replace `<path_to_your_document>` with the path to the document you want to summarize. The tool will process the document and output a summary along with key points.

## Directory Structure
Here's a brief overview of the project structure:

```
docsumm/
├── config.py                 # Configuration settings for the application
├── doclib/                   # Directory containing documents to be processed
├── frontend_doc_query.py     # Interface for querying document summaries
├── generate_summary_title_from_txt.py  # Main script for generating summaries
├── logs/                     # Log files generated during processing
├── multi_format_file_processor.py  # Handles multiple document formats
├── requirements.txt          # List of dependencies
└── __pycache__/              # Cached bytecode files
```

## File Descriptions

- **`config.py`**: Contains configuration settings such as directory paths for input, output, and logging. It ensures that necessary directories are created if they do not exist.

- **`frontend_doc_query.py`**: This file provides a simple command-line interface for querying and displaying document summaries. Users can input queries and receive processed summaries.

- **`generate_summary_title_from_txt.py`**: The core script that handles the summarization of text documents. It leverages NLP models to generate concise summaries.

- **`multi_format_file_processor.py`**: This script processes various document formats, converting them to a uniform structure suitable for summarization.

- **`logs/`**: A directory where log files are stored, providing insights into the processing workflow and any errors encountered.

## Next Steps

As you explore and utilize the Docsumm project, consider the following next steps to enhance your experience and contribute to the development of this tool:

1. **Enhance Document Support**:
   - Explore adding support for additional document formats such as Markdown or plain text. 
   - Implement error handling for unsupported file types.

2. **Improve Summarization Techniques**:
   - Experiment with different NLP models to compare summarization results and improve accuracy.
   - Investigate fine-tuning existing models on specific document types to optimize performance.

3. **Integrate User Interface**:
   - Develop a graphical user interface (GUI) for easier interaction with the tool.
   - Consider using frameworks like Tkinter or PyQt to build the UI.

4. **Add More Features**:
   - Implement functionality for comparing multiple document summaries side by side.
   - Consider adding options for customizing summary lengths or key point extraction methods.

5. **Conduct User Testing**:
   - Share the tool with friends or colleagues and gather feedback on usability and features.
   - Use feedback to guide future enhancements and improvements.

6. **Documentation and Tutorials**:
   - Create detailed tutorials for new users to help them get started with the tool.
   - Consider writing blog posts or making videos that demonstrate how to use Docsumm effectively.

7. **Community Contributions**:
   - Encourage other developers to contribute by providing clear contribution guidelines.
   - Actively participate in discussions on GitHub issues to foster a collaborative environment.

8. **Monitor and Update**:
   - Stay updated with the latest developments in NLP and document processing.
   - Regularly review and update dependencies in `requirements.txt` to ensure compatibility and security.

## Technical Next Steps for Vector Store Integration

Vector store intergration:

1. **Choose a Vector Store**:
   - Evaluate and select a vector database based on your needs. Popular options include:
     - **ChromaDB**: Known for its ease of use and performance.
     - **Pinecone**: Offers managed vector database services with high scalability.
     - **Weaviate**: An open-source vector database that also supports graph-like queries.
     - **FAISS**: A library for efficient similarity search and clustering of dense vectors.

2. **Document Embedding**:
   - Implement functionality to convert documents into vector embeddings. You can use models like Sentence Transformers, OpenAI’s embeddings, or other transformer-based models to achieve this.
   - Store these embeddings in your selected vector database.

3. **Indexing Documents**:
   - Create an indexing mechanism for processed documents so they can be quickly retrieved based on vector similarity.
   - Ensure that each document's metadata (title, summary, etc.) is associated with its vector representation for easy lookup.

4. **Similarity Search Implementation**:
   - Develop functionality to search for similar documents using cosine similarity or other distance metrics on the vectors stored in the database.
   - Allow users to query for documents related to a specific summary or topic.

5. **Integration with Summarization**:
   - Use the vector store to find relevant documents that can be summarized together, improving the overall context of the summary.
   - Implement a feature that retrieves documents similar to the user’s query before summarization.

6. **Scalability and Performance Optimization**:
   - Optimize the performance of vector storage and retrieval to handle large datasets efficiently.
   - Experiment with different embedding sizes and indexing techniques to balance speed and accuracy.

7. **Continuous Updates**:
   - Implement mechanisms to update the vector database as new documents are added or existing documents are modified. This might include re-indexing or incrementally updating the vector embeddings.

8. **Monitoring and Evaluation**:
   - Set up monitoring to evaluate the performance of the vector search and summarization. Use metrics like retrieval accuracy and summary relevance.
   - Regularly test the integration to ensure it meets the expected performance benchmarks.

9. **User Interface Enhancements**:
   - If applicable, enhance the user interface to allow users to specify query vectors, visualize similarity results, or filter documents based on their embeddings.
   - Create intuitive ways for users to interact with the vector store and see results in a meaningful way.

10. **Documentation and Examples**:
    - Update the documentation to include details about the vector store integration, including setup instructions and usage examples.
    - Provide sample code snippets or tutorials demonstrating how to use the vector store for common tasks.


## Contributing
Contributions are welcome! If you have suggestions or improvements, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Commit your changes.
4. Push your branch to your fork.
5. Create a pull request detailing your changes. 

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgements
- [Ollama](https://ollama.com/) for the powerful LLM used in the summarization process.
- [LangChain](https://www.langchain.com/) for their robust tools for working with language models.
- All contributors and supporters who make this project possible!

