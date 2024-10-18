# pip install tensorflow
# pip install transformers
# pip install tf-keras

def clean_text(text):
    """
    Clean the input text by removing special characters, numbers, and multiple spaces.
    """
    import re
    # Remove non-alphabetic characters and numbers
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    # Trim leading and trailing spaces
    text = text.strip()
    return text

def post_process_summary(summary):
    """
    Post-process the summary to remove unwanted characters or noise.
    """
    summary = clean_text(summary)  # Clean the summary using the same cleaning function
    summary = " ".join(summary.split())  # Remove any extra spaces
    return summary

def abstractive_text_summarization(text, number_of_Pages):
    """
    Perform abstractive text summarization using a pre-trained T5 model.
    """
    from transformers import pipeline

    # Clean the input text to remove unnecessary characters
    text = clean_text(text)
    
    # Initialize the T5 summarization pipeline
    summarizer = pipeline("summarization", model="t5-base", tokenizer="t5-base")
    
    # Generate the summary with appropriate parameters
    summary = summarizer(
        text, 
        max_length=150 * number_of_Pages, 
        min_length=50 * number_of_Pages, 
        do_sample=True, 
        top_k=50, 
        temperature=0.7
    )
    
    # Extract the summary text and clean it further
    summarized_text = " ".join([item['summary_text'] for item in summary])
    summarized_text = post_process_summary(summarized_text)
    
    return summarized_text