#http://stackoverflow.com/questions/19673669/python-no-module-name-pika-when-importing-pika/27987966#27987966
from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def index():
  return render_template('template.html')

@app.route('/my-link/')
def my_link():
  print 'I got clicked!'

  return 'Click.'

if __name__ == '__main__':
  app.run()