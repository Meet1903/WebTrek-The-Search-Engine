from scipy.linalg import triu
from gensim.models import KeyedVectors
word2vec_model = KeyedVectors.load_word2vec_format('GoogleNews-vectors-negative300.bin', binary=True, limit=100000)
import numpy as np

unnecessary_words = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 
              'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
              'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 
              'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 
              'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 
              'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before',
              'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again',
              'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few',
              'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very',
              'can', 'will', 'just', 'don', 'should', 'now']

stop_words = set(unnecessary_words)

def initiate_ranking_algorithm():
    print("Algorithm Initiated")

def preprocess_text(text):
    #tokens = word_tokenize(text.lower())
    # tokens = word_tokenize(text)
    tokens = text.split(' ')
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def preprocess_query(query):
    #tokens = word_tokenize(query.lower())
    # tokens = word_tokenize(query)
    tokens = query.split(' ')
    tokens = [token for token in tokens if token.isalpha()]
    tokens = [token for token in tokens if token not in stop_words]
    return tokens

def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def get_embedding(tokens):
    e= np.mean([word2vec_model[token] for token in tokens if token in word2vec_model], axis=0)
    if np.isnan(e).any():
        e = word2vec_model["the"]*0
    return e

def my_relevance_score(page_text, query):
    page_tokens = preprocess_text(page_text)
    query_tokens = preprocess_query(query)
    page_embedding = get_embedding(page_tokens)
    query_embedding = get_embedding(query_tokens)
    return cosine_similarity(page_embedding, query_embedding)

def find_sentence_in_chunks(content, query, chunk_size=300):
    # query_tokens = word_tokenize(query.lower())
    query_tokens = query.lower().split(' ')
    max_matched_words = 0
    best_sentence = None
    
    if chunk_size > len(content):
        chunk_size = len(content) - 1
    chunks = [content[i:i+chunk_size] for i in range(0, len(content), chunk_size)]
    
    for chunk in chunks:
        # sentence_tokens = word_tokenize(chunk.lower())
        sentence_tokens = chunk.lower().split(' ')
        # matched_words = sum(1 for word in sentence_tokens if word in query_tokens)
        matched_words = len(set(sentence_tokens) & set(query_tokens))
        
        if matched_words > max_matched_words:
            max_matched_words = matched_words
            best_sentence = chunk
    
    result = ""
    if best_sentence:
        for word in best_sentence.split(" "):
            if word.lower() in query_tokens:
                result += f"<strong>{word}</strong> "
            else:
                result += f"{word} "
    result = "... " + result + " ..."
    return result

def page_rank(pages, query):
    scores = []
    for page in pages:
        page["score"] = float(my_relevance_score(page["content"], query))
        page["summary"] = find_sentence_in_chunks(page["content"], query)
    sorted_pages = sorted(pages, key=lambda x: x.get('score', 0), reverse=True)
    return sorted_pages

def ranked_search_result(web_pages, query):
    ranked_pages= page_rank(web_pages, query)
    return ranked_pages