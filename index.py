from flask import Flask, render_template, request
import requests
import re

app = Flask(__name__)

def detect_language(url):
    try:
        if not url.startswith(("http://", "https://")):
            url = "http://" + url
        
        response = requests.get(url)
        html_content = response.text
        
        language_identifiers = {
            'Python': r'Python',
            'JavaScript': r'JavaScript|JS',
            'Java': r'Java',
            'Ruby': r'Ruby',
            'PHP': r'PHP',
            'C#': r'C#',
            'C++': r'C\+\+|C\+\+11',
            'Go': r'Go',
            'Swift': r'Swift',
            'TypeScript': r'TypeScript',
            'HTML': r'HTML',
            'CSS': r'CSS'
        }
        
        detected_languages = []
        
        for language, pattern in language_identifiers.items():
            if re.search(pattern, html_content, re.IGNORECASE):
                detected_languages.append(language)
        
        if detected_languages:
            return detected_languages
        else:
            return 'No language detected.'
    
    except requests.exceptions.RequestException:
        return 'Error: Unable to retrieve website content.'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website_url = request.form['url']
        detected_languages = detect_language(website_url)
        return render_template('result.html', url=website_url, languages=detected_languages)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
