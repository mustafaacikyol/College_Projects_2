from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import os
from pymongo import MongoClient
from bson import ObjectId
from elasticsearch import Elasticsearch
from datetime import datetime

app = Flask(__name__)
pdf_urls = []

# Connect to MongoDB
client = MongoClient()
db = client['academy']

# Connect to Elasticsearch
es = Elasticsearch(hosts=["http://localhost:9200"]) 
INDEX_NAME = 'articles_index'
DOC_TYPE = 'article'

def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(index=INDEX_NAME, body={
            'mappings': {
                'properties': {
                    'name': {'type': 'text'},
                    'authors': {'type': 'text'},
                    'type': {'type': 'text'},
                    'date': {'type': 'date'},
                    'publisher': {'type': 'text'},
                    'keywords_se': {'type': 'text'},
                    'keywords': {'type': 'text'},
                    'abstract': {'type': 'text'},
                    'references': {'type': 'text'},
                    'citation': {'type': 'text'},
                    'doi': {'type': 'text'},
                    'url': {'type': 'text'},
                }
            }
        })

""" def serialize_article(article):
    # Convert ObjectId to string
    if '_id' in article and isinstance(article['_id'], ObjectId):
        article['_id'] = str(article['_id'])

    return article

def index_article(article):
    article = serialize_article(article)
    es.index(index=INDEX_NAME, body=article) """

def index_article(article):
    article_id = article.pop('_id', None)  # Remove _id field from the body
    es.index(index=INDEX_NAME, body=article, id=article_id)  # Pass _id as a separate parameter

# Function to download PDF files
def download_pdf(pdf_urls, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    for i, pdf_url in enumerate(pdf_urls):
        response = requests.get(pdf_url)
        if response.status_code == 200:
            with open(os.path.join(folder, f"article_{i+1}.pdf"), 'wb') as f:
                f.write(response.content)
            print(f"Downloaded article_{i+1}.pdf")
        else:
            print(f"Failed to download article_{i+1}.pdf")

@app.route('/')
def index():
    collection = db['article']
    # Fetch data from MongoDB
    articles_data_cursor = collection.find()  # This retrieves all documents from the collection
    articles_data = list(articles_data_cursor)  # Convert cursor to a list
    articles_data_length = len(articles_data)
    date_list = []
    for article in articles_data:
        date_from_db = datetime.strptime(str(article['date']), "%Y-%m-%d %H:%M:%S")
        date_list.append(date_from_db)
    """ # List all indices
    indices = es.indices.get_alias(index="*")
    print("Indices:", indices)

    # Get information about a specific index
    index_info = es.indices.get(index=INDEX_NAME)
    print("Index Info:", index_info) """
    return render_template('index.html', articles_data=articles_data, articles_data_length = articles_data_length, date_list=date_list)

@app.route('/results', methods=['POST'])
def result():
    query = request.form['query']
    articles = scrape_dergipark(query)
    articles_length = len(articles)
    folder = "pdf"  # Specify the folder where you want to save PDFs
    download_pdf(pdf_urls, folder)  # Call the function to download PDFs
    insert_data(articles)
    return render_template('results.html', articles=articles, articles_length=articles_length)

@app.route('/article-detail', methods=['GET'])
def detail():
    collection = db['article']
    article_id = request.args.get('id')  # Get the article ID from the URL parameter
    # Fetch article details based on the article_id from your data source
    article = fetch_article_details(article_id)  # You need to implement this function
    return render_template('article-detail.html', article=article)

@app.route('/search', methods=['POST'])
def search():
    correction = False
    query = request.form['search-query']
    if query:
        search_query = get_corrected_query(query)
        if search_query != query:
            correction = True
        # Use Elasticsearch's search API to search for articles
        search_results = es.search(index=INDEX_NAME, body={'query': {'multi_match': {'query': search_query, 'fields': ['name', 'authors', 'type',  'publisher', 'keywords_se', 'keywords', 'abstract', 'references', 'citation', 'doi', 'url']}}})
        # Extract relevant information from search results
        # articles = [{'name': hit['_source']['name'], 'authors': hit['_source']['authors']} for hit in search_results['hits']['hits']]
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        for article in articles:
            date_from_db = datetime.strptime(str(article['_source']['date']), "%Y-%m-%dT%H:%M:%S")
            article['_source']['date']=date_from_db
        return render_template('search.html', articles=articles, search_query=search_query, correction=correction, query=query)
    else:
        return render_template('search.html', articles=None, search_query=search_query, correction=correction, query=query)

@app.route('/filter', methods=['POST'])
def filter():
    name = request.form['name']
    authors = request.form['authors']
    type = request.form['type']
    date = request.form['date']
    publisher = request.form['publisher']
    keywords_se = request.form['keywords_se']
    keywords = request.form['keywords']
    abstract = request.form['abstract']
    references = request.form['references']
    citation = request.form['citation']
    doi = request.form['doi']
    url = request.form['url']

    if name:
        # Use Elasticsearch's search API to search for articles
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'name': name}}})
        # Extract relevant information from search results
        # articles = [{'name': hit['_source']['name'], 'authors': hit['_source']['authors']} for hit in search_results['hits']['hits']]
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif authors:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'authors': authors}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif type:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'type': type}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif date:
        """ # Parse the selected year to create a date range
        start_date = datetime.strptime(f'01.01.{date}', '%d.%m.%Y')
        end_date = datetime.strptime(f'31.12.{date}', '%d.%m.%Y')

        # Use a range query to filter documents within the selected year
        search_results = es.search(index=INDEX_NAME, body={
            "query": {
                "range": {
                    "date": {
                        "gte": start_date.strftime('%d.%m.%Y'),
                        "lte": end_date.strftime('%d.%m.%Y')
                    }
                }
            }
        }) """

        """ # Parse the selected year to create a date range
        selected_year = int(date)
        start_date = datetime(selected_year, 1, 1)
        end_date = datetime(selected_year, 12, 31)

        # Use a range query to filter documents within the selected year
        search_results = es.search(index=INDEX_NAME, body={
            "query": {
                "bool": {
                    "must": [
                        {
                            "range": {
                                "date": {
                                    "gte": f"01.01.{selected_year}||.y",
                                    "lte": f"31.12.{selected_year}||.y"
                                }
                            }
                        }
                    ]
                }
            }
        }) """

        selected_year = int(date)
        # Create a range query to match documents within the year
        start_date = datetime(selected_year, 1, 1).strftime('%Y-%m-%d')
        end_date = datetime(selected_year, 12, 31).strftime('%Y-%m-%d')
        print(start_date)
        print(end_date)

        search_results = es.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "range": {
                        "date": {
                            "gte": start_date,
                            "lte": end_date
                        }
                    }
                }
            }
        )

        """ search_results = es.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "range": {
                        "date": {
                            "time_zone": "+01:00",        
                            "gte": "20.12.2023||/y", 
                            "lte": "now"                  
                        }
                    }
                }
            }
        ) """

        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        for article in articles:
            date_from_db = datetime.strptime(str(article['_source']['date']), "%Y-%m-%dT%H:%M:%S")
            article['_source']['date']=date_from_db
        return render_template('filter.html', articles=articles)
    elif publisher:
        # search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'publisher': publisher}}})
        search_results = es.search(index=INDEX_NAME, body={
            'query': {
                'multi_match': {
                    'query': publisher,
                    'fields': ['publisher'],  # Add other fields if needed
                    'operator': 'and'  # This ensures that all words must match
                }
            }
        })
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif keywords_se:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'keywords_se': keywords_se}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif keywords:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'keywords': keywords}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif abstract:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'abstract': abstract}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif references:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'references': references}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif citation:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'citation': citation}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif doi:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'doi': doi}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    elif url:
        search_results = es.search(index=INDEX_NAME, body={'query': {'match': {'url': url}}})
        articles = []
        for hit in search_results['hits']['hits']:
            article = {'_source': hit['_source'], '_id': hit['_id']}
            articles.append(article)
        return render_template('filter.html', articles=articles)
    else:
        return render_template('filter.html', articles=None)

""" def get_corrected_query(query):
    # Use Elasticsearch's suggest feature or fuzzy query to get suggestions
    suggestion = es.search(index=INDEX_NAME, body={"suggest": {"text": query, "simple_phrase": {"phrase": {"field": "name"}}}})
    corrected_query = suggestion['suggest']['simple_phrase'][0]['options'][0]['text']
    return corrected_query """

""" def get_corrected_query(query):
    # Use Elasticsearch's suggest feature or fuzzy query to get suggestions
    suggestion = es.search(index=INDEX_NAME, body={"suggest": {"text": query, "simple_phrase": {"phrase": {"field": "keywords"}}}})
    
    # Check if suggestions are available
    if 'simple_phrase' in suggestion['suggest'] and suggestion['suggest']['simple_phrase'][0]['options']:
        # Get the corrected query from the suggestions
        corrected_query = suggestion['suggest']['simple_phrase'][0]['options'][0]['text']
        return corrected_query
    else:
        # If no suggestions are available, return the original query
        return query """

def get_corrected_query(user_query):
    # Use Elasticsearch's "did you mean" feature to get suggestions for corrected query
    # Here's a simplified example, you may need to adjust based on your Elasticsearch setup
    suggestion = es.search(index=INDEX_NAME, body={
        "suggest": {
            "text": user_query,
            "simple_phrase": {
                "phrase": {
                    "field": "keywords",
                    "size": 1,
                    "gram_size": 3,
                    "direct_generator": [{
                        "field": "keywords",
                        "suggest_mode": "always"
                    }]
                }
            }
        }
    })

    # Extract corrected query from Elasticsearch response
    if suggestion['suggest']['simple_phrase'][0]['options']:
        corrected_query = suggestion['suggest']['simple_phrase'][0]['options'][0]['text']
    else:
        corrected_query = user_query  # Use original query if no suggestion found

    return corrected_query

@app.template_filter('highlight_search_term')
def highlight_search_term(text, search_query):
    if text is not None and search_query is not None:
        # Convert both text and search_query to lowercase for case-insensitive search
        text_lower = text.lower()
        search_query_lower = search_query.lower()

        # Split the search query into words
        search_words = search_query_lower.split()

        # Iterate over each word in the search query
        for word in search_words:
            # Replace word occurrences with bold formatting
            highlighted_text = text_lower.replace(word, f"<b>{word}</b>")
            text_lower = highlighted_text  # Update text_lower for the next word

        return highlighted_text
    else:
        return text

def insert_data(articles):
    collection = db['article']  # Replace 'articles' with your actual collection name

    # Insert each article into the collection
    for article in articles:
        collection.insert_one(article)
        index_article(article)

    # Close the MongoDB connection
    # client.close()

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
        date_string = article_soup.find('span', class_='article-subtitle').text.split(',')[-1].strip()
        date = datetime.strptime(date_string, "%d.%m.%Y")
        publisher = article_soup.find('div', class_='kt-heading kt-align-center').a.h1.text.strip()
        keywords = article_soup.find('div', class_='article-keywords').p.text.strip()
        # abstract = article_soup.find('div', class_='article-abstract data-section').p.text.strip()
        try:
            references = article_soup.find('div', class_='article-citations').div.text.strip()
        except AttributeError:
            references = None

        try:
            citation = article_soup.find('div', class_='article-doi').div.text.split(':')[-1].strip()
        except AttributeError:
            citation = None

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
            'citation': citation,
            'doi': doi,
            'url': url
        }
        
        articles.append(data)
        counter += 1

        for link in article_soup.find_all('a', title=True):
            if link['title'] == "Makale PDF linki":
                pdf_urls.append("https://dergipark.org.tr"+link['href'])
    
    
    # Render the template with the extracted data
    return articles

def fetch_article_details(article_id):
    collection = db['article']
    # Fetch the article details from MongoDB based on the provided article ID
    article = collection.find_one({'_id': ObjectId(article_id)})
    return article

if __name__ == '__main__':
    create_index()
    app.run(debug=True)
