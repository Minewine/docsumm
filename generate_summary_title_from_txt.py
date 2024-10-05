import asyncio
import logging
from pathlib import Path
from typing import List, Tuple

from langchain_community.chat_models import ChatOllama
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.document_loaders import TextLoader
from langchain_core.runnables import RunnableSequence

import config

# Set up logging
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT,
                    filename=config.LOG_FILE, filemode='a')
logger = logging.getLogger(__name__)

class TextProcessor:
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean text by removing extra whitespaces and non-ASCII characters."""
        import re
        logger.debug("Cleaning text...")
        text = re.sub(r'\s+', ' ', text)
        text = re.sub(r'[^\x00-\x7F]+', ' ', text)
        return text.strip()

class FileHandler:
    @staticmethod
    def extract_text_from_txt(file_path: Path) -> str:
        """Extract text from a text file with error handling."""
        try:
            logger.info(f"Extracting text from {file_path}")
            return file_path.read_text(encoding=config.DEFAULT_ENCODING)
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            return ""

class SummaryGenerator:
    def __init__(self):
        self.llm = ChatOllama(model=config.LLM_MODEL, temperature=config.LLM_TEMPERATURE)
        logger.info(f"Initialized SummaryGenerator with model: {config.LLM_MODEL}")

    def generate_summary(self, documents: List[str]) -> str:
        """Generate a summary from the given documents."""
        logger.info("Generating summary...")
        prompt = ChatPromptTemplate.from_messages([
            ("system", f"Write a concise summary of the following in {config.MAX_SUMMARY_LENGTH} words or less:\n\n{{context}}")
        ])
        chain = create_stuff_documents_chain(self.llm, prompt)
        return chain.invoke({"context": documents})

    def generate_title(self, summary: str) -> str:
        """Generate a title based on the summary."""
        logger.info("Generating title...")
        title_prompt = ChatPromptTemplate.from_messages([
            ("system", f"Generate one short and concise title ({config.MIN_TITLE_WORDS}-{config.MAX_TITLE_WORDS} words) for the following summary:\n\n{{summary}}.")
        ])
        title_chain = RunnableSequence(title_prompt | self.llm)
        return title_chain.invoke({"summary": summary}).content.strip()

class FileSummarizer:
    def __init__(self):
        self.summary_generator = SummaryGenerator()

    async def get_file_topics(self, file_path: Path) -> Tuple[str, str]:
        """Process a file and return its title and summary."""
        if not file_path.exists():
            logger.error(f"File not found: {file_path}")
            return "File Not Found", "The specified file could not be located."

        try:
            loader = TextLoader(str(file_path), encoding=config.DEFAULT_ENCODING)
            documents = loader.load()
            
            summary = await asyncio.to_thread(self.summary_generator.generate_summary, documents)
            title = await asyncio.to_thread(self.summary_generator.generate_title, summary)
            
            logger.info(f"Successfully processed file: {file_path}")
            return title, summary
        except Exception as e:
            logger.error(f"Error processing file {file_path}: {e}")
            return "Error", f"An error occurred while processing the file: {str(e)}"

async def main():
    summarizer = FileSummarizer()

    # Process the specific file
    file_path = config.INPUT_FILE
    title, summary = await summarizer.get_file_topics(file_path)
    print(f"File Summary:")
    print(f"File: {file_path}")
    print(f"Title: {title}")
    print(f"Summary: {summary}\n")

    # Save results to output directory
    output_file = config.OUTPUT_DIR / f"{file_path.stem}_summary.txt"
    with open(output_file, 'w', encoding=config.DEFAULT_ENCODING) as f:
        f.write(f"Title: {title}\n\nSummary: {summary}")

    print(f"Summary saved to: {output_file}")

if __name__ == "__main__":
    if config.DEBUG:
        print("Running in DEBUG mode")
        logging.getLogger().setLevel(logging.DEBUG)
    
    asyncio.run(main())