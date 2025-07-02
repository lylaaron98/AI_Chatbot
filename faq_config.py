from sentence_transformers import SentenceTransformer, util

# Load lightweight model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

# Your curated FAQ
FAQ = {
    "What is AIE?": "The Applied Innovation Exchange (AIE) is Capgemini's global innovation platform, providing our clients with a gateway to the latest technnology and thinking. The AIE enables our clients to explore the innovation landscape; contextualize opportunities within their business; experiment with new concepts and ideas; and de-risk innovation efforts.",
    "What is ASE?": "The ASE design and deliver dynamic",
    "What are the available booking hours?": "The room is available from 9:00 AM to 6:00 PM, Monday to Friday.",
}

faq_questions = list(FAQ.keys())
faq_embeddings = model.encode(faq_questions, convert_to_tensor=True)

def get_faq_response(user_input):
    user_embedding = model.encode(user_input, convert_to_tensor=True)
    scores = util.cos_sim(user_embedding, faq_embeddings)[0]
    best_idx = int(scores.argmax())
    best_score = float(scores[best_idx])

    if best_score > 0.65:
        return FAQ[faq_questions[best_idx]]
    else:
        return None
