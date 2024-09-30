# pip install spacy
# !python -m spacy download en_core_web_sm

import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from collections import Counter
import pandas as pd
from heapq import nlargest

def extractive_text_summarization(text, num_of_sentences):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    
    # Creating sentence tokens out of the text
    tokens = [token.text.lower() for token in doc if not token.is_stop and not token.is_punct and token.text != '\n']
    
    # List of tokenised words
    tokens1 = []
    stopwords = list(STOP_WORDS)
    allowed_pos = ['ADJ', 'PROPN', 'VERB', 'NOUN']

    for token in doc:
        if token.text in stopwords or token.text in punctuation:
            continue
        if token.pos_ in allowed_pos:
            tokens1.append(token.text)
            
    # Count word frequencies
    word_freq = Counter(tokens1)
    
    max_freq = max(word_freq.values())
    
    # Normalizing the word frequencies
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
        
    # Sentence tokens
    sent_tokens = [sent.text for sent in doc.sents] 
    
    # Sentence scores
    sent_score = {}
    for sent in sent_tokens:
        for word in sent.split():
            if word.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word]
                else:
                    sent_score[sent] += word_freq[word]
                    
    # Creating a dataframe for the sentence scores
    pd.DataFrame(list(sent_score.items()), columns = ['sentence', 'score'])
    
    n = nlargest(num_of_sentences, sent_score, key = sent_score.get)
    
    # Summarized text
    summarized_text = ' '.join(n)
    
    return summarized_text
            
            
    