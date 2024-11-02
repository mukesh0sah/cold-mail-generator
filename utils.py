import re

def clean_text(text):
    # Remove leading and trailing whitespace
    text = text.strip()

    # Convert to lowercase
    text = text.lower()

    # Remove HTML tags
    text = re.sub(r'<.*?>', '', text)

    # Remove URLs (http, https, ftp, etc.)
    text = re.sub(r'http\S+|www.\S+', '', text)

    # Remove special characters (anything that isn't a letter, number, or space)
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)

    # Remove extra whitespace between words
    text = ' '.join(text.split())

    return text