import pandas as pd
import re
from deep_translator import GoogleTranslator
from datetime import datetime

# === CONFIGURATION ===
INPUT_FILE = "input.xlsx"
TARGET_LANG = "ml"  # Use 'hi' for Hindi, 'ml' for Malayalam

# === FUNCTION: Check if translation is needed ===
def is_symbolic_only(text):
    if not isinstance(text, str):
        return True
    cleaned = re.sub(r'\{[^}]+\}', '', text)  # remove placeholders
    cleaned = re.sub(r'[^\w]', '', cleaned)   # remove punctuation/symbols
    return len(cleaned.strip()) == 0

# === FUNCTION: Translate text while preserving placeholders ===
def translate_preserving_curly_brackets(text):
    if not isinstance(text, str) or is_symbolic_only(text):
        return text

    try:
        # Find all {placeholders}
        curly_items = re.findall(r'\{[^}]+\}', text)

        # Temporarily replace with safe placeholders: <<0>>, <<1>>, ...
        temp_text = text
        for idx, item in enumerate(curly_items):
            temp_text = temp_text.replace(item, f"<<{idx}>>")

        # Translate the temporary version
        translated_temp = GoogleTranslator(source='en', target=TARGET_LANG).translate(temp_text)

        # Replace back with original {placeholders}
        for idx, item in enumerate(curly_items):
            translated_temp = translated_temp.replace(f"<<{idx}>>", item)

        return translated_temp

    except Exception as e:
        print(f"❌ Error translating: {text} | {e}")
        return text

# === MAIN FUNCTION ===
def main():
    try:
        df = pd.read_excel(INPUT_FILE)

        if 'Question' not in df.columns:
            print("❌ Column 'Question' not found in input.")
            return

        print(f"🔁 Translating to '{TARGET_LANG}'...")

        df['Question'] = df['Question'].apply(translate_preserving_curly_brackets)

        output_file = f"translated_output_{TARGET_LANG}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        df.to_excel(output_file, index=False)
        print(f"✅ Done! Saved as: {output_file}")

    except Exception as err:
        print("❌ Main Error:", err)

# === RUN ====
if __name__ == "__main__":
    main()
