from app import app

@app.route('/')
@app.route('/home', methods=['GET'])
def home():
    return '<h1>Home Page</h1>'