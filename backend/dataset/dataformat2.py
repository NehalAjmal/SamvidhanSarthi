import re
import pandas as pd
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_TXT_FILE = os.path.join(SCRIPT_DIR, "constitution_raw.txt")
OUTPUT_CSV_FILE = os.path.join(SCRIPT_DIR, "articles.csv")
# ---------------------

# --- Regex Patterns ---
# Matches "PART I", "PART IVA", etc.
PART_REGEX = re.compile(r"^\s*P\s*A\s*R\s*T\s+[IVXLCDM]+[A-Z]?.*$")
# Matches "CHAPTER I", "CHAPTER II", etc.
CHAPTER_REGEX = re.compile(r"^\s*C\s*H\s*A\s*P\s*T\s*E\s*R\s+[IVXLCDM]+.*$")
# Matches "1.", "15.", "31A.", "394A."
# It now IGNORES lines that are clearly footnotes (Ins. by, Subs. by, etc.)
ARTICLE_REGEX = re.compile(
    r"^\s*(\d+[A-Z]?)\.\s+(?!(Subs\. by|Ins\. by|Added by|Omitted by|Rep\. by|See|Cl\.|Now|Art|w\.e\.f\.))(.+)$"
)
# Matches junk lines to ignore
JUNK_REGEX = re.compile(
    r"^\s*--- Page \d+ ---\s*$|"  # Page markers
    r"^\s*\(i+\)\s*$|"             # Lines with just (i), (ii)
    r"^\s*\[.*\]\s*$|"             # Lines with just [bracketed content]
    r"^\s*______________________________________________\s*$"  # Footnote lines
)
# Matches lines that are probably the *end* of a multi-line title
TITLE_END_REGEX = re.compile(r".*[\.—]$") 

# Matches lines that are clearly NOT article text (headings, etc.)
NON_TEXT_REGEX = re.compile(
    r"^\s*Right to .*|"
    r"^\s*Cultural and Educational Rights|"
    r"^\s*Saving of Certain Laws|"
    r"^\s*Miscellaneous|"
    r"^\s*General|"
    r"^\s*Conduct of Government Business|"
    r"^\s*Council of Ministers|"
    r"^\s*Procedure Generally"
)

def is_junk(line):
    """Checks if a line should be ignored entirely."""
    if not line:
        return True
    if JUNK_REGEX.search(line):
        return True
    if NON_TEXT_REGEX.search(line):
        return True
    return False

def save_article(data_list, current_data, text_buffer):
    """Helper to save the completed article data."""
    if current_data:
        current_data["original_text"] = " ".join(text_buffer).strip()
        data_list.append(current_data)
    return {}, [] # Return new, empty data and buffer

def parse_constitution_text(txt_path, csv_path):
    if not os.path.exists(txt_path):
        print(f"Error: Raw text file not found at '{txt_path}'")
        return

    print(f"Starting robust parsing of '{txt_path}'...")
    
    articles_data = []
    current_part = "PREAMBLE"
    current_chapter = "NONE"
    text_buffer = []
    current_article_data = {}
    
    parsing_started = False

    try:
        with open(txt_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        for i, line in enumerate(lines):
            line = line.strip()

            if not parsing_started:
                if "PREAMBLE" in line:
                    parsing_started = True
                    print("Found PREAMBLE. Starting parse...")
                    current_article_data = {
                        "part": "PREAMBLE",
                        "chapter": "NONE",
                        "article_no": "PREAMBLE",
                        "title": "PREAMBLE",
                        "original_text": "", "simple_text_en": "", "simple_text_hi": ""
                    }
                continue

            if is_junk(line):
                continue
                
            part_match = PART_REGEX.search(line)
            chapter_match = CHAPTER_REGEX.search(line)
            article_match = ARTICLE_REGEX.search(line)

            if part_match:
                current_article_data, text_buffer = save_article(articles_data, current_article_data, text_buffer)
                current_part = part_match.group(0).strip()
                current_chapter = "NONE"
                print(f"Found: {current_part}")

            elif chapter_match:
                current_article_data, text_buffer = save_article(articles_data, current_article_data, text_buffer)
                current_chapter = chapter_match.group(0).strip()
                print(f"  Found: {current_chapter}")
            
            elif article_match:
                current_article_data, text_buffer = save_article(articles_data, current_article_data, text_buffer)
                
                article_no = article_match.group(1).strip()
                title = article_match.group(3).strip()

                # Handle multi-line titles
                # Check if next line looks like more title (not a new part/chapter/article)
                if (i + 1) < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not (PART_REGEX.search(next_line) or 
                                         CHAPTER_REGEX.search(next_line) or 
                                         ARTICLE_REGEX.search(next_line) or
                                         NON_TEXT_REGEX.search(next_line)) and \
                                         TITLE_END_REGEX.search(title):
                        title += " " + next_line
                        # We will process the next line as part of this one, so skip it
                        lines[i + 1] = "" # Blank it out so we skip it

                current_article_data = {
                    "part": current_part,
                    "chapter": current_chapter,
                    "article_no": article_no,
                    "title": title,
                    "original_text": "", "simple_text_en": "", "simple_text_hi": ""
                }
            
            # This is article text
            elif current_article_data and not (part_match or chapter_match or article_match):
                text_buffer.append(line)

        # --- Save the very last article ---
        save_article(articles_data, current_article_data, text_buffer)

        # --- Export to CSV ---
        if not articles_data:
            print("\nError: No articles were parsed.")
            return

        print(f"\nParsing complete. Found {len(articles_data)} articles.")
        
        df = pd.DataFrame(articles_data, columns=[
            "part", "chapter", "article_no", "title", 
            "original_text", "simple_text_en", "simple_text_hi"
        ])
        
        # Clean up any bad titles
        df['title'] = df['title'].str.replace('—$', '', regex=True).str.strip()
        
        df.to_csv(csv_path, index=False, encoding="utf-8")
        
        print(f"Success! Structured data saved to '{csv_path}'")

    except Exception as e:
        print(f"\nAn error occurred during parsing: {e}")

# --- Run the parsing ---
if __name__ == "__main__":
    parse_constitution_text(INPUT_TXT_FILE, OUTPUT_CSV_FILE)