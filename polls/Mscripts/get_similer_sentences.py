import time
from scipy import spatial

import torch
from sentence_transformers import SentenceTransformer, util

from .project_classes import query_n_sentence_list


def get_similer_sentences(queries, sentence, top_k=1):
    embedder = SentenceTransformer('paraphrase-distilroberta-base-v1')
    sentence_embeddings = embedder.encode(sentence, convert_to_tensor=True)
    similer_sentences_list = []

    for query in queries:
        similer_sentences = []
        query_embedding = embedder.encode(query, convert_to_tensor=True)
        cos_scores = util.pytorch_cos_sim(query_embedding, sentence_embeddings)[0]
        cos_scores = cos_scores.cpu()

        # We use torch.topk to find the highest 5 scores
        top_results = torch.topk(cos_scores, k=top_k)
        for index in top_results[1]:
            if sentence[index] != query:
                similer_sentences.append(sentence[index])

        similer_sentences_list.append(query_n_sentence_list(query, similer_sentences))
    return similer_sentences_list
