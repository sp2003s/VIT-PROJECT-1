def merge_broken_sentences(text):
    import re
    cleaned_text = re.sub(r'(?<!\.)\n+', ' ', text)  
    cleaned_text = re.sub(r'\s+', ' ', cleaned_text) 
    return cleaned_text

def extractive_summ(text):
    import spacy
    from spacy.lang.en.stop_words import STOP_WORDS
    from string import punctuation

    nlp = spacy.load('en_core_web_sm')

    doc = nlp(text)
    doc

    import re

    text = merge_broken_sentences(text)
    print(text)

    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text != '\n']
    
    custom_stopwords = list(STOP_WORDS) + ['april', 'contd', 'example']

    # Allowed parts of speech for filtering
    allowed_pos = ['ADJ', 'PROPN', 'VERB', 'NOUN']

    # Function to remove noise and filter tokens
    def filter_noise(text):
        doc = nlp(text)
        tokens = [token.text.lower() for token in doc 
                if not token.is_stop and not token.is_punct 
                and token.text.lower() not in custom_stopwords 
                and token.pos_ in allowed_pos]
        return tokens

    filtered_tokens = filter_noise(text)
    print(filtered_tokens)
    
    tokens1 = list(filtered_tokens)
    
    from collections import Counter
    word_freq = Counter(tokens1)
    max_freq = max(word_freq.values())
    
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
        
    def get_sentences(text):
        doc = nlp(text)
        sentences = [sent.text.strip() for sent in doc.sents]
        return sentences

    # Get sentences from the merged text
    sentences = get_sentences(text)
    print(sentences)
    
    
    from sklearn.feature_extraction.text import TfidfVectorizer
    import pandas as pd
    from heapq import nlargest

    # Function to score sentences using TF-IDF
    def score_sentences(sentences):
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(sentences)
        
        word_freq = dict(zip(vectorizer.get_feature_names_out(), vectorizer.idf_))
        
        sent_score = {}
        for sent in sentences:
            for word in sent.split():
                if word.lower() in word_freq.keys():
                    if sent not in sent_score.keys():
                        sent_score[sent] = word_freq[word.lower()]
                    else:
                        sent_score[sent] += word_freq[word.lower()]
        
        return sent_score

    sent_scores = score_sentences(sentences)

    print(pd.DataFrame(list(sent_scores.items()), columns=['Sentence', 'Score']))
    
    pd.DataFrame(list(sent_scores.items()), columns = ['sentence', 'score'])
    
    num_sentences = 5
    n = nlargest(num_sentences, sent_scores, key = sent_scores.get)
    out = " ".join(n)
    
    return out