import re
import pandas as pd
import os

# --- Configuration ---
# Get the directory where this script (dataformat2.py) is located
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT_FILE = os.path.join(SCRIPT_DIR, "constitution_raw.txt")
OUTPUT_CSV_FILE = os.path.join(SCRIPT_DIR, "articles.csv")
# ---------------------

# --- Regex Patterns ---
# We will try to find lines that match these patterns.
#
# ^\s* -> Starts with (^) any amount of whitespace (\s*)
# (\d+[A-Z]?)    -> Captures a number (e.g., "51" or "51A")
# \.             -> Followed by a literal dot
# \s+            -> Followed by one or more spaces
# (.+)           -> Captures all other text on the line (the title)
# $              -> End of the line
ARTICLE_REGEX = re.compile(r"^\s*(\d+[A-Z]?)\.\s+([^.]+)$")

# --- UPDATED REGEX ---
# This now looks for "PART [Roman Numeral]" and captures the ENTIRE line
PART_REGEX = re.compile(r"^\s*(P\s*A\s*R\s*T\s+[IVXLCDM]+.*)$")

# --- UPDATED REGEX ---
# This now looks for "CHAPTER [Roman Numeral]" and captures the ENTIRE line
CHAPTER_REGEX = re.compile(r"^\s*(C\s*H\s*A\s*P\s*T\s*E\s*R\s+[IVXLCDM]+.*)$")

# This is to filter out the junk lines we added
JUNK_REGEX = re.compile(r"^\s*--- Page \d+ ---\s*$")

def parse_constitution_text(txt_path, csv_path):
    """
    Reads the raw text file, parses it using regex, and saves the
    structured data to a CSV file.
    """
    
    if not os.path.exists(txt_path):
        print(f"Error: Raw text file not found at '{txt_path}'")
        return

    print(f"Starting parsing of '{txt_path}' (v2)...")
    
    articles_data = []
    current_part = "NONE"
    current_chapter = "NONE"
    text_buffer = []
    current_article_data = {}

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line_num, line in enumerate(f, 1):
                try:
                    line = line.strip()

                    if not line or JUNK_REGEX.search(line):
                        continue
                    
                    part_match = PART_REGEX.search(line)
                    chapter_match = CHAPTER_REGEX.search(line)
                    article_match = ARTICLE_REGEX.search(line)

                    if part_match:
                        if current_article_data:
                            current_article_data["original_text"] = " ".join(text_buffer).strip()
                            articles_data.append(current_article_data)
                        
                        current_part = part_match.group(1)
                        if current_part:  # Add null check
                            current_part = current_part.strip()
                        else:
                            current_part = "NONE"
                        current_chapter = "NONE"
                        current_article_data = {}
                        text_buffer = []
                        print(f"Found: {current_part}")

                    elif chapter_match:
                        if current_article_data:
                            current_article_data["original_text"] = " ".join(text_buffer).strip()
                            articles_data.append(current_article_data)
                            
                        current_chapter = chapter_match.group(1)
                        if current_chapter:  # Add null check
                            current_chapter = current_chapter.strip()
                        else:
                            current_chapter = "NONE"
                        current_article_data = {}
                        text_buffer = []
                        print(f"  Found: {current_chapter}")
                    
                    elif article_match:
                        if current_article_data:
                            current_article_data["original_text"] = " ".join(text_buffer).strip()
                            articles_data.append(current_article_data)

                        article_no = article_match.group(1)
                        title = article_match.group(2)
                        
                        if article_no and title:  # Add null checks
                            current_article_data = {
                                "part": current_part,
                                "chapter": current_chapter,
                                "article_no": article_no.strip(),
                                "title": title.strip(),
                                "original_text": "",
                                "simple_text_en": "",
                                "simple_text_hi": ""
                            }
                            text_buffer = []
                        
                    elif current_article_data:
                        text_buffer.append(line)

                except Exception as e:
                    print(f"Warning: Error processing line {line_num}: {str(e)}")
                    continue

        # --- 4. Save the very last article ---
        if current_article_data:
            current_article_data["original_text"] = " ".join(text_buffer).strip()
            articles_data.append(current_article_data)

        # --- 5. Export to CSV ---
        if not articles_data:
            print("\nError: No articles were parsed. The regex patterns might need adjustment.")
            return

        print(f"\nParsing complete. Found {len(articles_data)} articles.")
        
        # Use pandas to create a clean DataFrame and save to CSV
        df = pd.DataFrame(articles_data, columns=[
            "part", "chapter", "article_no", "title", 
            "original_text", "simple_text_en", "simple_text_hi"
        ])
        
        df.to_csv(csv_path, index=False, encoding="utf-8")
        
        print(f"Success! Structured data saved to '{csv_path}'")

    except Exception as e:
        print(f"\nAn error occurred during parsing: {e}")

# --- Run the parsing ---
if __name__ == "__main__":
    parse_constitution_text(INPUT_TXT_FILE, OUTPUT_CSV_FILE)