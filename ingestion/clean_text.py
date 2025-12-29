import re

def clean_text(text):
    text = re.sub(r'\n\s*\d+\s*\n', '\n', text)
    text = re.sub(r'Data and Computer Communications.*\n', '', text)
    text = re.sub(r'William Stallings.*\n', '', text)

    if "References" in text:
        text = text.split("References")[0]

    text = re.sub(r'\n{2,}', '\n\n', text)
    return text.strip()
