def summarizeText(text, n):
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    
    # Load the pre-trained model and tokenizer
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    # Tokenize input text
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    
    # Generate the summary with enhanced parameters
    summary_ids = model.generate(
        tokens["input_ids"],
        num_beams=4,  # Increase the number of beams to get better results
        no_repeat_ngram_size=3,  # Prevent repetition of 3-grams
        min_length=n*25,  # Minimum length of the summary
        max_length=n*175,  # Maximum length of the summary
        early_stopping=True,  # Stop when an optimal result is found
        length_penalty=2.0  # Encourage longer summaries without repetition
    )
    
    # Decode the summary
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    
    # Return the summary after further cleaning if needed
    return summary