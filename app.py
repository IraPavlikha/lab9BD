from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import os

app = Flask(__name__)

# Підключення до MongoDB через URI з .env
client = MongoClient(os.getenv("MONGODB_URI"))
db = client["book_catalog"]

@app.route('/')
def index():
    books = db.books.find()
    return render_template('index.html', books=books)

# Books CRUD
@app.route('/books/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        db.books.insert_one({"title": title, "author": author, "description": description})
        return redirect(url_for('index'))
    return render_template('books/add.html')

@app.route('/books/edit/<book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    book = db.books.find_one({"_id": book_id})
    if request.method == 'POST':
        title = request.form['title']
        author = request.form['author']
        description = request.form['description']
        db.books.update_one({"_id": book_id}, {"$set": {"title": title, "author": author, "description": description}})
        return redirect(url_for('index'))
    return render_template('books/edit.html', book=book)

@app.route('/books/delete/<book_id>')
def delete_book(book_id):
    db.books.delete_one({"_id": book_id})
    return redirect(url_for('index'))

# Reviews CRUD
@app.route('/reviews/add', methods=['GET', 'POST'])
def add_review():
    if request.method == 'POST':
        book_id = request.form['book_id']
        review_text = request.form['review_text']
        db.reviews.insert_one({"book_id": book_id, "review_text": review_text})
        return redirect(url_for('index'))
    books = db.books.find()
    return render_template('reviews/add.html', books=books)

@app.route('/reviews/edit/<review_id>', methods=['GET', 'POST'])
def edit_review(review_id):
    review = db.reviews.find_one({"_id": review_id})
    if request.method == 'POST':
        review_text = request.form['review_text']
        db.reviews.update_one({"_id": review_id}, {"$set": {"review_text": review_text}})
        return redirect(url_for('index'))
    return render_template('reviews/edit.html', review=review)

@app.route('/reviews/delete/<review_id>')
def delete_review(review_id):
    db.reviews.delete_one({"_id": review_id})
    return redirect(url_for('index'))

# Users CRUD
@app.route('/users/add', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        db.users.insert_one({"name": name, "email": email, "password": password, "role": role})
        return redirect(url_for('index'))
    return render_template('user/add.html')

@app.route('/users/edit/<user_id>', methods=['GET', 'POST'])
def edit_user(user_id):
    user = db.users.find_one({"_id": user_id})
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        db.users.update_one({"_id": user_id}, {"$set": {"name": name, "email": email, "password": password, "role": role}})
        return redirect(url_for('index'))
    return render_template('user/edit.html', user=user)

@app.route('/users/delete/<user_id>')
def delete_user(user_id):
    db.users.delete_one({"_id": user_id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
