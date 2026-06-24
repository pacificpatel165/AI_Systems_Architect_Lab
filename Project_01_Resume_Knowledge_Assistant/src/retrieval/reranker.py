from sentence_transformers import CrossEncoder


def load_reranker_model(model_name):
    reranker = CrossEncoder(model_name)
    print("Reranker Loaded")
    return reranker
