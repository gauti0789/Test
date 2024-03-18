from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def preprocess_text(text):
    # Perform any necessary preprocessing on the text
    # For example, lowercase, remove punctuation, etc.
    return text.lower()

def calculate_accuracy(generated_answer, retrieved_documents):
    try:
        # Preprocess generated answer
        generated_answer = preprocess_text(generated_answer)

        # Concatenate strings within each document to form a single text block
        concatenated_docs = [' '.join(doc) for doc in retrieved_documents]

        # Preprocess and vectorize retrieved documents
        vectorizer = TfidfVectorizer()
        document_vectors = vectorizer.fit_transform([preprocess_text(doc) for doc in concatenated_docs])
        # Calculate cosine similarity between generated answer and retrieved documents
        similarities = cosine_similarity(vectorizer.transform([generated_answer]), document_vectors)
        avg_similarity = similarities.max()
        accuracy = avg_similarity
        return accuracy
    except Exception as e:
        print("Error:", e)
        return None  # or handle the error in another way

def calculate_confidence_scores(generated_answer, retrieved_documents):
    try:
        # Preprocess generated answer
        generated_answer = preprocess_text(generated_answer)

        # Concatenate strings within each document to form a single text block
        concatenated_docs = [' '.join(doc) for doc in retrieved_documents]

        # Preprocess and vectorize retrieved documents
        vectorizer = TfidfVectorizer()
        document_vectors = vectorizer.fit_transform([preprocess_text(doc) for doc in concatenated_docs])

        # Calculate cosine similarity between generated answer and retrieved documents
        similarities = cosine_similarity(vectorizer.transform([generated_answer]), document_vectors)

        # Normalize similarity scores to range between 0 and 1
        max_similarity = similarities.max()
        min_similarity = similarities.min()
        confidence_scores = [(similarity - min_similarity) / (max_similarity - min_similarity) for similarity in similarities[0]]
        
        return confidence_scores
    except Exception as e:
        print("Error:", e)
        return None  # or handle the error in another way