def llm_summary(text):

    from groq import Groq
    import os
    from decouple import config

    
    client = Groq(
        api_key = config('API_KEY')
    )

    # Create the chat completion request to summarize the text
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": f"Summarize the following educational notes \n{text}\n clearly and concisely, focusing on the key concepts. Structure the summary as a list of bullet points for easy reference. Aim to make the summary detailed yet simple, ensuring it is suitable for college and school students to understand complex ideas easily. Keep it large",
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content
    
                