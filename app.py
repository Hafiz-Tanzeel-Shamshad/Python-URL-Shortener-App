from flask import Flask, request, redirect, render_template, url_for
import string
import random

app = Flask(__name__)
url_mapping = {}

def generate_short_url():
    characters = string.ascii_letters + string.digits
    while True:
        short_url = ''.join(random.choices(characters, k=6))
        if short_url not in url_mapping:
            return short_url

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        
        if original_url in url_mapping:
            short_url = url_mapping[original_url]
        else:
            short_url = generate_short_url()
            url_mapping[original_url] = short_url

        return render_template('index.html', short_url=short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_url(short_url):
    for original_url, mapped_short_url in url_mapping.items():
        if mapped_short_url == short_url:
            return redirect(original_url)
    return f'URL for "{short_url}" not found.'

if __name__ == '__main__':
    app.run(debug=True)
