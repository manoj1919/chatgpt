import openai

# Your GPT-4 API key
#API_KEY = "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"
openai.api_key = "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"

# Function to summarize an article using GPT-3 chat model
""" def summarize_article(article_text):
    try:
        # Format the prompt as a conversation
        conversation = [
            {"role": "system", "content": "You are a helpful assistant that summarizes articles."},
            {"role": "user", "content": f"Please summarize the following article: {article_text}"}
        ]
        
        response = openai.ChatCompletion.create(
            engine="gpt-4",  # Use the appropriate chat model engine
            messages=conversation,
            max_tokens=100,  # Limit the response length
            temperature=0,  # Adjust the randomness of the response
            api_key=openai.api_key  # Your API key
        )
        
        # Extract the assistant's response from the conversation
        summary = response["choices"][0]["message"]["content"].strip()
        return summary
    except Exception as e:
        print(f"Error: {e}")
        return None """

def get_article_text(url):
    from newspaper import Article

    # Use newspaper3k to extract the article
    article = Article(url)
    article.download()
    article.parse()

    # Get the article text
    article_text = article.text

    # Print the extracted article text
    return (article_text)


def get_summary(system_q,text):
    
    res=openai.ChatCompletion.create(
      model="gpt-4",
      max_tokens=450,
      temperature=0,
      messages=[
            {"role": "system", "content": system_q},
            {"role": "user", "content": "consider the following input text:{"+text+"}"},            
        ]
    )
    return (res)
# Example article text
article_text = """
The quick brown fox jumps over the lazy dog. The fox is known for its agility and speed. 
The dog, on the other hand, is known for its laziness and lack of motivation. 
Despite the differences between the two animals, they share a common habitat and are often seen together.
"""

# Summarize the article
#summary = summarize_article(article_text)
summary = get_summary("You are a helpful assistant that summarizes articles.",get_article_text("https://www.foxbusiness.com/technology/google-microsoft-tout-ai-advances-improve-search"))

print("Summary:", summary["choices"][0]["message"]["content"])
#print("Summary:", summary["choices"][0])
