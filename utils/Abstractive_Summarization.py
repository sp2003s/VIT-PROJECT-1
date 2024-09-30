# pip install tensorflow
# pip install transformers
# pip install tf-keras

from transformers import pipeline

def abstractive_text_summarization(text):
    
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)

    
    return summary
