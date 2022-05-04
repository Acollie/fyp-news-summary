from final_year_project_django.ingestion import between_two_sentences, text_reformatted
from final_year_project_django.models import News
from sentence_transformers import SentenceTransformer, util
# from manage import model
from operator import itemgetter
from manage import model


# Word2vec implementation
def find_similar_by_word_to_vec(search_string, n=5, threshold=0.75):
    news_articles = News.objects.all()
    largest_similar = []
    for article in news_articles:
        score = between_two_sentences(search_string, article.body_tldr,model)
        if score > threshold:
            largest_similar.append([score, {'title': article.title, 'body': article.body, 'body_tldr': article.body_tldr}])
    largest_similar.sort(key=itemgetter(0))

    return largest_similar[:n]


# This code is initially sources from this https://huggingface.co/sentence-transformers/multi-qa-MiniLM-L6-cos-v1
# However has been modified to work with django
# The threshold also has been added
"""Compute the Word Mover's Distance between two documents.
* `Ofir Pele and Michael Werman "A linear time histogram metric for improved SIFT matching"
  <http://www.cs.huji.ac.il/~werman/Papers/ECCV2008.pdf>`_
* `Ofir Pele and Michael Werman "Fast and robust earth mover's distances"
  <https://ieeexplore.ieee.org/document/5459199/>`_
* `Matt Kusner et al. "From Word Embeddings To Document Distances"
  <http://proceedings.mlr.press/v37/kusnerb15.pdf>`_.
"""

def find_similar_by_model_transformer(search_string, n=5, threshold=0.4):
    title = []
    articles = []
    article_tldr = []
    news_source = []
    for article in News.objects.all():
        title.append(article.title)
        articles.append(article.body)
        article_tldr.append(article.body_tldr)
        news_source.append(article.news_source)


    # Encode query and documents
    query_emb = model.encode(search_string)
    doc_emb = model.encode(title)

    # Compute dot score between query and all document embeddings
    scores = util.dot_score(query_emb, doc_emb)[0].cpu().tolist()

    # Combine title & scores
    doc_score_pairs = list(zip(title, scores, articles, article_tldr, news_source))

    # Sort by decreasing score
    doc_score_pairs = sorted(doc_score_pairs, key=lambda x: x[1], reverse=True)

    # Output passages & scores

    return_array = []
    for title, score, article, tldr,source in doc_score_pairs:
        if score > threshold:
            return_array.append([score, {'title': title, 'body': article, 'body_tldr': tldr,'news_source':source}])

    return return_array[:n]