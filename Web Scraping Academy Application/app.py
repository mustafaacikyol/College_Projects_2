from flask import Flask, redirect, url_for, request, render_template
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)

if __name__ == '__main__':
   app.run(port=5000, debug = True)