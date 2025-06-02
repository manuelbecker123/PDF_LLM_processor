# 1_extract_content.py
import fitz  # PyMuPDF
import os
import sys
import config  # Import the configuration

def process_pdf(pdf_path, chapter_name, output_base_folder):
    """
    Extracts text and images from a PDF file, page by page.
    """
    chapter_folder = os.path.join(output_base_folder, chapter_name)
    os.makedirs(chapter_folder, exist_ok=True)

    img_dir = os.path.join(chapter_folder, f'{chapter_name}_imgs')
    os.makedirs(img_dir, exist_ok=True)

    try:
        doc = fitz.open(pdf_path)
    except Exception as e:
        print(f"Error opening PDF {pdf_path}: {e}")
        return

    start_page_index = 0
    end_page_index = doc.page_count

    if config.PAGE_RANGE_TO_PROCESS:
        start_page_index = config.PAGE_RANGE_TO_PROCESS[0]
        # Ensure end_page_index is within bounds and correctly set
        # If user specifies (0, 2) for a 10-page doc, they mean pages 0, 1.
        # So if end_page_index in config is N, we want to process up to page N-1.
        # The range function then needs to go up to N.
        end_page_index = min(config.PAGE_RANGE_TO_PROCESS[1], doc.page_count)


    output_text_file = os.path.join(chapter_folder, f'extracted_text_{chapter_name}.txt')

    with open(output_text_file, 'w', encoding='utf-8') as f_out:
        for page_number_idx in range(start_page_index, end_page_index):
            try:
                page = doc.load_page(page_number_idx)
                text = page.get_text("text")
                relevant_text = text.strip()

                image_list = page.get_images(full=True)
                for img_index, img_info in enumerate(image_list):
                    xref = img_info[0]
                    base_image = doc.extract_image(xref)
                    image_bytes = base_image["image"]
                    image_ext = base_image["ext"] # Get image extension

                    img_filename = f"PAGE_{page_number_idx + 1}_IMG_{img_index + 1}.{image_ext}"
                    img_path = os.path.join(img_dir, img_filename)

                    with open(img_path, "wb") as img_file:
                        img_file.write(image_bytes)

                    image_reference = f"(IMAGE: {img_filename})"
                    relevant_text += f"\n{image_reference}"

                f_out.write("=" * 50 + "\n")
                f_out.write(f"START OF PAGE: {page_number_idx + 1}\n")
                f_out.write("=" * 50 + "\n")
                f_out.write(relevant_text.strip() + "\n")
                f_out.write("=" * 50 + "\n")
                f_out.write(f"END OF PAGE: {page_number_idx + 1}\n")
                f_out.write("=" * 50 + "\n\n")
            except Exception as e:
                print(f"Error processing page {page_number_idx + 1} in {pdf_path}: {e}")
                f_out.write("=" * 50 + "\n")
                f_out.write(f"ERROR PROCESSING PAGE: {page_number_idx + 1}\n")
                f_out.write(str(e) + "\n")
                f_out.write("=" * 50 + "\n\n")


    doc.close()
    print(f"Extraction complete for {chapter_name}. Output saved to: {chapter_folder}")

def main():
    if not os.path.exists(config.ORIGINAL_PDFS_FOLDER):
        print(f"ERROR: Original PDFs folder not found: {config.ORIGINAL_PDFS_FOLDER}")
        print("Please create this folder and add your PDFs or update its path in config.py.")
        return

    if not os.path.exists(config.EXTRACTED_CONTENT_FOLDER):
        os.makedirs(config.EXTRACTED_CONTENT_FOLDER)
        print(f"Created output folder: {config.EXTRACTED_CONTENT_FOLDER}")

    pdf_files = [f for f in os.listdir(config.ORIGINAL_PDFS_FOLDER) if f.lower().endswith('.pdf')]
    pdf_files.sort()

    if not pdf_files:
        print(f"No PDF files found in {config.ORIGINAL_PDFS_FOLDER}")
        return

    print(f"Found {len(pdf_files)} PDF(s) to process.")

    for i, pdf_file in enumerate(pdf_files, 1):
        # Use original PDF filename (without extension) as chapter name for better identification
        chapter_name = os.path.splitext(pdf_file)[0]
        # Sanitize chapter_name to be a valid directory name
        chapter_name = "".join(c if c.isalnum() or c in (' ', '_', '-') else '_' for c in chapter_name).rstrip()
        chapter_name = f"doc_{i:03d}_{chapter_name}" # Add a numeric prefix for ordering

        pdf_path = os.path.join(config.ORIGINAL_PDFS_FOLDER, pdf_file)
        print(f"\nProcessing PDF: {pdf_file} as '{chapter_name}'...")
        process_pdf(pdf_path, chapter_name, config.EXTRACTED_CONTENT_FOLDER)

    print("\nAll PDF processing finished.")
    print(f"Extracted content can be found in: {config.EXTRACTED_CONTENT_FOLDER}")

if __name__ == '__main__':
    main()