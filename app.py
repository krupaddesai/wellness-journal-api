from flask import Flask, jsonify, request
from flask_restful import Resource, Api, reqparse
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import datetime
from flask_marshmallow import Marshmallow


app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://krupadesai:dance.7890@127.0.0.1/flask'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text())
    date = db.Column(db.DateTime, default = datetime.datetime.now)

    def __init__(self, title, body):
        self.title = title
        self.body = body

class ArticleSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'body','date')

article_schema = ArticleSchema()
articles_schema = ArticleSchema(many=True)

@app.route('/get', methods = ['GET'])
def get_articles():
    all_articles = Articles.query.all()
    results = articles_schema.dump(all_articles)
    return jsonify(results)

@app.route('/get/<id>/', methods = ['GET'])
def post_details(id):
    article = Articles.query.get(id)
    return article_schema.jsonify(article)

@app.route('/add', methods = ['POST'])
def add_article():
    title = request.json['title']
    body = request.json['body']

    articles = Articles(title, body)
    db.session.add(articles)
    db.session.commit()
    return article_schema.jsonify(articles)

@app.route('/update/<id>/', methods = ['PUT'])
def update_article(id):
    article = Articles.query.get(id)
    title = request.json['title']
    body = request.json['body']
    article.title = title
    article.body = body

    db.session.commit()
    return article_schema.jsonify(article)


@app.route('/delete/<id>/', methods = ['DELETE'])
def article_delete(id):
    article = Articles.query.get(id)
    db.session.delete(article)
    db.session.commit()
    return article_schema.jsonify(article)









api = Api(app)
cors = CORS(app, resources={r"/anagram": {"origins": "http://localhost:3000"}})





if __name__ == '__main__':
    app.run(debug=True)


























def index():
    return "welcome"


@app.endpoint('words.json')
@app.route('/words.json', methods=['POST', 'DELETE', 'GET'])
def bouncer():
    global dictionary_words
    if request.method == 'POST':

        return '', 201

    elif request.method == 'DELETE':
        dictionary_words = []
        return '', 204

    elif request.method == 'GET':
    
  
        counts = {
   
    
        }
        return jsonify({"counts": counts}), 200


@app.route('/anagrams/<word>', methods=['GET', 'DELETE'])
def gramanas(word):
    global dictionary_words
    if request.method == 'DELETE':
        real_word = word.split('.')[0]
        lower_case = request.args.get('ignorecase')
        deletes = []
        for dict_word in dictionary_words:
            if str(lower_case) == 'yes':
                if sorted(dict_word.lower()) == sorted(real_word.lower()):
                    deletes.append(dict_word)
            else:
                if sorted(dict_word) == sorted(real_word):
                    deletes.append(dict_word)
        for i in deletes:
            dictionary_words.remove(i)
        return '', 204

    else:
        how_many = request.args.get('limit')
        lower_case = request.args.get('ignorecase')
        real_word = word.split('.')[0]
        anagrams = []
        for dict_word in dictionary_words:
            if str(lower_case) == 'yes':
                if sorted(dict_word.lower()) == sorted(real_word.lower()):
                    anagrams.append(dict_word)
            else:
                if sorted(dict_word) == sorted(real_word):
                    anagrams.append(dict_word)
        if real_word in anagrams:
            anagrams.remove(real_word)
        if how_many is not None:
            anagrams = anagrams[0:int(how_many)]
        return jsonify({'anagrams': anagrams}), 200


@app.route('/words/<word>', methods=['DELETE', 'GET'])
def deleteOne(word):
    global dictionary_words
    if request.method == 'DELETE':
        real_word = word.split('.')[0]
        dictionary_words.remove(real_word)
        return '', 200

    elif request.method == 'GET':
        if word.split('.')[0] in dictionary_words:
            result = "True"
        else:
            result = "False"
        return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)