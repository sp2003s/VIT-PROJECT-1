def cleanText(text):
    import re
    
    text = re.sub(r'\s+', ' ', text).strip()
    text = re.sub(r'[^A-Za-z0-9.,!?;:()\'\" ]+', '', text)
    
    text = re.sub(r'Page \d+', '', text)
    irrelevant_phrases = ["References", "Appendix", "Table of Contents"]
    for phrase in irrelevant_phrases:
        text = text.replace(phrase, '')
        
    text = text.lower()
    text = re.sub(r'\s+([?.!,])', r'\1', text)
    
    return text