def summarizeText(text):
    from transformers import PegasusForConditionalGeneration, PegasusTokenizer
    
    model_name = "google/pegasus-xsum"
    tokenizer = PegasusTokenizer.from_pretrained(model_name)
    model = PegasusForConditionalGeneration.from_pretrained(model_name)
    
    tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
    
    summary_ids=model.generate(
        tokens["input_ids"],
        num_beams=4,
        max_length=60,
        early_stopping=True
    )
    
    summary = tokenizer.decode(summary_ids[0], skip_special_token=True)
    return summary