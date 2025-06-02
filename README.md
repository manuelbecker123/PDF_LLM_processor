# PDF Page-by-Page LLM Processor

This project provides a two-step workflow to extract content from PDF files (text and images) on a page-by-page basis, and then process the text from each page using a Large Language Model (LLM) like OpenAI's GPT series. The processed content, along with the original, is saved into Word documents, preserving page structure and image references.

The key advantage of this tool is its flexibility. Instead of being just a translator, you can customize the prompt sent to the LLM to perform various tasks on each page of your documents, such as:

* **Translation:** Translate academic papers or Ebooks page by page.
* **Summarization:** Generate concise summaries for each page.
* **Question Answering/Generation:** Create quiz questions based on page content, or even attempt to answer predefined questions about each page.
* **Data Extraction:** Identify key information, entities, or themes per page.
* **Content Transformation:** Rephrase content, change its tone, or explain complex topics in simpler terms for each page.

## Features

* Extracts text and images from PDFs.
* Preserves page structure with clear "START OF PAGE" and "END OF PAGE" markers.
* Embeds image references directly in the extracted text (`(IMAGE: filename.png)`).
* Processes text from each page using an OpenAI LLM.
* Highly customizable LLM interaction via a user-defined task instruction and a prompt template.
* Saves both original extracted text and LLM-processed text as Word documents (.docx).
* Copies associated images to the output folders for easy reference.
* Handles multiple PDFs and processes them in distinct chapter-like folders.
* Supports concurrent processing of pages to speed up LLM interactions (configurable).
* Optionally process only a specific range of pages from the PDFs.

## Prerequisites

* Python 3.7+
* Pip (Python package installer)
* An OpenAI API Key

## Setup

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/pdf_llm_processor.git](https://github.com/YOUR_USERNAME/pdf_llm_processor.git)
    cd pdf_llm_processor
    ```

2.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure API Key:**
    * **Recommended:** Set your OpenAI API key as an environment variable:
        ```bash
        export OPENAI_API_KEY="sk-yourSecretApiKeyHere"
        ```
        (On Windows, use `set OPENAI_API_KEY=sk-yourSecretApiKeyHere` in Command Prompt or `$env:OPENAI_API_KEY="sk-yourSecretApiKeyHere"` in PowerShell).
    * **Alternative:** Directly edit `config.py` and set the `OPENAI_API_KEY` variable. **Warning:** Avoid committing your API key to a public repository if you do this.

5.  **Configure Paths and Settings:**
    * Open `config.py`.
    * **Crucially, update:**
        * `ORIGINAL_PDFS_FOLDER`: Path to your source PDF files.
        * `EXTRACTED_CONTENT_FOLDER`: Where intermediate text/image files will be stored.
        * `PROCESSED_OUTPUT_FOLDER`: Where the final Word documents and images will be saved.
    * Review and adjust other settings like `OPENAI_MODEL`, `MAX_WORKERS`, `PAGE_RANGE_TO_PROCESS`, and font sizes as needed.

6.  **Customize the LLM Prompt (Optional but Important for Non-Translation Tasks):**
    * The core interaction with the LLM is defined in `prompts/process_page_prompt.txt`.
    * This template uses `{{TASK_INSTRUCTION}}` and `{{PAGE_TEXT}}`.
    * When you run `2_process_with_llm.py`, you will be asked to provide the `TASK_INSTRUCTION`.
    * Examples for `TASK_INSTRUCTION`:
        * "Translate the following text from English to German, maintaining a formal and academic tone."
        * "Summarize the key points of the following text in three bullet points."
        * "Generate three potential quiz questions based on the content of this text, along with their answers."
    * You can modify `prompts/process_page_prompt.txt` for more advanced control over the LLM's overall behavior.

## Usage

The process is two-staged:

**Stage 1: Extract Content from PDFs**

* Place your PDF files into the folder specified by `ORIGINAL_PDFS_FOLDER` in `config.py`.
* Run the extraction script:
    ```bash
    python 1_extract_content.py
    ```
* This will create subfolders (one for each PDF, named e.g., `doc_001_YourPDFName`) inside `EXTRACTED_CONTENT_FOLDER`. Each subfolder will contain:
    * `extracted_text_doc_001_YourPDFName.txt`: The text content with page markers and image references.
    * `doc_001_YourPDFName_imgs/`: A folder with all images extracted from that PDF.

**Stage 2: Process Extracted Content with LLM**

* Ensure Stage 1 is complete and `config.py` points to the correct `INPUT_EXTRACTED_FOLDER` (usually same as `EXTRACTED_CONTENT_FOLDER`).
* Run the LLM processing script:
    ```bash
    python 2_process_with_llm.py
    ```
* You will be prompted to enter your specific `TASK_INSTRUCTION` for the LLM (e.g., "Translate to Spanish", "Summarize this page").
* This script will:
    * Read the `.txt` files generated in Stage 1.
    * For each page's text, send it to the OpenAI API with your instructions.
    * Create subfolders inside `PROCESSED_OUTPUT_FOLDER` (mirroring the structure from `EXTRACTED_CONTENT_FOLDER`).
    * In each subfolder, it will save:
        * `original_doc_001_YourPDFName.docx`: The original extracted text as a Word document.
        * `processed_doc_001_YourPDFName.docx`: The LLM-processed text as a Word document.
        * `doc_001_YourPDFName_imgs/`: A copy of the images folder.

## Customization Ideas

* **Different LLMs:** Modify `2_process_with_llm.py` to use other LLM APIs (e.g., Anthropic Claude, Google Gemini) by changing the API call logic in `call_llm_for_page`.
* **Advanced Prompting:** Experiment with different `{{TASK_INSTRUCTION}}` inputs or edit `prompts/process_page_prompt.txt` for more sophisticated few-shot prompting or role-playing instructions.
* **Output Format:** Change `save_text_as_word` in `2_process_with_llm.py` to output in Markdown, JSON, or other formats instead of .docx.
* **Image Processing:** Extend the scripts to also send images to multimodal LLMs for description or analysis.

## Contributing

Feel free to fork this repository, make improvements, and submit pull requests!

## License

This project is licensed under the MIT License - see the LICENSE file for details (you'll need to create a `LICENSE` file, typically with the MIT license text).