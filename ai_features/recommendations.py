from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import pandas as pd

# Load a pre-trained model (once, during app startup)
model = SentenceTransformer('all-MiniLM-L6-v2')

def recommend_businesses_transformer(user_query, location, business_data):
    """
    Recommends businesses using a Transformer-based model (Sentence-BERT).
    """
    df = pd.DataFrame(business_data)

    # Filter by location
    if location:
        df = df[df['location'].str.contains(location, case=False, na=False)]

    # If no businesses match, return an empty list
    if df.empty:
        return []

    # Combine relevant text fields
    df['combined_text'] = df['name'] + " " + df['services_offered']

    # Encode business descriptions into vectors
    business_embeddings = model.encode(df['combined_text'].tolist())

    # Encode user query
    query_embedding = model.encode([user_query])[0]

    # Compute similarity scores using dot product
    similarity_scores = np.dot(business_embeddings, query_embedding)

    # Add similarity scores to the DataFrame and sort
    df['similarity'] = similarity_scores
    recommended = df.sort_values(by='similarity', ascending=False).head(5)

    return recommended[['name', 'services_offered', 'location', 'similarity']].to_dict(orient='records')

def recommend_businesses_tfidf(user_query, location, business_data):
    """
    Recommends businesses using a TF-IDF vectorizer with cosine similarity.
    """
    df = pd.DataFrame(business_data)

    # Filter by location
    if location:
        df = df[df['location'].str.contains(location, case=False, na=False)]

    # If no businesses match, return an empty list
    if df.empty:
        return []

    # Combine text fields for better matching
    df['combined_text'] = df['name'] + " " + df['services_offered']

    # Apply TF-IDF
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(df['combined_text'])

    # Convert query into a TF-IDF vector
    query_vector = vectorizer.transform([user_query])

    # Compute similarity scores using cosine similarity
    similarity_scores = cosine_similarity(query_vector, tfidf_matrix).flatten()

    # Add similarity scores and sort
    df['similarity'] = similarity_scores
    recommended = df.sort_values(by='similarity', ascending=False).head(5)

    return recommended[['name', 'services_offered', 'location', 'similarity']].to_dict(orient='records')
