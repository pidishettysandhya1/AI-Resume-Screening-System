from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_similarity_score(job_desc, resume_text):

    tfidf = TfidfVectorizer()

    vectors = tfidf.fit_transform([job_desc, resume_text])

    score = cosine_similarity(vectors[0], vectors[1])[0][0]

    return round(score * 100, 2)