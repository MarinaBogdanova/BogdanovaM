from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres@localhost:5432/postgres'
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

from views import *

if __name__ == '__main__':
    app.run()
