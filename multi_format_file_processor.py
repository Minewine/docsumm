import os
import json
import logging
import shutil
import time
from pathlib import Path
from typing import Union, List
import asyncio
from tenacity import retry, stop_after_attempt, wait_fixed
from tqdm.asyncio import tqdm

from faster_whisper import WhisperModel
import fitz  # PyMuPDF for PDF processing
import ebooklib
from ebooklib import epub
from bs4 import BeautifulSoup
from docx import Document
import requests
from requests.exceptions import RequestException

import config

# Set up logging
logging.basicConfig(level=config.LOG_LEVEL, format=config.LOG_FORMAT,
                    filename=config.LOG_FILE, filemode='a')
logger = logging.getLogger(__name__)

# Decorator for logging duration of processes
def log_duration(func):
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        duration = time.time() - start_time
        logger.info(f"{func.__name__} took {duration:.2f} seconds")
        return result
    return wrapper

class AudioTranscriber:
    def __init__(self, model_size="small", device="cpu", compute_type="float32"):
        self.model = WhisperModel(model_size, device=device, compute_type=compute_type)
        logger.info(f"Initialized AudioTranscriber with model: {model_size}")

    def transcribe(self, file_path: Path) -> str:
        logger.info(f"Transcribing audio file: {file_path}")
        result_generator, _ = self.model.transcribe(str(file_path))
        return ''.join([segment.text for segment in result_generator])

class PDFProcessor:
    @staticmethod
    def extract_text(file_path: Path) -> str:
        logger.info(f"Extracting text from PDF: {file_path}")
        with fitz.open(file_path) as doc:
            return "\n".join([page.get_text() for page in doc])

class EPUBProcessor:
    @staticmethod
    def extract_text(file_path: Path) -> str:
        logger.info(f"Extracting text from EPUB: {file_path}")
        book = epub.read_epub(file_path)
        texts = []
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.content, 'html.parser')
            texts.append(soup.get_text())
        return "\n".join(texts)

class DOCXProcessor:
    @staticmethod
    def extract_text(file_path: Path) -> str:
        logger.info(f"Extracting text from DOCX: {file_path}")
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

class WebPageProcessor:
    @staticmethod
    def extract_text(url: str) -> str:
        logger.info(f"Fetching and extracting text from webpage: {url}")
        try:
            response = requests.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup.get_text()
        except RequestException as e:
            logger.error(f"Failed to fetch webpage {url}: {e}")
            raise

class FileProcessor:
    def __init__(self):
        self.audio_transcriber = AudioTranscriber()
        self.process_map = {
            '.mp3': self.audio_transcriber.transcribe,
            '.wav': self.audio_transcriber.transcribe,
            '.opus': self.audio_transcriber.transcribe,
            '.pdf': PDFProcessor.extract_text,
            '.epub': EPUBProcessor.extract_text,
            '.docx': DOCXProcessor.extract_text
        } 

    @log_duration
    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    async def process_file(self, file_path: Path) -> str:
        extension = file_path.suffix.lower()
        if extension in self.process_map:
            return await asyncio.to_thread(self.process_map[extension], file_path)
        elif file_path.suffix.lower() == '.url':  # For URLs/webpages
            with file_path.open('r') as url_file:
                url = url_file.read().strip()
                return await asyncio.to_thread(WebPageProcessor.extract_text, url)
        else:
            raise ValueError(f"Unsupported file type: {extension}")

class OutputManager:
    @staticmethod
    def save_output(content: str, output_dir: Path, filename: str):
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"{filename}.txt"
        output_file.write_text(content)
        logger.info(f"Output saved to {output_file}")

        metadata_file = output_dir / f"{filename}_metadata.json"
        with metadata_file.open('w') as meta_file:
            json.dump({'text': content}, meta_file, indent=2)
        logger.info(f"Metadata saved to {metadata_file}")

@log_duration
async def process_files(input_files: Union[Path, List[Path]]):
    processor = FileProcessor()
    if isinstance(input_files, Path):
        input_files = [input_files]

    tasks = []
    for file_path in input_files:
        try:
            logger.info(f"Processing file: {file_path}")
            output_dir = config.OUTPUT_DIR / file_path.stem
            if output_dir.exists():
                logger.info(f"Directory {output_dir} already exists. Deleting it.")
                shutil.rmtree(output_dir)

            tasks.append(processor.process_file(file_path))
        except Exception as e:
            logger.error(f"An error occurred while preparing {file_path}: {e}")

    results = await asyncio.gather(*tasks)
    for file_path, content in zip(input_files, results):
        output_dir = config.OUTPUT_DIR / file_path.stem
        OutputManager.save_output(content, output_dir, file_path.stem)
        logger.info(f"Processing complete for {file_path}")

async def main():
    input_files = [config.INPUT_FILE_TO_TRANSCRIBE]
    if config.INPUT_FILE_TO_TRANSCRIBE.is_dir():
        input_files = list(config.INPUT_FILE_TO_TRANSCRIBE.glob('*'))

    await process_files(input_files)

if __name__ == "__main__":
    if config.DEBUG:
        print("Running in DEBUG mode")
        logging.getLogger().setLevel(logging.DEBUG)
    
    asyncio.run(main())
