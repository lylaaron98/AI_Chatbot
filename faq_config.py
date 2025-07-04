from sentence_transformers import SentenceTransformer, util

# Load lightweight model for semantic similarity
model = SentenceTransformer("all-MiniLM-L6-v2")

# Your curated FAQ
FAQ = {
    "What is AIE?": "The Applied Innovation Exchange (AIE) is Capgemini's global innovation platform, providing our clients with a gateway to the latest technnology and thinking. The AIE enables our clients to explore the innovation landscape; contextualize opportunities within their business; experiment with new concepts and ideas; and de-risk innovation efforts.",
    "What is ASE?": "The ASE design and deliver dynamic, empowering experiences that create the right conditions to unleash group genius. Using our unique combination of capabiltiies, we strip away the rational, emtional and political blockers that get in the way of powerful, transformative business outcomes. By unlocking this human potential, we enable teams, projects and organisations to connect differently. This creates the passion, engagement, alignment and momentum you need to get the future you want.",
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
