from sentence_transformers import SentenceTransformer, util

# Load lightweight model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

# Your curated FAQ
FAQ = {
    "What is AIE?": "The Applied Innovation Exchange (AIE) is Capgemini’s global network focused on innovation and emerging technologies. It serves as a structured environment where clients and teams can explore new technologies, assess their relevance to specific business contexts, and test ideas through rapid prototyping. The AIE supports innovation by helping organizations reduce risk, align stakeholders, and accelerate the adoption of new solutions.",
    "What is ASE?": "The Accelerated Solutions Environment (ASE) is a facilitation approach developed by Capgemini to help teams solve complex problems and align on strategic decisions. It combines design thinking, systems thinking, and collaborative methods to create high-impact working sessions. ASE engagements are designed to remove common barriers to progress—such as misalignment, lack of clarity, or organizational silos—by fostering focused, inclusive, and creative group work.",
    "Can I use AIE?": "The room is available from 9:00 AM to 6:00 PM, Monday to Friday.",
    "What do I need to provide if I want to use the AIE & ASE service?" : "To use the AIE & ASE service, you need to provide a brief description of your project or idea, the number of participants, and any specific requirements you may have for the session.",
    "What is the difference between AIE and ASE?": "The AIE focuses on innovation by providing a platform to explore, experiment, and de-risk new ideas and technologies. On the other hand, the ASE specializes in creating dynamic, collaborative experiences to unlock group potential and drive transformative business outcomes. While AIE is centered on innovation enablement, ASE is focused on facilitating human-centered collaboration.",

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
