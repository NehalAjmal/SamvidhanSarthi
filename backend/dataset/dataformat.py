import pdfplumber
import os

# --- Configuration ---
PDF_FILE_NAME = "20240716890312078.pdf"  # The name of your PDF file
OUTPUT_TXT_FILE = "constitution_raw.txt"   # The name of the text file we will create
# ---------------------

def extract_text_from_pdf(pdf_path, txt_path):
    """
    Extracts all text from a PDF and saves it to a single .txt file,
    preserving page order.
    """
    
    # Check if the PDF file exists
    if not os.path.exists(pdf_path):
        print(f"Error: PDF file not found at '{pdf_path}'")
        print("Please make sure the file is in the same directory and the name is correct.")
        return

    print(f"Starting extraction from '{pdf_path}'...")
    
    full_text = ""
    
    try:
        with pdfplumber.open(pdf_path) as pdf:
            total_pages = len(pdf.pages)
            print(f"PDF has {total_pages} pages.")
            
            for i, page in enumerate(pdf.pages):
                # Extract text from the current page
                page_text = page.extract_text()
                
                if page_text:
                    full_text += page_text + "\n"
                
                # Add a clear separator between pages
                full_text += f"\n--- Page {i + 1} ---\n\n"

                # Print progress
                if (i + 1) % 50 == 0 or (i + 1) == total_pages:
                    print(f"Processed page {i + 1} / {total_pages}")

        # Write the extracted text to the output file
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(full_text)
            
        print(f"\nSuccess! All text extracted and saved to '{txt_path}'")

    except Exception as e:
        print(f"\nAn error occurred: {e}")

# --- Run the extraction ---
if __name__ == "__main__":
    extract_text_from_pdf(PDF_FILE_NAME, OUTPUT_TXT_FILE)