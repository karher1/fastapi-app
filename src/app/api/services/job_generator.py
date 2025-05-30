import openai

#stream genereator for job description
#this will send chunks of information incrementally to the client
def openai_stream(prompt: str): #this will be the prompt for the OPENAI API
    response = openai.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        stream=True)
    for chunk in response: #this itirates through the response 
        if "choices" in chunk and chunk["choices"][0]["delta"].get("content"):
            content = chunk["choices"][0]["delta"]["content"]
            if content:
                yield content

    