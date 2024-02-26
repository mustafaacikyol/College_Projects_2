from flask import Flask, redirect, url_for, request, render_template
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

""" @app.route('/hello')
def hello_world():
   return 'hello world' """

""" @app.route('/hello/<name>')
def hello_name(name):
   return 'Hello %s!' % name """

""" @app.route('/blog/<int:postID>')
def show_blog(postID):
   return 'Blog Number %d' % postID

@app.route('/rev/<float:revNo>')
def revision(revNo):
   return 'Revision Number %f' % revNo """

""" @app.route('/admin')
def hello_admin():
   return 'Hello Admin'

@app.route('/guest/<guest>')
def hello_guest(guest):
   return 'Hello %s as Guest' % guest

@app.route('/user/<name>')
def hello_user(name):
   if name =='admin':
      return redirect(url_for('hello_admin'))
   else:
      return redirect(url_for('hello_guest',guest = name)) """

""" @app.route('/success/<name>')
def success(name):
   return 'welcome %s' % name

@app.route('/index',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['search']
      return redirect(url_for('success',name = user))
   else:
      user = request.args.get('search')
      return redirect(url_for('success',name = user)) """

""" @app.route('/qwe')
def hello_name():
   return render_template('hello.html') """

""" @app.route('/hello/<int:score>')
def hello_name(score):
   return render_template('hello.html', marks = score) """

""" @app.route('/')
def result():
   dict = {'phy':50,'che':60,'maths':70}
   return render_template('hello.html', result = dict) """

""" @app.route("/")
def index():
   return render_template("index.html") """

""" @app.route('/')
def student():
   return render_template('student.html')

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result) """

""" @app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result) """


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/results', methods=['POST'])
def search():
    query = request.form['query']
    results = scrape_google_scholar(query)
    results_length = len(results)
    return render_template('results.html', results=results, results_length=results_length)

def scrape_google_scholar(query):
    url = f"https://scholar.google.com/scholar?q={query}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract relevant information from the soup object
    # Example: titles, authors, publication dates, etc.
    results = []
    for item in soup.find_all('div', class_='gs_ri'):
        title = item.find('h3', class_='gs_rt').a.text
        if title is None:
            title = item.find("h3", class_="gs_rt").find("span").text
        authors = item.find('div', class_='gs_a').text.split('-')[0].strip()
        #   authors = item.find('div', class_='gs_a').text
        #   type = item.find('div', class_='gs_a').text.split(' - ')[0]
        date_element = item.find('div', class_='gs_a').text
        date = date_element.split('-')[-2].strip()  # Extract the last part as the date
        if ',' in date:
         parts = date.split(',')

         # Get the second part (index 1)
         date = parts[1].strip()  # Use strip() to remove leading/trailing whitespace
        
        link = item.find('h3', class_='gs_rt').a['href']
        results.append({'title': title, 'authors': authors, 'type': type, 'date': date, 'link': link})
    return results
   


if __name__ == '__main__':
   app.run(port=5000, debug = True)