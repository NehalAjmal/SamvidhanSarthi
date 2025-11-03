import re
import pandas as pd
import os

# --- Configuration ---
INPUT_TXT_FILE = "constitution_raw.txt"
OUTPUT_CSV_FILE = "articles.csv"
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
ARTICLE_REGEX = re.compile(r"^\s*(\d+[A-Z]?)\.\s+(.+)$")

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
    
    articles_data = []          # Our final list of all articles
    current_part = "NONE"       # Stores the current Part (e.g., "PART V")
    current_chapter = "NONE"    # Stores the current Chapter (e.g., "CHAPTER I")
    text_buffer = []            # Temporarily holds the text for the current article
    current_article_data = {}   # Holds the data for the article being processed

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip() # Clean up leading/trailing whitespace

                # --- 1. Filter out Junk ---
                if not line or JUNK_REGEX.search(line):
                    continue
                
                # --- 2. Check for Structure (Part, Chapter, Article) ---
                # We check in order of importance
                part_match = PART_REGEX.search(line)
                chapter_match = CHAPTER_REGEX.search(line)
                article_match = ARTICLE_REGEX.search(line)

                # --- 3. Handle Found Patterns ---
                
                # A. Found a new PART
                if part_match:
                    # Before moving to the new part, save the PREVIOUS article
                    if current_article_data:
                        current_article_data["original_text"] = " ".join(text_buffer).strip()
                        articles_data.append(current_article_data)
                    
                    # Now, set the new part and reset everything else
                    # We capture the full line as the part title
                    current_part = part_match.group(1).strip() 
                    current_chapter = "NONE" # Reset chapter
                    current_article_data = {}
                    text_buffer = []
                    print(f"Found: {current_part}")

                # B. Found a new CHAPTER
                elif chapter_match:
                    # Before moving to the new chapter, save the PREVIOUS article
                    if current_article_data:
                        current_article_data["original_text"] = " ".join(text_buffer).strip()
                        articles_data.append(current_article_data)
                        
                    # Now, set the new chapter
                    # We capture the full line as the chapter title
                    current_chapter = chapter_match.group(1).strip()
                    current_article_data = {}
                    text_buffer = []
                    print(f"  Found: {current_chapter}")
                
                # C. Found a new ARTICLE
                elif article_match:
                    # Before moving to the new article, save the PREVIOUS article
                    if current_article_data:
                        current_article_data["original_text"] = " ".join(text_buffer).strip()
                        articles_data.append(current_article_data)

                    # Now, create the new article's data
                    article_no = article_match.group(1)
                    title = article_match.group(2).strip()
                    
                    current_article_data = {
                        "part": current_part,
                        "chapter": current_chapter,
                        "article_no": article_no,
                        "title": title,
                        "original_text": "",
                        "simple_text_en": "", # Will be filled by content team
                        "simple_text_hi": ""  # Will be filled by content team
                    }
                    text_buffer = [] # Clear the buffer for the new article's text

                # D. Not a Part, Chapter, or Article title
                else:
                    # This line must be the body text of the current article.
                    # Add it to our buffer.
                    if current_article_data: # Only add if we're "inside" an article
                        text_buffer.append(line)

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