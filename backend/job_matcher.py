"""Compare resumes with job descriptions."""
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


# Load pretrained Sentence Transformer model
model = SentenceTransformer("all-MiniLM-L6-v2")


def generate_embedding(text):

    embedding = model.encode(text)

    return embedding


def calculate_similarity(resume_text, job_description):

    # Generate embeddings
    resume_embedding = generate_embedding(resume_text)

    job_embedding = generate_embedding(job_description)

    # Calculate cosine similarity
    similarity = cosine_similarity(
        [resume_embedding],
        [job_embedding]
    )

    # Convert similarity into percentage
    score = similarity[0][0] * 100

    return round(float(score), 2)