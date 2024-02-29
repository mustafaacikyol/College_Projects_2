from flask import Flask, render_template, request
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def search():
    query = request.form['query']
    articles = scrape_dergipark(query)
    articles_length = len(articles)
    print(articles_length)
    return render_template('results.html', articles=articles, articles_length=articles_length)

def scrape_dergipark(query):
    # URL of the page you want to scrape
    url = f'https://dergipark.org.tr/tr/search?q={query}&section=articles'
    
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract information from the elements
    articles = []
    counter = 0
    for article in soup.find_all('div', class_='article-card'):
        if counter == 10:
            break

        name = article.find('h5', class_='card-title').a.text.strip()
        try:
            abstract = article.find('div', class_='kt-list kt-list--badge matches').text.strip()
        except AttributeError:
            abstract = None
        
        article_url = article.find('h5', class_='card-title').a['href']  # Extract detail page URL
        # Access detail page and perform web scraping
        article_response = requests.get(article_url)
        article_soup = BeautifulSoup(article_response.text, 'html.parser')
        
        # Example: Extracting abstract from detail page
        authors = article_soup.find('p', class_='article-authors').text.strip()
        try:
            type = article_soup.find('div', class_='kt-portlet__head-title').span.text.strip()
        except AttributeError:
            type = None
        date = article_soup.find('span', class_='article-subtitle').text.split(',')[-1].strip()
        publisher = article_soup.find('div', class_='kt-heading kt-align-center').a.h1.text.strip()
        keywords = article_soup.find('div', class_='article-keywords').p.text.strip()
        # abstract = article_soup.find('div', class_='article-abstract data-section').p.text.strip()
        try:
            references = article_soup.find('div', class_='article-citations').div.text.strip()
        except AttributeError:
            references = None

        try:
            # doi = article_soup.find('div', class_='article-doi').a.text.split('/')[-1][-2].strip()
            doi = article_soup.find('div', class_='article-doi').a['href'].split('org/')[-1]
        except AttributeError:
            doi = None

        url = article.find('h5', class_='card-title').a['href']

        data = {
            'name': name,
            'authors': authors,
            'type': type,
            'date': date,
            'publisher': publisher,
            'keywords_se': query,
            'keywords': keywords,
            'abstract': abstract,
            'references': references,
            'doi': doi,
            'url': url
        }
        
        articles.append(data)
        counter += 1
    
    # Render the template with the extracted data
    return articles

if __name__ == '__main__':
    app.run(debug=True)
