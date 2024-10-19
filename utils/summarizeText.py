def summarizeText(text, n):
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    
    summary_ids = model.generate(
        tokens["input_ids"],
        num_beams=4,   
        no_repeat_ngram_size=3,   
        min_length=n*25,  
        max_length=n*175,
        early_stopping=True, 
        length_penalty=2.0  
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    return summary