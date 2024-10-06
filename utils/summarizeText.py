def summarizeText(text):
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    
    summary_ids=model.generate(
        tokens["input_ids"],
        num_beams=8,
        min_length=100,
        max_length=500,
        early_stopping=True
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary