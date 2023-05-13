from flask import Flask, render_template, request, send_file
import openai
from newspaper import Article
import pandas as pd
import io
from urllib.parse import urlparse

app = Flask(__name__)

# Your GPT-3 API key
#openai.api_key = "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"
openai.api_key="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"


def summarize_article(text):
    system_q="""You are an expert market analyst. You summarize news articles by following these steps:
Step1: read the user entered article text

step2: summarize the article by following the below rules and remember the summary do not give it as output

rule 1. Never use numbers or names or topics that are not present in the article text
rule 2. Focus on including points with the keywords: 5G, AI, Automotive, Self-driving, ADAS, Cloud, MEC, telecom, infrastructure, base station, RAN, FWA, MIMO, CBRS, cellular, network, broadband, IoT, mobile, processor, SoC, chip, CPU, GPU, Earnings, M&A, merger, investment, regulatory, AR, VR, XR
rule 3. The summary should have 350 to 450 characters, including spaces.
rule 4. End the summary with ...

step3: extract all the words in generated summary that are not present in article text and remember them

step4: for each word in the above step, give an explanation of why the word is present and which part of the article contains that word. If not present, then rewrite the summary do not give it as output
 
Step5: count the number of words in the summary,remember the count

step6: if the count is more than 450 or less than 350, re summarize to get the word count between 350 and 450 donot give it as output

step7: add three dots at the end of the summary text and show"""
    res=openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      max_tokens=450,
      temperature=0,
      messages=[
            {"role": "system", "content": system_q},
            {"role": "user", "content": "consider the following input text:{"+text+"}"},            
        ]
    )
    return (res["choices"][0]["message"]["content"])

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    if 'url' in request.form:
        url = request.form['url']
        if not url or not urlparse(url).scheme:
            return render_template('index.html', error='Invalid URL')
        try:
            article = Article(url)
            article.download()
            article.parse()
            article_text = article.text
            summary = summarize_article(article_text)
            # Pass both the article_text and summary to the template
            return render_template('index.html', article_text=article_text, summary=summary)
        except Exception as e:
            return render_template('index.html', error=str(e))
    elif 'file' in request.files:
        file = request.files['file']
        df = pd.read_csv(file)
        summaries = []
        for url in df['url']:
            article = Article(url)
            article.download()
            article.parse()
            article_text = article.text
            summary = summarize_article(article_text)
            summaries.append(summary)
        df['summary'] = summaries
        excel_file = io.BytesIO()
        writer = pd.ExcelWriter(excel_file, engine='xlsxwriter')
        df.to_excel(writer, index=False)
        writer.save()
        excel_file.seek(0)
        return send_file(excel_file, attachment_filename='summaries.xlsx', as_attachment=True)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
