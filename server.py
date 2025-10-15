from flask import Flask, request, render_template
app = Flask(__name__)

@app.get('/')
@app.get('/home')
def home():
    return '<h1>Home Page</h1>'

if __name__ == '__main__':
    app.run(debug=True)