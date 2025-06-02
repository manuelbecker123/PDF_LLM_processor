# config.py

# --- PDF Extraction (1_extract_content.py) ---
# MANDATORY: Path to the folder containing your original PDF files
ORIGINAL_PDFS_FOLDER = "/path/to/your/pdf(s)/folder"

# MANDATORY: Path where extracted text and images will be stored
EXTRACTED_CONTENT_FOLDER = "/path/to/your/extraction/folder"

# --- LLM Processing (2_process_with_llm.py) ---
# MANDATORY: Path to the folder containing the extracted content (should be the same as EXTRACTED_CONTENT_FOLDER above)
INPUT_EXTRACTED_FOLDER = EXTRACTED_CONTENT_FOLDER # Or specify a different path if needed

# MANDATORY: Path where the LLM processed output (e.g., translated, summarized) will be stored
PROCESSED_OUTPUT_FOLDER = "/path/to/your/output/folder"

# MANDATORY: Your OpenAI API Key.
# IMPORTANT: It's best to set this as an environment variable OPENAI_API_KEY.
# If not set as an environment variable, the script will try to use the value below.
# Example: OPENAI_API_KEY = "sk-yourkeyhere"
OPENAI_API_KEY = None
# OpenAI Model to use (e.g., "gpt-4o-mini", "gpt-4-turbo", "gpt-3.5-turbo")
OPENAI_MODEL = "gpt-4o-mini" # A good balance of capability and cost

# Path to the prompt file for LLM processing
PROMPT_FILE_PATH = "prompts/process_page_prompt.txt"

# Number of concurrent workers for LLM processing (adjust based on your CPU and API rate limits)
MAX_WORKERS = 4 # Sensible default, adjust as needed

# --- Word Document Generation ---
# Default font size for content in generated Word documents
DEFAULT_FONT_SIZE_PT = 8
# Font size for pages with more than this many sentences (set to a high number to disable)
SMALLER_FONT_SIZE_PT = 6
SENTENCE_THRESHOLD_FOR_SMALLER_FONT = 15 # Adjust if you want dynamic font sizing

# --- Optional: PDF Page Range ---
# Set to None to process all pages.
# Otherwise, set as a tuple (start_page_index, end_page_index), e.g., (0, 5) for first 5 pages.
# Remember, page indexing is 0-based.
PAGE_RANGE_TO_PROCESS = None # Example: (0, 2) to process page 1 and 2 (0-indexed)