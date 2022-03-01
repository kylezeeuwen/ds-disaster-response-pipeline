import re

import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.wordnet import WordNetLemmatizer

def conditionally_download_nltk_package (lookup_name, download_name):
    try:
        nltk.data.find(lookup_name)
    except LookupError:
        print(f"downloading nltk {download_name}")
        nltk.download(download_name)

conditionally_download_nltk_package('tokenizers/punkt', 'punkt')
conditionally_download_nltk_package('stopwords', 'stopwords')
conditionally_download_nltk_package('wordnet', 'wordnet')
conditionally_download_nltk_package('omw-1.4', 'omw-1.4')

english_stopwords = stopwords.words("english")

# TODO better name
def my_tokenize(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9]", " ", text)
    words = word_tokenize(text)
    words = [w for w in words if w not in english_stopwords]
    words = [WordNetLemmatizer().lemmatize(w) for w in words]

    return words
