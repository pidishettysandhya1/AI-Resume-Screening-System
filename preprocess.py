import re
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')

# function to clean text
def preprocess_text(text):

    # convert to lowercase
    text = text.lower()

    # remove special characters
    text = re.sub(r'[^a-zA-Z ]', '', text)

    # remove stopwords
    stop_words = set(stopwords.words('english'))
    words = text.split()

    clean_words = [w for w in words if w not in stop_words]

    return " ".join(clean_words)